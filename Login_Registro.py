import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import datetime
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Fortrek.1'
app.config['MYSQL_DB'] = 'users_db'

mysql = MySQL(app)

def register_user(login, password, name, birthday, cpf, email, user_type):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE login = %s OR email = %s", (login, email))
    existing_user = cursor.fetchone()

    if existing_user:
        if existing_user[1] == login:
            return "Login já em uso"
        elif existing_user[2] == email:
            return "Email já em uso"
    
    cursor.execute("INSERT INTO users(login, password, name, birthday, cpf, email, type) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                   (login, password, name, birthday, cpf, email, user_type))
    mysql.connection.commit()
    cursor.close()
    return "Usuário registrado com sucesso"

@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    if request.method == 'POST':
        login_or_email = request.form['login']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE login = %s OR email = %s", (login_or_email, login_or_email))
        user = cursor.fetchone()
        cursor.close()
        if user:
            # coloca aqui a lógica para enviar o email se quiser se n fdc kkkkk
            return jsonify(success=True)
        else:
            return jsonify(success=False)
    return render_template('recovery.html')

@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE login = %s AND password = %s", (login, password))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return user_type(user, login)
    else:
        return jsonify(success=False)

def user_type(user, login):
    if len(user) < 8:
        return jsonify(success=False, message="Tipo de usuário não encontrado.")
    return jsonify(success=True, user_type=user[7], login=login)

@app.route('/rh', methods=['POST', 'GET'])
def rh():
    return render_template('rh.html')

@app.route('/market', methods=['POST', 'GET'])
def market():
    return render_template('market.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/storage', methods=['POST', 'GET'])
def storage():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    users_db = cursor.fetchall()
    cursor.close()
    
    for user in users_db:
        if user[7] == "storage":
            user_name = user[3]
        else:
            user_name = "Nome não encontrado"    

    return render_template('storage.html', user=user_name)

@app.route('/products', methods=['GET', 'POST'])
def products():
    return render_template('products.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        name = request.form['name']
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']
        cpf = request.form['cpf']
        email = request.form['email']
        type = request.form['type']
        message = register_user(login, password, name, f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}", email, cpf, type)
        flash(message)
        return redirect(url_for('home'))
    return render_template('register.html', datetime=datetime)

if __name__ == "__main__":
    app.run(debug=True)
