from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', titulo="Home")

@app.route('/autenticacao', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', titulo="Login", form=form)

# Usuarios
@app.route('/cadastro')
def cadastro():
    return render_template('cadastrar_usuario.html', titulo="Cadastre-se!")