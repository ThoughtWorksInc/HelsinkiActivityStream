import flask
import requests


def get_test_client():
    """
    :rtype : FlaskClient
    :return: the flask test client
    """

    return app.test_client()


def set_remote_url(url):
    app.config['REMOTE_URL'] = url


app = flask.Flask(__name__)
set_remote_url('http://dev.hel.fi/paatokset/v1/agenda_item/')


@app.route('/')
def show_something():
    response = requests.get(app.config['REMOTE_URL'])
    return flask.jsonify(response.json())


if __name__ == '__main__':
    app.run()
