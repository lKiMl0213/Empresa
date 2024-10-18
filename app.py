from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
from user_management import user_management_bp
from estoque import estoque_bp
from dotenv import load_dotenv
from passlib.hash import scrypt
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

app.register_blueprint(user_management_bp, url_prefix='/user_management')
app.register_blueprint(estoque_bp, url_prefix='/estoque')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
                return jsonify(success=False, message="Senha inválidos.")
        else:
            return jsonify(success=False, message="Usuário não encontrado.")

    return render_template('home.html')

def user_type(user, login):
    if len(user) < 8:
        return jsonify(success=False, message="Tipo de usuário não encontrado.")
    return jsonify(success=True, user_type=user[7], login=login)

if __name__ == "__main__":
    app.run(debug=True)
