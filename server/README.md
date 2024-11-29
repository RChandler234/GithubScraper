### Github Scraper Server

REST API written in Python using Flask as a server framework and Poetry for package management to manage database interactions and github scraping

### Commands

Run `poetry install` to setup dependencies

Run `poetry dev` to run this app in development mode

Run `poetry test` to run the test suite

Run `poetry prod` to run the app in production mode

`poetry run flask db init`
`poetry run flask db migrate`
`poetry run flask db upgrade`

### Implementation Notes

I'm using poetry aliases to setup easier aliases for running and testing the server

I'm using pytest to run the tests and waitress to serve the application in production mode

I'm using SQL-Alchemy as the ORM for database interactions, and I'm using FlaskMigrate (Alembic under the hood) to manage migrations. (using pg8000 to do the actual db interactions since it's a pure python postgresql driver, allows me to avoid system dependecy issues)

You can run with pure PostgresSQL setup, or run the server/ database dockerized

Doing my own serializing (transformers)

Setup Swagger/ API stuff: https://www.geeksforgeeks.org/documenting-restful-apis-with-swagger/?ref=oin_asr1
