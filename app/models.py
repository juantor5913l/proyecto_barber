from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship


class Cita(db.Model):
    __tablename__ = 'cita'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    servicio = db.Column(db.String(120), nullable=False)
    
    # Relaciones
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    barbero_id = db.Column(db.Integer, db.ForeignKey('barbero.id'), nullable=True)
    
    cliente_rel = db.relationship('Cliente', back_populates='citas')
    barbero_rel = db.relationship('Barbero', back_populates='citas')


class Cliente(db.Model):
    __tablename__ = 'cliente'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    
    # Relación con citas
    citas = db.relationship('Cita', back_populates='cliente_rel', cascade="all, delete-orphan")


class Barbero(db.Model):
    __tablename__ = 'barbero'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    
    citas = db.relationship('Cita', back_populates='barbero_rel', cascade="all, delete-orphan")
