from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
import app
from datetime import datetime
from . import cliente_blueprint


# --- Paso 1: calendario (selección de día) ---
@cliente_blueprint.route('/calendario')
def calendario_view():
    return render_template('cliente/calendario.html')


@cliente_blueprint.route('/dias_restringidos')
def dias_restringidos():
    dias = app.models.DiaRestringido.query.all()
    fechas = [d.fecha.strftime('%Y-%m-%d') for d in dias]
    return jsonify(fechas)


@cliente_blueprint.route('/seleccionar_fecha', methods=['POST'])
def seleccionar_fecha():
    fecha = request.form.get('fecha')
    if not fecha:
        flash('Debe seleccionar una fecha válida.')
        return redirect(url_for('cliente.calendario_view'))
    session['fecha_cita'] = fecha
    return redirect(url_for('cliente.seleccionar_hora'))


# --- Paso 2: selección de hora ---
@cliente_blueprint.route('/horas', methods=['GET', 'POST'])
def seleccionar_hora():
    if request.method == 'POST':
        hora = request.form.get('hora')
        if not hora:
            flash('Debe seleccionar una hora.')
            return redirect(url_for('cliente.seleccionar_hora'))
        session['hora_cita'] = hora
        return redirect(url_for('cliente.datos_cita'))
    
    fecha = session.get('fecha_cita')
    if not fecha:
        return redirect(url_for('cliente.calendario_view'))
    
    # --- Obtener horas ocupadas ---
    citas_existentes = app.models.Cita.query.filter_by(fecha=fecha).all()
    horas_ocupadas = [c.hora.strftime('%H:%M') for c in citas_existentes]

    # --- Definir todas las horas disponibles ---
    todas_las_horas = [
        '08:00', '09:00', '10:00', '11:00',
        '13:00', '14:00', '15:00', '16:00', '17:00'
    ]

    # --- Filtrar horas libres ---
    horas_disponibles = [h for h in todas_las_horas if h not in horas_ocupadas]

    return render_template('cliente/horas.html', fecha=fecha, horas_disponibles=horas_disponibles)


# --- Paso 3: formulario de datos personales ---
@cliente_blueprint.route('/datos', methods=['GET', 'POST'])
def datos_cita():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo_electronico = request.form['correo_electronico']
        telefono = request.form['telefono']
        fecha = session.get('fecha_cita')
        hora = session.get('hora_cita')

        # Validaciones
        if not telefono.isdigit() or len(telefono) != 10:
            return "Error: el teléfono debe tener 10 dígitos."
        elif '@' not in correo_electronico or '.' not in correo_electronico:
            return "Error: el correo electrónico no es válido."

        # --- Validar que no exista cita en ese día/hora ---
        cita_existente = app.models.Cita.query.filter_by(fecha=fecha, hora=hora).first()
        if cita_existente:
            return "Error: Ya existe una cita agendada para ese día y hora. Por favor selecciona otra."

        # Guardar nueva cita
        nueva_cita = app.models.Cita(
            nombre=nombre,
            apellido=apellido,
            correo_electronico=correo_electronico,
            telefono=telefono,
            fecha=fecha,
            hora=hora
        )
        app.db.session.add(nueva_cita)
        app.db.session.commit()

        # Limpiar sesión
        session.pop('fecha_cita', None)
        session.pop('hora_cita', None)

        return render_template('cliente/confirmacion.html', nombre=nombre, fecha=fecha, hora=hora)

    return render_template('cliente/datos.html')
