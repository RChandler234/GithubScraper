# Github Scraper Server

REST API to manage database interactions and github scraping. Written in Python using Flask as a server framework and Poetry for package management

## Local Development

### Setup Database

Before running the server, you need to setup a postgres database. Make sure you have Docker setup, then run the following two docker commands from the root directory of the project:

```
docker compose pull
docker compose up postgres-database -d
```

### Initialize Database

You then need to setup the server and initialize the database

Run the following to setup dependencies:

```
poetry install
```

Create a .env file with the following contents for local development:

```
DATABASE_URL="postgresql+pg8000://postgres@localhost:5432/postgres"
CLIENT_URL="http://localhost:5173"
```

Then run the following commands to initialize the database:

```
poetry run flask db init
poetry run flask db migrate
poetry run flask db upgrade
```

### Run the Server

If database setup was sucessful, you should now be able to run the server with the following command:

```
poetry run start
```

Congratulations! You've successfully setup the server, you can now run the client to use the application: [Client README](../client/README.md)

## Useful Commands

Run `poetry test` to run the test suite

Run `poetry debug` to run this app in debug mode

Run `poetry run black .` to run the code formatter

## Docs

This application uses Swagger, go to http://127.0.0.1:5000/apidocs, to see the auto-generated docs

## Implementation Notes

I'm using poetry aliases to setup easier aliases for running and testing the server

I'm using pytest to run the tests and waitress to serve the application in production mode

I'm using SQL-Alchemy as the ORM for database interactions, and I'm using FlaskMigrate (Alembic under the hood) to manage migrations. (using pg8000 to do the actual db interactions since it's a pure python postgresql driver, allows me to avoid system dependecy issues)
