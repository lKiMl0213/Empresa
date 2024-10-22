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

@estoque_bp.route('/', methods=['GET', 'POST'])
def manage_product():
    if request.method == 'GET':
        action = request.args.get('action')
        if not action:
            return render_template('storage.html')
        if action == 'check_barcode':
            barcode = request.args.get('barcode')
            cursor = get_cursor()
            cursor.execute("SELECT * FROM products WHERE barcode = %s", (barcode,))
            product = cursor.fetchone()
            close_cursor(cursor)
            if product:
                expiration_date_str = product[6]
                month = str(expiration_date_str.month).zfill(2)
                year = str(expiration_date_str.year)
                return jsonify({
                    'exists': True,
                    'name': product[2],
                    'buy_price': product[3],
                    'sell_price': product[4],
                    'stock': product[5],
                    'month': month,
                    'year': year
                })
            else:
                return jsonify({'exists': False})
        if action == 'low_stock':
            cursor = get_cursor()
            cursor.execute("SELECT * FROM products WHERE stock < 10")
            products = cursor.fetchall()
            close_cursor(cursor)
            low_stock_products = []
            for product in products:
                low_stock_products.append({
                    'barcode': product[1],
                    'name': product[2],
                    'stock': product[5]
                    })
            return jsonify(success=True, products=low_stock_products)
        if action == 'expiration_date_verify':
            cursor = get_cursor()
            cursor.execute("SELECT * FROM products WHERE expiration_date < CURDATE() + INTERVAL 2 MONTH")
            products = cursor.fetchall()
            close_cursor(cursor)
            closed_to_expire = []
            for product in products:
                closed_to_expire.append({
                    'barcode': product[1],
                    'name': product[2],
                    'expiration_date': product[6]
                })
            return jsonify(success=True, products=closed_to_expire)
        if action == 'list_products':
            cursor = get_cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            close_cursor(cursor)

            product_list = []
            for product in products:
                product_list.append({
                    'barcode': product[1],
                    'name': product[2],
                    'buy_price': product[3],
                    'sell_price': product[4],
                    'stock': product[5],
                    'expiration_date': product[6].strftime('%m/%Y')
                })
            return jsonify(success=True, products=product_list)
    elif request.method == 'POST':
        action = request.args.get('action')
        if not action:
            return render_template('storage.html')
        if action == 'add_product':
            data = request.form
            barcode = data.get('barcode')
            name = data.get('name')
            buy_price = data.get('buy_price')
            sell_price = data.get('sell_price')
            stock = data.get('stock')
            month = data.get('month').strip()
            year = data.get('year').strip()
            expiration_date = f"{year}-{str(month).zfill(2)}-01"

            expiration_date_obj = datetime.strptime(expiration_date, '%Y-%m-%d')

            if not all([barcode, name, buy_price, sell_price, stock, month, year]):
                return jsonify(success=False, message="Todos os campos são obrigatórios.")
        
            cursor = get_cursor()
            cursor.execute("SELECT * FROM products WHERE barcode = %s", (barcode,))
            product = cursor.fetchone()

            if product:
                cursor.execute("""
                    update products
                    set name = %s,
                    buy_price = %s,
                    sell_price = %s,
                    stock = %s,
                    expiration_date = %s
                    where barcode = %s
                """, (name, buy_price, sell_price, stock, expiration_date_obj, barcode))
                mysql.connection.commit()
                close_cursor(cursor)
                return jsonify(success=True, message="Produto atualizado com sucesso.")
            else:
                cursor.execute("""
                    INSERT INTO products (barcode, name, buy_price, sell_price, stock, expiration_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (barcode, name, buy_price, sell_price, stock, expiration_date_obj))
                mysql.connection.commit()
                close_cursor(cursor)
                return jsonify(success=True, message="Produto cadastrado com sucesso.")
        
        if action == 'remove_product':
            data = request.form
            barcode = data.get('barcode')

            if not barcode:
                return jsonify(success=False, message="Código de barras é obrigatório.")
            
            cursor = get_cursor()
            cursor.execute("SELECT * FROM products WHERE barcode = %s", (barcode,))
            product = cursor.fetchone()

            if product:
                cursor.execute("DELETE FROM products WHERE barcode = %s", (barcode,))
                mysql.connection.commit()
                close_cursor(cursor)
                return jsonify(success=True, message="Produto removido com sucesso.")
            else:
                close_cursor(cursor)
                return jsonify(success=False, message="Produto não encontrado.")

                    
