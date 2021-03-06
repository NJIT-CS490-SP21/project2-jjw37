# Milestone 2 Readme

## Requirements
1. `npm install`
2. `pip install -r requirements.txt`
3.  `pip install flask-socketio`
3. `pip install flask-cors`
4. `pip install psycopg2-binary`
5. `pip install Flask-SQLAlchemy==2.1`
4. in directory: `npm install socket.io-client --save`

## For Heroku
2. `heroku login -i`
1. `heroku create --buildpack heroku/python`
2. `heroku buildpacks:add --index 1 heroku/nodejs`
3. `git push heroku milestone_2:main` if your branch is different than replace milestone_2 with your branch name
4. `heroku addons:create heroku-postgresql:hobby-dev`
5. `heroku config` copy the DATABASE_URL
6. make an .env file and type export DATABASE_URL='value you copied from before goes here' 

## Setup
1. Run `echo "DANGEROUSLY_DISABLE_HOST_CHECK=true" > .env.development.local` in the project directory
2. `npm run start` and `python app.py`

## Problems/future additions
1. 
2. 

## Techincal issues
1. 
2. 
