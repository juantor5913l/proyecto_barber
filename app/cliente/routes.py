from flask import redirect, render_template, request, flash, url_for
import app
from . import cliente_blueprint
from datetime import datetime
@cliente_blueprint.route('/agendar', methods=['GET'])
def agendar_form():
    dias_restringidos = [d.fecha.strftime('%Y-%m-%d') for d in models.DiaRestringido.query.all()]
    return render_template('index.html', dias_restringidos=dias_restringidos)


@cliente_blueprint.route('/agendar_cita', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo_electronico = request.form['correo_electronico']
        telefono = request.form['telefono']
        fecha = request.form['fecha_cita']
        hora = request.form['hora_cita']

        # Convertir fecha (str) a tipo date
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d').date()

        # 🔒 Verificar si la fecha está restringida
        fecha_bloqueada = models.DiaRestringido.query.filter_by(fecha=fecha_dt).first()
        if fecha_bloqueada:
            return f"Error: no se pueden agendar citas el {fecha_dt}. Motivo: {fecha_bloqueada.motivo or 'día bloqueado por el administrador'}."

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

        # Verificar disponibilidad de hora
        consulta_hora = models.Cita.query.filter_by(fecha=fecha_dt, hora=hora).first()
        if consulta_hora:
            return 'La hora seleccionada ya está ocupada. Por favor, elige otra hora.'

        # Guardar nueva cita
        nueva_cita = models.Cita(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            correo_electronico=correo_electronico,
            fecha=fecha_dt,
            hora=hora
        )
        db.session.add(nueva_cita)
        db.session.commit()

        return '¡Cita agendada correctamente!'
    
    return render_template('index.html')
