import flask

app = flask.Flask(__name__)


@app.route('/')
def show_something():
    return flask.jsonify({"a": 1,
                          "b": "This is a test!"})

if __name__ == '__main__':
    app.run()
