import flask
from openahjo_activity_streams import convert
import requests


def get_test_client():
    """
    :rtype : FlaskClient
    :return: the flask test client
    """

    return app.test_client()


def set_remote_url(url):
    app.config['REMOTE_URL'] = url


def set_converter_to(converter):
    app.config['CONVERTER'] = converter

app = flask.Flask(__name__)
set_remote_url('http://dev.hel.fi/paatokset/v1/agenda_item/')
set_converter_to(convert.identity_converter)


@app.route('/')
def show_something():
    openahjo_data = requests.get(app.config['REMOTE_URL'])
    converted_data = app.config['CONVERTER'](openahjo_data.json())
    return flask.jsonify(converted_data)


if __name__ == '__main__':
    app.run()


