from app import app
from flask import render_template
from flask_mail import Message
from app import mail

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def enviar_email_recuperacao_senha(usuario):
    senha_temporaria = usuario.gerar_senha_temporaria()
    send_email('[Barbearia] Nova senha temporária',
                sender=app.config['ADMINS'][0],
                recipients=[usuario.email],
                text_body=render_template('email/redefinir_senha.txt',
                                            usuario=usuario, senha=senha_temporaria),
                html_body=render_template('email/redefinir_senha.html',
                                            usuario=usuario, senha=senha_temporaria))
    
    return senha_temporaria

def enviar_email_recuperacao_senha_barbeiro(barbeiro):
    senha_temporaria = barbeiro.gerar_senha_temporaria()
    send_email('[Barbearia] Nova senha temporária',
                sender=app.config['ADMINS'][0],
                recipients=[barbeiro.email],
                text_body=render_template('email/redefinir_senha_barbeiro.txt',
                                            barbeiro=barbeiro, senha=senha_temporaria),
                html_body=render_template('email/redefinir_senha_barbeiro.html',
                                            barbeiro=barbeiro, senha=senha_temporaria))

    return senha_temporaria