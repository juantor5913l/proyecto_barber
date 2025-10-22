from app import db
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Text, DECIMAL
from datetime import datetime

from sqlalchemy.orm import relationship

class Cita(db.Model):
    __tablename__ = 'cita'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    correo_electronico = db.Column(db.String(120))
    telefono = db.Column(db.String(20))
    fecha = db.Column(Date, nullable=False)
    hora = db.Column(Time, nullable=False)

class DiaRestringido(db.Model):
    __tablename__ = 'dia_restringido'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)

