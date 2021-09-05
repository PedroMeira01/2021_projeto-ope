from app import app, db
from app.models import Usuario, Barbeiro, Servico, Reserva

@app.shell_context_processor
def make_shell_context():
    return {
            'db': db, 
            'Usuario': Usuario, 
            'Barbeiro': Barbeiro, 
            'Servico': Servico, 
            'Reserva': Reserva
            }