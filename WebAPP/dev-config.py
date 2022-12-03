import flask

app = flask.Flask(__name__)


@app.route("/")
@app.route("/hello")
def hello():
    return "Hello, World ~ !!! Text Text Text ~ !!!"


if __name__ == '__main__':
    app.run()
    # app.run('127.0.0.1:5000', debug=True)
