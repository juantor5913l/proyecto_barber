#dependencia de flask
from flask import Flask
from flask import render_template,url_for,session
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import random
import string
#Dependencia de configuracion 
from .config import Config #El punto es para indicarle a python que los archivos estan en el mismo paquete

#dependencia de modelos
from flask_sqlalchemy import SQLAlchemy

#dependencia de las migraciones
from flask_migrate import Migrate

#crear el objeto flask
app = Flask(__name__)

#Configuracion del objeto flask
app.config.from_object(Config)


#Importar el modulo 
#from app.administrador import admin_blueprint
#from app.cliente import cliente_blueprint
#Vincular submodulos del proyecto
#app.register_blueprint(admin_blueprint)
#app.register_blueprint(cliente_blueprint)
#crear el objeto de modelos:


db = SQLAlchemy(app)





#crear el obejeto de migracion 
migrate=Migrate(app,db)

from .models import Cita, Cliente, Barbero
@app.route('/')
def index():
    return render_template('index.html')
    