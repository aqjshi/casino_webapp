from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class GameOfferForm(FlaskForm):
    host_role = SelectField('Play as', choices=[('row', 'Row Player'), ('col', 'Col Player')], validators=[DataRequired()])
    matrix = SelectField('Select Payoff Matrix', choices=[
        ('[[1,-5],[-5,9]]', '[[1,-5],[-5,9]]'),
        ('[[2,-3],[-5,6]]', '[[2,-3],[-5,6]]')
    ], validators=[DataRequired()])
    incentive = DecimalField('Incentive', validators=[DataRequired(), NumberRange(min=0)])
    # host selects a fixed row if playing row or fixed col if playing col
    host_choice = SelectField('Your Fixed Choice (Index)', choices=[('0', '0'), ('1', '1')], validators=[DataRequired()])
    submit = SubmitField('Offer Game')

class JoinGameForm(FlaskForm):
    game_id = IntegerField('Game ID', validators=[DataRequired()])
    # if host fixed a row, client picks a column; if host fixed a col, client picks a row
    client_choice = SelectField('Your Choice (Index)', choices=[('0', '0'), ('1', '1')], validators=[DataRequired()])
    submit = SubmitField('Join Game')
