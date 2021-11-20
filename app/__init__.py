from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
from flask_mail import Mail
import os


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
mail = Mail(app)
from app import routes, models

if not app.debug:
    # Fazer com que a aplicação grave erros num arquivo de log 
    if not os.path.exists('logs'):
        os.mkdir('logs')

        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('App startup')

if __name__ == "__main__":
	app.run(debug=True)