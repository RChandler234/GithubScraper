### Github Scraper Server

REST API written in Python using Flask as a server framework and Poetry for package management to manage database interactions and github scraping

### Commands

Run `poetry install` to setup dependencies

Run `poetry dev` to run this app in development mode

Run `poetry test` to run the test suite

Run `poetry prod` to run the app in production mode

### Implementation Notes

I'm using poetry aliases to setup easier aliases for running and testing the server

I'm using pytest to run the tests and waitress to serve the application in production mode
