from flask import Blueprint, render_template, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime, timedelta

estoque_bp = Blueprint('estoque', __name__)

mysql = MySQL()

def register_product(barcode, name, buy_price, sell_price, stock, expiration_date):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products WHERE barcode = %s OR name = %s", (barcode, name))
    existing_product = cursor.fetchone()
    cursor.close()

    if existing_product:
        if existing_product[1] == barcode:
            return "Código de barras já em uso!"
        elif existing_product[2] == name:
            return "Nome do produto já em uso!"
    
    cursor.execute("INSERT INTO products(barcode, name, buy_price, sell_price, stock, expiration_date) VALUES (%s, %s, %s, %s, %s, %s)", 
                   (barcode, name, buy_price, sell_price, stock, expiration_date))
    mysql.connection.commit()
    cursor.close()
    return "Produto cadastrado com sucesso"
    
def add_storage():
    if request.method == 'POST':
        barcode = request.form.get('barcode')
        name = request.form.get('name')
        buy_price = request.form.get('buy_price')
        sell_price = request.form.get('sell_price')
        stock = request.form.get('stock')
        month = request.form.get('month')
        year = request.form.get('year')
    
        expiration_date = f"{year}-{str(month).zfill(2)}"

        if not all([barcode, name, buy_price, sell_price, stock, expiration_date]):
            return jsonify(success=False, message="Todos os campos são obrigatórios.")
    
        try:
            message = register_product(barcode, name, buy_price, sell_price, stock, expiration_date)
            if message == "Produto cadastrado com sucesso":
                return jsonify(success=True)
            else:
                return jsonify(success=False, message=message)
        except Exception as e:
            return jsonify(success=False, message=f"Ocorreu um erro: {str(e)}")
    return render_template('storage.html', datetime=datetime)


def remove_storage():
    barcode_or_name = request.form.get('productId')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM storage WHERE barcode = %s OR name = %s", (barcode_or_name, barcode_or_name))
    product = cursor.fetchone()
    cursor.close()

    if product:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM storage WHERE barcode = %s OR name = %s", (barcode_or_name, barcode_or_name))
            mysql.connection.commit()
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, error=str(e))
        finally:
            cursor.close()
    

def low_stock():
    try: 
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM storage")
        products = cursor.fetchall()
        low_stock_products = []
        for product in products:
            if product[5] < 5:
                low_stock_products.append((product[2], product[4]))
        if low_stock_products:
            return jsonify(success=True, message="Os produtos com estoque baixo são: " + low_stock_products)
        else:
            return jsonify(success=False, message="Não há produtos com estoque baixo.")
    except Exception as e:
        return jsonify(success=False, message=f"Ocorreu um erro: {str(e)}")
    finally:
        cursor.close()
    
def expiration_date_verify():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM storage")
        products = cursor.fetchall()
        closed_to_expire = []

        for product in products:
            expiration_date = product[6]
            if expiration_date:
                try:
                    expiration_date = datetime.strptime(expiration_date, "%Y-%m")
                    if expiration_date <= datetime.now() + timedelta(days=30):
                        closed_to_expire.append(product[2])
                except ValueError:
                    print(f"Erro ao analisar a data de validade do produto: {product[2]}")

        if closed_to_expire:
            return jsonify(success=True, message="Os produtos próximos de vencer são: " + closed_to_expire)
    except Exception as e:
        return jsonify(success=False, message=f"Ocorreu um erro: {str(e)}")
    finally:
        cursor.close()

def update_product(barcode, name, buy_price, sell_price, stock, expiration_date):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM storage WHERE barcode = %s OR name = %s", (barcode, name))
    existing_product = cursor.fetchone()

    if existing_product:
        if existing_product[1] == barcode or existing_product[2] == name:
            try: 
                cursor.execute("""
                    update storage
                    set barcode = %s, name = %s, buy_price = %s, sell_price = %s, stock = %s, expiration_date = %s
                    where id = %s
                    """, (barcode, name, buy_price, sell_price, stock, expiration_date, existing_product[0]))
                mysql.connection.commit()
                return "Produto atualizado com sucesso"
            except Exception as e:
                return f"Ocorreu um erro: {str(e)}"
        else:
            return "Produto não encontrado"
    else:
        return "Produto não encontrado"
    cursor.close()

def update_storage():
    if request.method == 'POST':
        barcode_or_name = request.form.get('productId')
        if not barcode_or_name:
            return jsonify(success=False, message="Nenhum produto selecionado.")
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM storage WHERE barcode = %s OR name = %s", (barcode_or_name, barcode_or_name))
            product = cursor.fetchone()
            cursor.close()
            
            if not product:
                return jsonify(success=False, message="Produto não encontrado.")
            
            if request.form.get('fetch_data'):
                product_data = {
                    'barcode': product[1],
                    'name': product[2],
                    'buy_price': product[3],
                    'sell_price': product[4],
                    'stock': product[5],
                    'expiration_date': product[6]
                }
                return jsonify(success=True, product=product_data)
            
            barcode = request.form.get('barcode')
            name = request.form.get('name')
            buy_price = request.form.get('buy_price')
            sell_price = request.form.get('sell_price')
            stock = request.form.get('stock')
            month = request.form.get('month')
            year = request.form.get('year')
            expiration_date = f"{year}-{str(month).zfill(2)}" if year and month else None

            if not all([barcode, name, buy_price, sell_price, stock, expiration_date]):
                return jsonify(success=False, message="Todos os campos são obrigatórios.")
            
            try:
                message = update_product(barcode, name, buy_price, sell_price, stock, expiration_date)
                if message == "Produto atualizado com sucesso":
                    return jsonify(success=True)
                else:
                    return jsonify(success=False, message=message)
            except Exception as e:
                return jsonify(success=False, message=f"Ocorreu um erro: {str(e)}")
        except Exception as e:
            return jsonify(success=False, message=f"Ocorreu um erro ao buscar o produto: {str(e)}")
    
    return render_template('storage.html', datetime=datetime)


@estoque_bp.route('/storage', methods=['GET', 'POST'])
def storage():
    return render_template('storage.html')

if __name__ == "__main__":
    app.run(debug=True)
