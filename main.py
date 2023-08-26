import requests
from flask import Flask, render_template, url_for, redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bahae03'


API_KEY = '8caf0227291b44ef9b4121126232608'


@app.route("/")
def home():
    return render_template('home.html')
