from flask import render_template, redirect, url_for, flash, request, session
from app import app, db
from app.forms import EditarPerfilUsuario, LoginForm, CadastrarUsuario,\
CadastrarBarbeiro, EditarPerfilBarbeiro
from app.models import Usuario, Barbeiro, Servico, Reserva
from datetime import datetime, timedelta, time, date
import json

#  -------------------------------------------------

# RESERVAS -------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """ Tela de agendamento """
        # Verifica se o usuário já está logado
    if 'id_usuario' in session:
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
    # Se não estiver logado, redireciona para o login
    else:
        flash('Por favor, faça o login para acessar esta página.')
        return redirect(url_for('login'))

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

    quadro = [
        horario 
        for horario in quadro_de_horarios
        if horario not in reservas
    ]
    
    return quadro

@app.route('/cadastrar_reserva', methods=['POST'])
def cadastrar_reserva():
    if 'id_usuario' in session:
        id_barbeiro = request.form['barbeiro']
        data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        horario = request.form['horario']
        # Convertendo a string para timedelta para determinar o horário fim
        horario_inicio = datetime.strptime(horario, '%H:%M:%S')
        horario_fim = horario_inicio + timedelta(minutes=29)
        usuario_id = session['id_usuario']

        existe_reserva = verifica_se_existe_reserva(horario_inicio.time(), data, int(id_barbeiro))

        if not existe_reserva:
            reserva = Reserva(
                horario_inicio=horario_inicio.time(),
                horario_fim=horario_fim.time(),
                data=data,
                usuario_id=usuario_id,
                barbeiro_id=id_barbeiro,
                servico_id=1
            )

            db.session.add(reserva)
            db.session.commit()

            flash('Sua reserva foi agendada com sucesso!\
            Consulte as informações no seu histórico de agendamento.')
            return redirect(url_for('historico_reservas'))
        else:
            flash('Já existe uma reserva marcada neste horário,\
                 por favor, escolha outro horário.')

            return redirect(url_for('index'))
    # Se não estiver logado, redireciona para o login
    else:
        return redirect(url_for('login'))

def verifica_se_existe_reserva (horario, data, barbeiro):
    r = Reserva.query.filter_by(horario_inicio=horario, data=datetime.date(data),
    barbeiro_id=barbeiro).first()

    return r

@app.route('/historico_reservas')
def historico_reservas():
    """Lista todas as reservas de um usuário"""
    usuario_id = session['id_usuario']

    reservas = Reserva()
    reservas = reservas.reservas_por_cliente(usuario_id)

    return render_template(
            'historico_reservas.html', 
            titulo='Histórico de Reservas', 
            reservas=reservas
        )

# AUTENTICAÇÃO  -----------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Verifica se o usuário já está logado
    if 'id_usuario' in session:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Busca usuário com credenciais compátiveis a recebida
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        
        if usuario is None or not usuario.checar_senha(form.senha.data):
            flash('E-mail ou senha inválido(s).')
            return redirect(url_for('login'))
        # Guarda o id do usuário na sessão
        session['id_usuario'] = usuario.id
        return redirect(url_for('index'))

    return render_template('login.html', titulo="Login", form=form)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    # Verifica se o usuário já está logado
    if 'id_barbeiro' in session:
        return redirect(url_for('admin'))

    form = LoginForm()
    if form.validate_on_submit():
        # Busca usuário com credenciais compátiveis a recebida
        barbeiro = Barbeiro.query.filter_by(email=form.email.data).first()
        
        if barbeiro is None or not barbeiro.checar_senha(form.senha.data):
            flash('E-mail ou senha inválido(s).')
            return redirect(url_for('login_admin'))
        # Guarda o id do usuário na sessão
        session['id_barbeiro'] = barbeiro.id_barbeiro
        return redirect(url_for('admin'))

    return render_template('login_admin.html', titulo="Login", form=form)

@app.route('/logout')
def logout():
    """."""
    if 'id_usuario' in session:
        session.clear()
    return redirect(url_for('login'))

# USUÁRIOS -----------------------------------------
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """ Cadastro de usuários no site """
    # Verifica se o usuário já está logado
    if 'id_usuario' in session:
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

@app.route('/editar_perfil/<id>', methods=['GET', 'POST'])
def editar_perfil(id):
    if 'id_usuario' in session:
        if session['id_usuario'] == int(id):
            usuario = Usuario.query.filter_by(id=id).first()
            form = EditarPerfilUsuario(usuario.email)

            if form.validate_on_submit():
                usuario.nome = form.nome.data
                usuario.email = form.email.data
                if form.nova_senha:
                    usuario.criptografar_senha(form.nova_senha.data)

                db.session.add(usuario)
                db.session.commit()
                
                flash('Suas informações foram editadas com sucesso!')

                return redirect(url_for('editar_perfil', id=id))

            elif request.method == 'GET':
                form.nome.data = usuario.nome
                form.email.data = usuario.email

            return render_template('editar_perfil_usuario.html', titulo='Editar perfil', form=form)
        # Se tentar editar o perfil de outro usuário
        return redirect(url_for('editar_perfil', id=id))
    else:
        flash('Por favor, faça o login para acessar esta página.')
        return redirect(url_for('login'))

# BARBEIROS ------------------------------------------
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/funcionarios')
def listagem_funcionarios():
    barbeiros = Barbeiro.query.all()
    return render_template('barbeiro/listagem_funcionarios.html', barbeiros=barbeiros)

@app.route('/cadastrar_barbeiro', methods=['GET', 'POST'])
def cadastrar_barbeiro():
    form = CadastrarBarbeiro()
    if form.validate_on_submit():
        barbeiro = Barbeiro(nome=form.nome.data, email=form.email.data)
        barbeiro.criptografar_senha(form.senha.data)

        db.session.add(barbeiro)
        db.session.commit()

        flash('Conta criada com sucesso!')

        return redirect(url_for('listagem_funcionarios'))

    return render_template('barbeiro/cadastrar_barbeiro.html', 
        titulo='Cadastrar barbeiro',
        form=form
    )

@app.route('/editar_perfil_barbeiro/<id>', methods=['GET', 'POST'])
def editar_perfil_barbeiro(id):
    if 'id_barbeiro' in session:
        if session['id_barbeiro'] == int(id):
            barbeiro = Barbeiro.query.filter_by(id=id).first()
            
            form = EditarPerfilUsuario(barbeiro.email)

            if form.validate_on_submit():
                barbeiro.nome = form.nome.data
                barbeiro.email = form.email.data
                if form.nova_senha:
                    barbeiro.criptografar_senha(form.nova_senha.data)

                db.session.add(barbeiro)
                db.session.commit()
                
                flash('Suas informações foram editadas com sucesso!')

                return redirect(url_for('editar_perfil_barbeiro', id=id))

            elif request.method == 'GET':
                form.nome.data = barbeiro.nome
                form.email.data = barbeiro.email

            return render_template('editar_perfil_barbeiro.html', titulo='Editar perfil', form=form)
        # Se tentar editar o perfil de outro usuário
        return redirect(url_for('editar_perfil_barbeiro', id=id))
    else:
        flash('Por favor, faça o login para acessar esta página.')
        return redirect(url_for('login_admin'))
