# social_network

![image](https://github.com/IsThatASkyline/social_network/assets/67318020/207aa4d4-d30c-46a9-ba9f-1a7f95e00a41)


## Description

Simple REST API social network with FastAPI


## Functional requirements:

- There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)
- As a user I need to be able to signup and login
- As a user I need to be able to create, edit, delete and view posts
- As a user I can like or dislike other users’ posts but not my own 
- The API needs a UI Documentation (Swagger/ReDoc)

## Install
First you need clone git repo using
```
git clone https://github.com/IsThatASkyline/social_network.git
cd social_network
```

## Run the project:
### Using Docker-compose:
Set environment variables in .docker-compose.env (you can leave variables and it will work) and run
```
docker-compose up --build
```

### Using terminal:
You need run PostgreSQL database by yourself, then set variables in .env file, then run
```
pip install -r requirements.txt
alembic revision --autogenerate -m 'Init'
alembic upgrade head
uvicorn src.main:app --reload
```

## API Documentation
To see docs visit
```
http://localhost:8000/docs
```
## Testing API
Tests are in 'tests' folder, you can run them
### If you use Docker-compose:
First you need to create database for test (TEST_POSTGRES_DB in .docker-compose.env)
1) Check CONTAINER_ID of running postgres:
```
docker ps
```
2) Connect to container using
```
docker exec -it CONTAINER_ID bash
```
3) Connect to Postgres
```
psql -U postgres
```
4) Create database for tests 
```
CREATE DATABASE test_db;
```
5) After creating database you can check CONTAINER_ID of app and connect to it:
```
docker ps
```
```
docker exec -it CONTAINER_ID bash
```
6) And run tests
```
pytest -v -s tests/
```
   
### And if you use terminal just run:
```
pytest -v -s tests/
```

------------------------------------
## What could be improved
1) Make special init file to create databases from docker-compose up and not to create them manually https://stackoverflow.com/questions/49024243/how-do-i-create-a-database-within-a-docker-container-using-only-the-docker-compo
2) Use an in-memory DB for storing post likes and dislikes (As a cache, that gets updated whenever new likes and dislikes get added) https://github.com/long2ice/fastapi-cache
3) Use emailhunter.co for verifying email existence on registration (or just background tasks (Celery for example))
4) Use https://clearbit.com/platform/enrichment for getting additional data for the user on signup (or u can create OneToOne table 'user_profile' and store additional data there)
