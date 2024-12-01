# Github Scraper

Fullstack Project to track project data from Github based on Github usernames.

Frontend is written in typescript using React, Backend is written in python using Flask and Poetry.

## Local Development

Follow the Instructions in the [Server README](./server/README) and then the [Client README](./client/README.md) to run the application in development mode

## API Documentation

When running the server, go to http://127.0.0.1:5000/apidocs to see the auto-generated Swagger docs

## CodeGen

I used [create-vite](https://vite.dev/guide/) to make the starter code for the frontend

I used [poetry new](https://python-poetry.org/docs/basic-usage/) to generate the starter poetry project for the backend

I used ChatGPT for suggestions and debugging issues as I was figuring out how to setup the poetry/ flask backend since I haven't worked with them in-depth before. I particularly had issues with setting up SQLAlchemy initially, all the project.toml configuration stuff, and setting up the tests and mocking at first (I'm used to jest in Typescript). I also used it for color suggestions for the frontend and debugging some CSS issues I had trying to make sure only the cards were scrollable on the querying pages.
