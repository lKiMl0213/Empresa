from flask import Blueprint, request, jsonify, render_template
from flask_mysqldb import MySQL
from passlib.hash import scrypt
import datetime

user_management_bp = Blueprint('user_management', __name__)

mysql = MySQL()

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

@user_management_bp.route('/register', methods=['GET', 'POST'])
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

@user_management_bp.route('/recovery', methods=['GET', 'POST'])
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

@user_management_bp.route('/login', methods=['POST'])
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
