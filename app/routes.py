from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import LoginForm, CadastrarUsuario
from app.models import Usuario, Barbeiro, Servico, Reserva
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import timedelta, date
import json

# HOME -------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """ Tela de agendamento """
    # Se não houver dados na request, seta um valor padrão
    data = request.args.get('data' , date.today())
    id_barbeiro = request.args.get('id_barbeiro', 1)

    barbeiros = busca_barbeiros()
    reservas = busca_reservas(data, id_barbeiro)
    quadro_de_horarios = gerar_quadro_horarios(reservas)

    dados = {
        'barbeiros': barbeiros,
        'quadro_de_horarios': quadro_de_horarios,
        'barbeiro_escolhido': id_barbeiro
    }
    # Se houverem dados na request, retorna apenas o quadro de horários
    if request.args:
        return json.dumps(dados['quadro_de_horarios'])

    return render_template('index.html', titulo="Home", dados=dados)

def busca_barbeiros():
    """ Busca todos os barbeiros """
    dados = Barbeiro.query.all()
    return dados
# Busca reservas do barbeiro escolhido na data passada
def busca_reservas(data, id_barbeiro):
    dados = Reserva.query.\
    filter_by(data=data, barbeiro_id=id_barbeiro).all()
    return dados

def gerar_quadro_horarios(reservas):
    """ Gera um quadro de horários completo
    de acordo com o horário de funcionamento
    do estabelecimento """
    horario = timedelta(hours=10)
    horario_limite = timedelta(hours=19)
    # Horário de almoço
    horarios_restritos = [
        timedelta(hours=13), 
        timedelta(hours=13, minutes=30)
    ]
    
    acrescimo = timedelta(minutes=30)
    
    quadro_de_horarios = [str(horario)]
    
    while horario < horario_limite:
        horario += acrescimo
        if horario not in horarios_restritos:
            quadro_de_horarios.append(str(horario))

    quadro_horarios = quadro_horarios_vagos(quadro_de_horarios, reservas)

    return quadro_horarios

def quadro_horarios_vagos(quadro_de_horarios, reservas):
    """ Formata o quadro de horários e mantém apenas os 
    horários disponíveis """
    reservas = [str(r.horario_inicio) for r in reservas]

    for horario in quadro_de_horarios:
        if horario in reservas:
            horario_reservado = quadro_de_horarios.index(horario)
            quadro_de_horarios.pop(horario_reservado)

    return quadro_de_horarios


# AUTENTICAÇÃO  -----------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    """"."""
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
    """."""
    logout_user()
    return redirect(url_for('index'))

# USUÁRIOS -----------------------------------------
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """ Cadastro de usuários no site """
    # Verifica se o usuário já está logado
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = CadastrarUsuario()

    if form.validate_on_submit():
        # Popula um objeto de Usuario
        usuario = Usuario(nome=form.nome.data,  email=form.email.data)
        usuario.criptografar_senha(form.senha.data)
        # Adiciona ao banco
        db.session.add(usuario)
        db.session.commit()

        flash('Sua conta foi criada com sucesso!')
        return redirect(url_for('login'))
    
    return render_template('cadastrar_usuario.html', titulo="Crie sua conta", form=form)