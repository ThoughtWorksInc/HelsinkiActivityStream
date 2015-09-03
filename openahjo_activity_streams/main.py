# Copyright (c) 2015 ThoughtWorks
#
# See the file LICENSE for copying permission.

import flask
from openahjo_activity_streams import convert
import requests

OPENAHJO_URL = 'http://dev.hel.fi/paatokset/v1/agenda_item/'


def create_app(remote_url=OPENAHJO_URL, converter=convert.to_activity_stream):
    application = flask.Flask(__name__)
    application.config['REMOTE_URL'] = remote_url
    application.config['CONVERTER'] = converter

    @application.route('/')
    def show_something():
        openahjo_data = requests.get(application.config['REMOTE_URL'])
        converted_data = application.config['CONVERTER'](openahjo_data.json())
        return flask.jsonify(converted_data)

    return application

app = create_app()
if __name__ == '__main__':
    app.run()
