# casino_webapp
Qingjian Shi
qshi10@u.rochester.edu

Terminal:

source venv/bin/activate

python test.py  ( for check password input- this is the only vulnerablility for injection. )

python casino.py

then open http://127.0.0.1:5000 port in browser.


Precreated Users: 

username: bob
password: 12345

username: alice
password: 54321

You can create your own user, you start with 1000 dollars


Try joining a game first there are available games on the market in join a game. Enter game id, 
the list above has the available games you can play, this is a async game, so the host has already chosen, 
just choose the index of either row or col, opposite of what the host is. 
Then you win or lose, automatically applies to your account- you can see in home. 

Offer game: 
You can choose either row or col, the payoff matrix you want to play, the index you choose for the row or col, 
and what you offer to the client, a decimal > 0. then you wait for another user to pick your game. 



Deeper Desc:

Game Logic:
This is a turn based matching that uses persistent and open database of a 
simple casino game. The game is simple row-player col-player payoff matrix game. 
Row player has 2 rows they can choose, col player has 2 cols they can choose. 

The matrix can be chosen out of a set of public "fair" matrices, 
{[1,-5], [-5,9]}
{[2,-3], [-5,6]}

A person can offer a game to become a host, or a person can be a client and join the game. 
The host can choose if they want to be the row player or the col player, and the client must like the
conditions of the host if they want to join the host's game. An incentive, greater than equal 0, must be 
served by the host to the client to pay the game. This sounds like a bad deal to host a game, 
but you would be surprised. 


Features: 
I implemented a block chain type transaction recording. For debugging, and demonstration, the blockchain 
containing of all actions and transactions are viewable in the blockchain tab. In a real setting, you would 
just not show game host's fixed choice in the blockchain. I made the games async so its faster and compatible with 
REST, also it solves the problem with queuing/matchmaking theory- beyond the scope of this course. 



Files: 
app/main/views.py controls html
app/main/errors.py control escape page
app/forms.py controls login, register, offer game, join game - 4 actions you can take to alter the db
app/models.py has 5 main objects
User: contain name, hased pass, id, balance, also has a pointer to the games they participate in
Game: game id, host id, client id, host role, payout matrix, client choice, host choice, and state (still offering or no)
Transaction: transaction id, block number, transaction type (offer, join, result), client, host, game id, optional notes 
HostOffering: offering id, host, picked_host_role, payout matrix, incentive, game_id


static/ contains css
templates/ contains html

config.py:  loads the database directory, correctly assigns cookies, and prevent attacker reduce vulnerability. 
casino.py: main execution program. 


Extra Note:

In a 2 player zero sum game, players converge to a equilibrium very fast, but when you introduce more
players, the maximal return strategy is much, much harder to converge to- you cannot assume everyone 
behaves the same way, no guarantee the game you offered will be played by the person you pick, everyone
is fair game.







