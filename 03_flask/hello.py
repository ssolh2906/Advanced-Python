from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/about')
def about():
    return 'Hi, this is description for my flask app.'


@app.route('/contact')
def contact():
    return 'Talk to me solheetucker@gmail.com'