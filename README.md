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
    
    > python -m openahjo_activity_streams.server

# Hosting

## Heroku

The included ````Procfile```` configures Heroku to use [gunicorn](http://gunicorn.org/) to serve the site.

## Digital Ocean (or other Ubuntu servers)

### Provisioning

To provision the server, you will need make sure the ```ansible_ssh_host``` variable in deployment.inventory is set to your server's IP address.
Then run ```ansible-playbook deployment_playbook.yml -i deployment.inventory```. This will install docker and a python3 docker image on your server.

### Deployment

First make sure to add the appropriate ssh private key.
Then, add the correct environment varaibles in the ```helsinkiAS.env``` file that is in the ```ops/``` directory.
Lastly, run the deploy script by first entering the ```ops/``` directory by typing ``` cd ops/ ``` and running ```./deploy.sh``` with environment variables ```USER``` and ```IP_ADDRESS``` set according to your server's details.

# Converting from OpenAhjo to Activity Stream 2.0 Format

There is not currently an obvious mapping from the data published by the OpenAhjo project, and the [Activity Stream 2.0 standard](http://www.w3.org/TR/activitystreams-core/).  For term definitions relating to the OpenAhjo project, see [this](https://github.com/City-of-Helsinki/openahjo).  For those relating to the Activity Streams standard, see [this](http://www.w3.org/TR/activitystreams-core/) and [this](http://www.w3.org/TR/activitystreams-vocabulary/).

## High Level Description

At a high level, each activity item has the following structure:

```javascript
{
    "@context": "http://www.w3.org/ns/activitystreams",
    "published": "2015-08-28T11:06:47.879150",
    "@type": "Add",
    "actor": {   },   // json object representing the policy committee making a decision
    "object": {   },  // json object representing the meeting agenda item during which the decision was made
    "target": {   }   // json object representing the issue about which the decision is being made
}
```

This represents a decision (the _object_) being made by a policy committee (the _actor_) about an issue (the _target_).  The closest standard activity type we could identify in the Activity Stream 2.0 specifications was 'Add'.

At this point, the activity stream is served as an unwrapped json list of activity items, in preference to using the activity stream ```orderedCollection``` types:

    [
       {...},
       {...},
       ...
    ]
    
## Actor (OpenAhjo Policymaker)

- Has the ```Group``` @type, as this represents a group of entities capable of acting

## Object (OpenAhjo Agenda Item)

- Has the ```Content``` @type, representing an arbitrary piece of content
- The ```content``` attribute of this object is populated from text contained in the first element of the ```content``` list in the OpenAhjo ```AgendaItem```.

## Target (OpenAhjo Issue)

- Has the ```Content``` @type, representing an arbitrary piece of content
- The ```content``` attribute is populated from the ```summary``` field of the ```issue``` record in the ```AgendaItem```, if the ```summary``` field exists; otherwise left blank.
