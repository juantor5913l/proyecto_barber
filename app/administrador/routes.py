from flask import render_template, request, redirect, url_for, flash
import app
from . import admin_blueprint



@admin_blueprint.route('/listar_cortes', methods=['GET', 'POST'])
def listar_cortes():
    from app import db, models  # Importación local para evitar circularidad
    lista_cortes = db.session.query(models.Cita).all()
    return render_template('listar_cortes.html', lista_cortes=lista_cortes)

@admin_blueprint.route('/dias_restringidos', methods=['GET', 'POST'])
def gestionar_dias_restringidos():
    from app import db, models
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        motivo = request.form.get('motivo')

        if not fecha:
            flash("Debes seleccionar una fecha.", "danger")
            return redirect(url_for('administrador.gestionar_dias_restringidos'))

        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d').date()

        # Verificar si ya existe
        existente = DiaRestringido.query.filter_by(fecha=fecha_dt).first()
        if existente:
            flash("Esa fecha ya está restringida.", "warning")
        else:
            nuevo_dia = DiaRestringido(fecha=fecha_dt, motivo=motivo)
            db.session.add(nuevo_dia)
            db.session.commit()
            flash("Día restringido agregado correctamente.", "success")

        return redirect(url_for('administrador.gestionar_dias_restringidos'))

    dias = app.db.session.query(models.DiaRestringido.fecha.asc()).all()
    return render_template('admin/dias_restringidos.html', dias=dias)


# ------------------------------------------------
# ❌ Eliminar día restringido
# ------------------------------------------------
@admin_blueprint.route('/dias_restringidos/eliminar/<int:id>', methods=['POST'])
def eliminar_dia_restringido(id):
    dia = DiaRestringido.query.get_or_404(id)
    db.session.delete(dia)
    db.session.commit()
    flash("Día restringido eliminado correctamente.", "success")
    return redirect(url_for('administrador.gestionar_dias_restringidos'))