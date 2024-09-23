# Auth-service
A kutumbita auth micro-service for authentication and authorization

## Technologies
- Django 2.1
- DRF 3.9
- Redis 3.0.1
- PyJWT 1.6.4

## Installation
- Fork This repo
- Clone this repo on your local
- `cd auth-service`
- Copy `.env.example` file into new `.env` and update all parameters of your own.
- Install and setup Postgress (For ubuntu 18.40 LTS)
  - `sudo apt update`
  - `sudo apt install postgresql postgresql-contrib`
  - `sudo -i -u postgres`
  - `psql`
  - `\password postgres`
  - `\q`
- Install pgadmin3 for maintain database (optional)
- pipenv --three (If you have not installed pipenv before visit this link(https://pypi.org/project/pipenv/)
- pipenv install (Install dependencies)
- Install redis (https://redis.io/download)

## Runing procedure
if you use pgadmin3:
- Open pgadmin3
- Click into a socket icon left-top of the pgadmin window.
- Fill up the form
  - name: `KithAI`
  - host: `localhost`
  - maintain db: `postgres`
  - username: `postgres`
  - password: `postgres`
- Click ok. If you won't see any error then its ok.
- Now expand `server groups` then `servers` then `KithAI`. Then you find databases. Click right button on it and create new database.
  - give database name: `auth`
  - Owner: `postgres`
- click ok.
- If you use command line then setup the above config or you can customise it. Update the settings file if needed.
- Run Server with this command `./runserver.sh`

## Testing
- `python manage.py test app_name`

## API Documentation
https://documenter.getpostman.com/view/5851478/RzZFCbjL

### User
- POST - `api/v1/users`
- LOGIN
  - POST - `api/v1/web/login` (For Dashboard Users)
  - POST - `api/v1/mobile/login` (For Mobile Users)
- LOGOUT - `api/v1/logout`
- VERIFY_USER
  - POST - `api/v1/verify`

## Architechture
![auth_login](https://user-images.githubusercontent.com/44048291/51301780-9a52b080-1a5a-11e9-8da5-50a876ddff24.png)



![token_verify](https://user-images.githubusercontent.com/44048291/51301899-ed2c6800-1a5a-11e9-9c62-85adec5a927d.png)


## TODO
- Need to implement reset password, change password, refresh token, and authorization endpoint.
