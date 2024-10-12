import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import datetime
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def initialize_users_db():
    default_data = []
    with open('users.json', 'w') as file:
        json.dump(default_data, file)

def load_users_db():
    try:
        with open('users.json', 'r') as file:
            content = file.read()
            data = json.loads(content)
            return data
    except Exception as e:
        initialize_users_db()
        return []

def save_users_db(users):
    with open('users.json', 'w') as file:
        json.dump(users, file)

def register_user(login, password, name, birthday, email, type):
    users_db = load_users_db()
    if any(user["login"] == login for user in users_db):
        return "Usuário já em uso"
    elif any(user["email"] == email for user in users_db):
        return "Email já em uso"
    else:
        users_db.append({
            "login": login,
            "password": password,
            "name": name,
            "birthday": birthday,
            "email": email,
            "type": type
        })
        save_users_db(users_db)
        return "Usuário registrado com sucesso!"
    
@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    if request.method == 'POST':
        login_or_email = request.form['login']
        users_db = load_users_db()
        user = next((user for user in users_db if user["login"] == login_or_email or user["email"] == login_or_email), None)

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
    users_db = load_users_db()
    user = next((user for user in users_db if user["login"] == login), None)

    if user and user["password"] == password:
        return user_type(user)
    else:
        return jsonify(success=False)

def user_type(user):
    if 'type' not in user:
        return jsonify(success=False, message="Tipo de usuário não encontrado.")
    return jsonify(success=True, user_type=user["type"])

@app.route('/rh', methods=['POST', 'GET'])
def rh():
    #return redirect(url_for('rh')) tenhoq ver como fazer isso
    return render_template('rh.html')

@app.route('/storage', methods=['POST', 'GET'])
def storage():
    #return redirect(url_for('storage')) tenhoq ver como fazer isso
    return render_template('storage.html')
@app.route('/market', methods=['POST', 'GET'])
def market():
    #return redirect(url_for('market')) tenhoq ver como fazer isso
    return render_template('market.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        name = request.form['name']
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']
        email = request.form['email']
        type = request.form['type']
        message = register_user(login, password, name, f"{day}/{month}/{year}", email, type)
        flash(message)
        return redirect(url_for('home'))
    return render_template('register.html', datetime=datetime)

if __name__ == "__main__":
    app.run(debug=True)
