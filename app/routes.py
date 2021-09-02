from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', titulo="Home")

@app.route('/autenticacao')
def login():
    return render_template('auth.html', titulo="Login")