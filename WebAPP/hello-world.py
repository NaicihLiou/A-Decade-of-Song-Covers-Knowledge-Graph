# save this as app.py
import flask
from flask import Flask, render_template

app = flask.Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=50000, debug=True)
