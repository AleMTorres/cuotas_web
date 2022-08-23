from flask import Flask, render_template, request, redirect, url_for, flash
from coneccion import cursor

app = Flask(__name__)
app.secret_key = 'mysecretkey'

meses = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}


def get_paid():
    cursor.execute("SELECT * FROM Cuotas WHERE cant_cuotas-cuota +1 > 0")
    data = cursor.fetchall()
    for item in data:
        mes = item[4]+item[3]-1
        item[4] = meses[mes]
    return data


def get_products_paid():
    cursor.execute("SELECT * FROM Cuotas WHERE cant_cuotas-cuota +1 <= 0")
    paid = cursor.fetchall()
    for item in paid:
        if item[3] > item[5]:
            mes = item[4]+item[3]-2
            item[4] = meses[mes]
            return paid
        else:
            mes = item[4]+item[3]-1
            item[4] = meses[mes]
    return paid


@app.route('/')
def index():
    data = get_paid()
    paid = get_products_paid()
    return render_template('index.html', products=data, paid_out=paid)


@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        product = request.form['Producto']
        price = request.form['Monto']
        fee = request.form['Cuota']
        month = request.form['Mes']
        quantity = request.form['CantCuotas']
        cursor.execute(f"INSERT INTO Cuotas (producto, monto, cuota, mes, cant_cuotas) VALUES ('{product}', {price}, {fee}, '{month}', {quantity})")
        cursor.commit()
        flash('Producto agregado correctamente')
        return redirect(url_for('index'))


@app.route('/edit/<id>')
def get_product(id):
    cursor.execute(f"SELECT * FROM Cuotas WHERE id={id}")
    data = cursor.fetchall()
    return render_template('edit_product.html', product=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_product(id):
    if request.method == 'POST':
        product = request.form['Producto']
        price = request.form['Monto']
        fee = request.form['Cuota']
        month = request.form['Mes']
        quantity = request.form['CantCuotas']
        cursor.execute(f"UPDATE Cuotas SET producto='{product}', monto={price}, cuota={fee}, mes='{month}', cant_cuotas={quantity} WHERE id={id}")
        cursor.commit()
        flash('Producto editado correctamente')
        return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete_product(id):
    cursor.execute(f"DELETE FROM Cuotas where id={id}")
    cursor.commit()
    flash('Producto borrado')
    return redirect(url_for('index'))


@app.route('/pay/<string:id>')
def pay_product(id):
    cursor.execute(f"SELECT cant_cuotas-cuota +1 as cuota from cuotas where id={id}")
    item = cursor.fetchall()
    print(item)
    if item[0][0] > 0:
        cursor.execute(f"UPDATE Cuotas SET Cuota = Cuota+1 WHERE id={id}")
        cursor.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
