from flask import redirect, render_template, request, flash, url_for
import app
from . import gasto_blueprint

@gasto_blueprint.route('/agregarg', methods=['GET', 'POST'])
def agregar_gasto():
    if request.method == 'POST':
        cantidad_gastada = request.form['cantidad_gastada']
        metodo_pago_id = request.form['metodo_pago']
        categoria_id = request.form['categoria']
        descripcion_detallada = request.form['descripcion_detallada']

        gasto = app.models.Gasto(
            cantidad_gastada=cantidad_gastada,
            metodo_pago_id=metodo_pago_id,
            categoria_id=categoria_id,
            descripcion_detallada=descripcion_detallada
        )
        app.db.session.add(gasto)
        app.db.session.commit()

        flash("Gasto registrado correctamente ✅", "success")
        return redirect(url_for('gasto_blueprint.agregar_gasto'))

    # GET → igual, pasamos ambos
    metodos = app.models.MetodoPago.query.all()
    categorias = app.models.Categoria.query.all()
    return render_template('index.html', metodos=metodos, categorias=categorias)