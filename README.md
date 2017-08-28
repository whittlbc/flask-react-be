# Flask React Back-end

## Requirements

* Python 2.7.X
* pip
* virtualenv
* PostgreSQL

## Intallation

1. Install virtualenv if not already installed:

```
$ pip install virtualenv
```

2. Download and install [PostgreSQL](https://www.postgresql.org/download/).

3. Create a new user and new database for this app:

```
$ createuser -s flask-react-be
```
```
$ createdb -O flask-react-be flask-react-be
```

4. Clone this repo:

```
$ git clone https://github.com/whittlbc/flask-react-be && cd flask-react-be
```

5. Add a new `.env` file with the following contents and make sure they're activated:

```
export ENV="dev"
export DATABASE_URL="postgresql://flask-react:flask-react@localhost/flask-react?user=flask-react"
```

6. Create a new virtual environment and activate it:

```
$ virtualenv venv && source venv/bin/activate
```

7. Install requirements:

```
$ pip install -r requirements.txt
```

## Usage

**Interacting with the DB**

To initialize the database for your project, run the following:

```
$ python manage.py db init
```

This should create a `migrations/ directory inside the root of your project.

Whenever you make changes to your `src/models.py` file, you will want to apply them to your database. Doing this requires 2 steps: generating migration files and applying those migrations to the database. These 2 steps can be done with the following commands, respectively:

```
$ python manage.py db migrate
```
```
$ python manage.py db upgrade
```

**Starting the app**

```
$ python app.py
```

## Procfile

This exists for use with Heroku.

## Database Models

You can find these in `src/models.py`.

## Interacting with the Database

Look at `src/dbi.py`, which provides great helper methods for talking to Postgres.

## API Routes

All API routes exist inside `src/routes/`, with routes separated into different files, each corresponding to a different database model.

Currently, `src/routes/user.py` exists as an example of how to go about handling user-related requests. 

**Note**: New route files won't take effect unless `from mynewfile import *` is added to the bottom of `src/routes/__init__.py`.

## SSL & LetsEncrypt

A `letsencrypt.py` route file is already included to help speed up the certificate registration process for LetsEncrypt. To make that endpoint available, do the following:

1. Add `from letsencrypt import *` to the bottom of `src/routes/__init__.py`.
2. Add `LETSENCRYPT_ROUTE_KEY` and `LETSENCRYPT_RESPONSE_KEY` as environment variables. Their values should be provided to you during the certificate request process.

For more info on setting up SSL, a full description can be found in the [front-end repo for this boilerplate](https://github.com/whittlbc/flask-react-fe#setting-up-ssl-support).

## License

MIT  
