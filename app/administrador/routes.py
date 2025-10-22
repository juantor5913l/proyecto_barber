from datetime import datetime
from flask import render_template, request, redirect, session, url_for, flash
import app
from . import admin_blueprint



@admin_blueprint.route('/listar_cortes', methods=['GET', 'POST'])
def listar_cortes():
    from app import db, models  # Importación local para evitar circularidad
    lista_cortes = db.session.query(models.Cita).all()
    return render_template('administrador/listar_cortes.html', lista_cortes=lista_cortes)

@admin_blueprint.route('/dias_restringidos/fecha', methods=['GET', 'POST'])
def seleccionar_fecha():
    if request.method == 'POST':
        fecha_str = request.form['fecha']
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        # Guardamos temporalmente la fecha en sesión
        session['fecha_seleccionada'] = fecha_str
        return redirect(url_for('administrador.seleccionar_hora'))


    return render_template('administrador/seleccionar_fecha.html')

@admin_blueprint.route('/dias_restringidos/hora', methods=['GET', 'POST'])

def seleccionar_hora():
    

    fecha_str = session.get('fecha_seleccionada')
    if not fecha_str:
        flash("Primero selecciona una fecha.")
        return ("selecciona hora gay")

    if request.method == 'POST':
        hora_str = request.form['hora']


        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora_dt = datetime.strptime(hora_str, '%H:%M').time()

        dia_restringido = app.models.DiaRestringido(fecha=fecha_dt)
        dia_restringido.hora = hora_dt  # si el modelo tiene el campo
        app.db.session.add(dia_restringido)
        app.db.session.commit()

        todas_las_horas = [
        '08:00', '09:00', '10:00', '11:00',
        '13:00', '14:00', '15:00', '16:00', '17:00'
    ]
        horas_string_cruda = str(todas_las_horas)

        session.pop('fecha_seleccionada', None)
        flash('Día restringido guardado correctamente.')
        print("Día restringido guardado:", fecha_str, hora_str)
        return ("dia restringido guardado")


    return render_template('administrador/seleccionar_hora.html', fecha=fecha_str)