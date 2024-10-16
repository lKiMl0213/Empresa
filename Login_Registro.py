import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import datetime
from flask_mysqldb import MySQL
from passlib.hash import scrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Fortrek.1'
app.config['MYSQL_DB'] = 'users_db'

mysql = MySQL(app)

def register_user(login, hashed_password, name, birthday, cpf, email, user_type):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE login = %s OR email = %s", (login, email))
    existing_user = cursor.fetchone()

    if existing_user:
        if existing_user[1] == login:
            return "Login já em uso"
        elif existing_user[6] == email:
            return "Email já em uso"
    
    cursor.execute("INSERT INTO users(login, password, name, birthday, cpf, email, type) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                   (login, hashed_password, name, birthday, cpf, email, user_type))
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
            # se quiser q envie email faz aq, se n quiser fdc
            return jsonify(success=True)
        else:
            return jsonify(success=False)
    return render_template('recovery.html')

@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE login = %s", (login,))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        stored_hash = user[2]
        if scrypt.verify(password, stored_hash):
            return user_type(user, login)
        else:
            print("Senha incorreta.")
    else:
        print("Usuário não encontrado.")
    
    return jsonify(success=False, message="Login ou senha inválidos.")

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
    
    user_name = "Nome não encontrado"
    for user in users_db:
        if user[7] == "storage":
            user_name = user[3]
            break

    return render_template('storage.html', user=user_name)

@app.route('/products', methods=['GET', 'POST'])
def products():
    return render_template('products.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        user_type = request.form.get('type')

        
        hashed_password = scrypt.hash(password)
                
        if not all([login, password, name, day, month, year, cpf, email, user_type]):
            return jsonify(success=False, message="Todos os campos são obrigatórios.")
        
        birthday = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"

        try:
            message = register_user(login, hashed_password, name, birthday, cpf, email, user_type)
            if message == "Usuário registrado com sucesso":
                return jsonify(success=True)
            else:
                return jsonify(success=False, message=message)
        except Exception as e:
            return jsonify(success=False, message=f"Ocorreu um erro: {str(e)}")

    return render_template('register.html', datetime=datetime)

if __name__ == "__main__":
    app.run(debug=True)
