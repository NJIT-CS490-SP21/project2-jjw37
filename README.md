# Milestone 2 Readme

## Requirements
1. `npm install`
2. `pip install -r requirements.txt`
3.  `pip install flask-socketio`
3. `pip install flask-cors`
4. `pip install psycopg2-binary`
5. `pip install Flask-SQLAlchemy==2.1`
4. in directory: `npm install socket.io-client --save`

## For Heroku and database
2. `heroku login -i`
1. `heroku create --buildpack heroku/python`
2. `heroku buildpacks:add --index 1 heroku/nodejs`
3. `git push heroku milestone_2:main` if your branch is different than replace milestone_2 with your branch name
4. `heroku addons:create heroku-postgresql:hobby-dev`
5. `heroku config` copy the DATABASE_URL
6. make an .env file and type export DATABASE_URL='value you copied from before goes here' 

## Setup
1. Run `echo "DANGEROUSLY_DISABLE_HOST_CHECK=true" > .env.development.local` in the project directory
2. run before starting app
`python`
`>> from app import DB`
`>> import models`
`>> DB.create_all()`
`>> admin = models.Player(username='admin', score=100)`
`>> db.session.add(admin)`
`>> db.session.commit()`
`>> exit()`
2. `npm run start` and `python app.py`


## Problems/future additions
1. One problem I would have like to have fixed is to have a logout event that will update the user list as people log out. 
Could be set up similarly to the login event incept on server side could pop the user from the list, then emit the new list to the event same as with login.
2. There is a minor bug for when the game ends on the last move possible, x on move 9, the x player will have correct display, that x has won. Howver every other player will see game was a draw.
I think this could have been fixed by chaning the conditonal statement for displaying game draw, it wasn't getting the correct state for the winner on the other clients.
3. I would have also liked to add along with the logout, a switch player. Basically if player O left, then the spot was open, and then spectator could take his place. 
Implementing this would probably be very tricky, one way would be just to have whoever was third to become player then, as the list would move down 1, so person at index 3 would then be at index 2.
and then have a listener client side for this that then changes the spectator to a player.

## Techincal issues
1. The first issue I encountered was was making the table row of the current user unique from the other rows. I spend a lot trying to figure out how I could use css and conditonal rendering to make this work. 
Eventually I found that I could store the user name in a state when they logged on than in an inline condtional statment inside the style of the row, I would check the userName state, with the name from the array that 
was emitted from server with all usernames. The if the 2 matched it would give it a diferent background color, blue, compared to the others, red.
2. Another problem I had to deal with was how I would tell the server when there was a winner and to update the database accordingly. 
I did some googleing on react hooks and state get a sense of how some other people have tackled similar problems. Eventually I figure that I could just pass in the xNext state to determine if winner was O
or X, and I would keep a isWinner state in the board compotent that would be emitted when the winner function returned a winner. With this I was able to emit the winner event at the right time and be able to determine which player
won and which lost.
