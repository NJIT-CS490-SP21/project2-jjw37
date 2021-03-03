# Milestone 1 Readme

## Requirements
1. `npm install`
2. `pip install -r requirements.txt`
3.  `pip install flask-socketio`
3. `pip install flask-cors`
4. in directory: `npm install socket.io-client --save`

## Setup
1. Run `echo "DANGEROUSLY_DISABLE_HOST_CHECK=true" > .env.development.local` in the project directory
2. `npm run start` and `python app.py`

## Problems/future additions
1. One thing in the program I wanted to add was for the game to not allow the other player to make a move when its the other player's turn.
One way I could have implemented this is through 2 states containting a boolean value , isX isO, that is set when user is logged in first or second
,and then add a contional statement to the click handlers to check the isx/iso states aswell as the game state isXNext.
2. I would have also like to add in a state that contains the user's username, that they entered in, then  mark in the userList which one they are, through css.

## Techincal issues
1. One issue I ran into was how to determine if a user is a spectator or player. A player is either the first or second user to login, and a spectator is the 3rd and onward 
login. After looking up some documentation on react state hooks I came up with a solution. To solve it I implemented a counter server side in the python file that kept tracked of the logins and sent it out in an emit, on the client side in board, there was a listener
for this event and then using conitional statments and 2 boolean states, isplayer and isspectator, I would use the counter to determine if the user was a player or spectator and set the states.
2. Another issue I had was how to render the board after the user logins. I looked at the example react code from class, and googles on contional rendering in react. For the solution I created a state isLogin
that would start as false and then be changed to true once the user logged in by pressing the button. Also to make it so the login screen would only be displayed before user logged in, I put the it in a contional statement 
in the render with the board components, based on the value of isLogin. Since the isLogin is by default false it would display the login page, when the login button was hit, in the button handler it would change it to true, and 
the board component would then render instead of the login screen.
