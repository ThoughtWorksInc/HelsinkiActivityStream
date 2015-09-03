# HelsinkiActivityStream
Publish OpenAhjo (https://github.com/City-of-Helsinki/openahjo) most recent agenda items in Activity Streams 2.0 format.

# Setting up for Development

Requires Python 3.4

## Creating a Python Virtual Environment

At the base level of the repository, create a python virtual environment using the ````pyvenv```` tool:

    > pyvenv venv

Activate the environment with (again from the base level of the repo):

    > source venv/bin/activate

(You can return to your default Python environment by typing ````deactivate```` at the command line)

Install development dependencies and run tests and linter with:

    > ./pre_push.sh

## Run Server Locally

At the repository root execute the following from the command line:
    
    > python -m openahjo_activity_streams.main

# Hosting

## Heroku

The included ````Procfile```` configures Heroku to use [gunicorn](http://gunicorn.org/) to serve the site.
