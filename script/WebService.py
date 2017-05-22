from flask import Flask

app = Flask(__name__)

from flask import views

from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"