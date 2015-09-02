import flask
import requests

app = flask.Flask(__name__)

REMOTE_URL = "http://localhost:3000"


@app.route('/')
def show_something():
    response = requests.get(REMOTE_URL + "/test.json")

    return flask.jsonify(response.json())

if __name__ == '__main__':
    app.run()
