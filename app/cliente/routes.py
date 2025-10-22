from flask import redirect, render_template, request, flash, url_for
import app
from . import cliente_blueprint
from datetime import datetime


@cliente_blueprint.route('/agendar_cita', methods=['GET', 'POST'])
def registro():  
    from app import db, models  
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo_electronico = request.form['correo_electronico']
        telefono = request.form['telefono']
        fecha = request.form['fecha_cita']
        hora = request.form['hora_cita']

        # Validaciones existentes
        if not telefono.isdigit():
            return "Error: el teléfono debe contener solo números."
        elif '@' not in correo_electronico or '.' not in correo_electronico:
            return "Error: el correo electrónico no es válido."
        elif not fecha:
            return "Error: la fecha no puede estar vacía."
        elif not hora:
            return "Error: la hora no puede estar vacía."
        elif len(telefono) != 10:
            return "Error: el teléfono debe tener 10 dígitos."


        # Guardar nueva cita
        nueva_cita = models.Cita(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            correo_electronico=correo_electronico,
            fecha=fecha,
            hora=hora
        )
        db.session.add(nueva_cita)
        db.session.commit()

        return '¡Cita agendada correctamente!'
    
    return render_template('index.html')