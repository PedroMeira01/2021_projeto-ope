from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Usuario
from flask import session

# Para os formulários do site, usamos a extensão FlaskWTF
# que é uma parte do pacote WTForms. Os formulários do site
# serão representados por classes que herdarão a classe FlaskForm
# do pacote FlaskWTF

class LoginForm(FlaskForm):
    # Os atributos da classe serão os campos do formulário e eles
    # recebem instância de classes do "WTForms" de acordo com o tipo
    # de dado que irá receber, tem também como parâmetro o tipo de
    # validação que irá protegê-lo, como por exemplo a "DataRequired"
    # que obriga o usuário a preencher o campo. O tipo de validação
    # vem do módulo "validators" do pacote WTForms.

    # O primeiro parametro das instâncias abaixo corresponde a label do formulário
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_me = BooleanField('Lembrar Me')
    entrar = SubmitField('Entrar')

class CadastrarUsuario(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmação de senha', 
        validators=[
            DataRequired(),
            EqualTo('senha')
        ]
    )
    cadastrar = SubmitField('Cadastrar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario is not None:
            raise ValidationError('O e-mail inserido já está sendo usado por outro usuário!')

class EditarPerfilUsuario(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha_atual = PasswordField('Senha atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar nova senha', 
        validators=[
            DataRequired(),
            EqualTo('nova_senha')
        ]
    )
    editar = SubmitField('Editar')

    def __init__(self, email_original, *args, **kwargs):
        super(EditarPerfilUsuario, self).__init__(*args, **kwargs)
        self.email_original = email_original

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            if usuario.id != session['id_usuario']:
                raise ValidationError('O e-mail inserido já está sendo usado por outro usuário!')
    
    def validate_senha_atual(self, senha_atual):
        usuario = Usuario.query.filter_by(email=self.email_original).first()
        if not usuario.checar_senha(senha_atual.data):
            raise ValidationError('A senha atual está incorreta.')


