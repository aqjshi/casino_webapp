from flask import render_template, flash, redirect, url_for, request
from app import db
from app.main import bp
from app.forms import RegistrationForm, LoginForm, GameOfferForm, JoinGameForm
from app.models import User, Game, Transaction, HostOffering
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        # Query all users except the current one
        users = User.query.all()
    else:
        users = []
    return render_template('index.html', title='Home', users=users)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/offer_game', methods=['GET', 'POST'])
@login_required
def offer_game():
    form = GameOfferForm()
    if form.validate_on_submit():
        game = Game(
            host_id=current_user.id,
            host_role=form.host_role.data,
            incentive=form.incentive.data,
            state='offering',
            host_choice=form.host_choice.data  # store host fixed choice
        )
        # Use eval for demo purposes only; in production, use safe parsing (e.g. json.loads with proper structure)
        game.set_matrix(eval(form.matrix.data))
        db.session.add(game)
        db.session.commit()
        
        # Create Host Offering record (if you use this structure)
        offering = HostOffering(
            host_id=current_user.id,
            host_role=form.host_role.data,
            incentive=form.incentive.data,
            game_id=game.id
        )
        offering.set_matrix(eval(form.matrix.data))
        db.session.add(offering)
        db.session.commit()
        
        # Log transaction as game offer
        tx = Transaction(
            block_number=1,
            tx_type='game_offer',
            host_user=current_user.username,
            game_id=game.id,
            details=str({
                'host_role': form.host_role.data,
                'matrix': form.matrix.data,
                'incentive': form.incentive.data,
                'host_choice': form.host_choice.data
            })
        )
        db.session.add(tx)
        db.session.commit()
        
        flash(f'Game offered successfully! Game ID: {game.id}')
        return redirect(url_for('main.index'))
    return render_template('offer_game.html', title='Offer Game', form=form)

@bp.route('/join_game', methods=['GET', 'POST'])
@login_required
def join_game():
    form = JoinGameForm()
    available_games = Game.query.filter_by(state='offering').all()
    
    if form.validate_on_submit():
        game = Game.query.filter_by(id=form.game_id.data, state='offering').first()
        if game is None:
            flash('Game not found or already joined.')
            return redirect(url_for('main.join_game'))
        
        # Save client's choice from form
        game.client_id = current_user.id
        game.state = 'completed'
        game.client_choice = form.client_choice.data  # stored as string
        
        matrix = game.get_matrix()
        # Compute payoff based on roles:
        if game.host_role == 'row':
            # Host fixed a row index; client chooses a column index.
            host_index = int(game.host_choice)
            client_index = int(form.client_choice.data)
            payout = matrix[host_index][client_index]
        elif game.host_role == 'col':
            # Host fixed a column index; client chooses a row index.
            host_index = int(game.host_choice)
            client_index = int(form.client_choice.data)
            payout = matrix[client_index][host_index]
        else:
            flash('Invalid host role.')
            return redirect(url_for('main.join_game'))
        
        # Calculate payouts
    
        payout_to_host = payout - game.incentive
        payout_to_client = payout + game.incentive

        host = User.query.get(game.host_id)
        client = User.query.get(game.client_id)

        # Check for self-play: if the same user is both host and client, net effect should be zero.
        if host.id == client.id:
            payout_to_host = 0
            payout_to_client = 0
        else:
            host.balance += payout_to_host
            client.balance += payout_to_client

        # Log transaction for joining
        tx_join = Transaction(
            block_number=1,
            tx_type='game_join',
            host_user=host.username,
            client_user=client.username,
            game_id=game.id,
            details=str({'action': 'join', 'client_choice': form.client_choice.data})
        )
        db.session.add(tx_join)
        
        # Log transaction for game result
        tx_result = Transaction(
            block_number=1,
            tx_type='game_result',
            host_user=host.username,
            client_user=client.username,
            game_id=game.id,
            details=str({
                'host_choice': game.host_choice,
                'client_choice': game.client_choice,
                'payout_to_host': payout_to_host,
                'payout_to_client': payout_to_client
            })
        )
        db.session.add(tx_result)
        
        db.session.commit()
        flash(f'Joined game {game.id}. Payouts processed.')
        return redirect(url_for('main.index'))
    
    return render_template('join_game.html', title='Join Game', form=form, available_games=available_games)

@bp.route('/blockchain')
@login_required
def blockchain():
    transactions = Transaction.query.all()
    return render_template('blockchain.html', title='Blockchain Ledger', transactions=transactions)
