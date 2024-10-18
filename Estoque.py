from flask import Blueprint, render_template, request, jsonify, Flask, current_app
from flask_mysqldb import MySQL
from datetime import datetime
import os

estoque_bp = Blueprint('estoque', __name__)
mysql = MySQL()


def get_cursor():
    return mysql.connection.cursor()

def close_cursor(cursor):
    cursor.close()

@estoque_bp.route('/storage', methods=['GET'])
def check_barcode(barcode):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM products_db.product WHERE barcode = %s", (barcode,))
    product = cursor.fetchone()
    close_cursor(cursor)
    if product:
        return jsonify({
            'exists': True,
            'name': product[2],
            'buy_price': product[3],
            'sell_price': product[4],
            'stock': product[5],
            'expiration_date': product[6]
        })
        return product_exists(barcode)
    else:
        return jsonify({'exists': False})

@estoque_bp.route('/storage', methods=['GET', 'POST'])
def add_storage():
    if request.method == 'POST':
        barcode = request.form['barcode']
        name = request.form['name']
        buy_price = request.form['buy_price']
        sell_price = request.form['sell_price']
        stock = request.form['stock']
        month = request.form['month']
        year = request.form['year']
        expiration_date = f"{year}-{str(month).zfill(2)}-01"

        if not all([barcode, name, buy_price, sell_price, stock, expiration_date]):
            return jsonify({'error': 'Todos os campos são obrigatórios'})
        
        try:
            message = register_product(barcode, name, buy_price, sell_price, stock, expiration_date)
            return jsonify(success=message == "Produto registrado com sucesso!", message=message)
        except Exception as e:
            return jsonify(success=False, message=str(e))
        
@estoque_bp.route('/storage', methods=['GET', 'POST'])
def remove_storage(product_exists):
    product = product_exists(barcode)
    if product:
        try:
            cursor = get_cursor()
            cursor.execute("DELETE FROM products_db.product WHERE barcode = %s", (product[1],))
            mysql.connection.commit()
            close_cursor(cursor)
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, message=str(e))
    return jsonify(success=False, message="Produto não encontrado")

@estoque_bp.route('/storage', methods=['GET'])
def low_stock():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM products_db.product WHERE stock < 10")
    product = cursor.fetchall()
    close_cursor(cursor)

    low_stock_product = []
    for product in product:
        low_stock_product.append({
            'barcode': product[1],
            'name': product[2],
            'stock': product[5]
        })
    return jsonify(success=True, product=low_stock_product)

@estoque_bp.route('/storage', methods=['GET'])
def expiration_date_verify():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM products_db.product WHERE expiration_date < CURDATE() + INTERVAL 2 MONTH")
    product = cursor.fetchall()
    close_cursor(cursor)

    closed_to_expire = []
    for product in product:
        closed_to_expire.append({
            'barcode': product[1],
            'name': product[2],
            'expiration_date': product[6]
        })
    return jsonify(success=True, product=closed_to_expire)
        
if __name__ == '__main__':
    app.run(debug=True)
