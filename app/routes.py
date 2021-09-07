from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import LoginForm, CadastrarUsuario
from app.models import Usuario
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

# HOME -------------------------------------------------
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', titulo="Home")

# AUTENTICAÇÃO  -----------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Verifica se o usuário já está logado
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    # Verifica se passou nas validações do FlaskForm
    if form.validate_on_submit():
        # Busca o usuário com o e-mail informado no banco
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        # Verifica se o usuário existe e se a senha está correta
        if usuario is None or not usuario.checar_senha(form.senha.data):
            flash('E-mail ou senha inválido(s).')
            return redirect(url_for('login'))
        # Realiza o login
        login_user(usuario, remember=form.lembrar_me.data)
        # Verifica se houve uma página requisitada restrita pelo login
        pagina_requisitada = request.args.get('next')
        if not pagina_requisitada or url_parse(pagina_requisitada).netloc != '':
            pagina_requisitada = url_for('index')
        return redirect(pagina_requisitada)

    return render_template('login.html', titulo="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# USUÁRIOS -----------------------------------------
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    # Verifica se o usuário já está logado
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = CadastrarUsuario()
    # Se passar na validação de formulário faça a lógica abaixo
    if form.validate_on_submit():
        # Popula um objeto de Usuario
        usuario = Usuario(nome=form.nome.data,  email=form.email.data)
        usuario.criptografar_senha(form.senha.data)
        # Adiciona ao banco
        db.session.add(usuario)
        db.session.commit()
        flash('Sua conta foi criada com sucesso!')
        return redirect(url_for('login'))
    return render_template('cadastrar_usuario.html', titulo="Crie sua conta: ", form=form)