from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
from user_management import user_management_bp
from estoque import estoque_bp
from rh_management import rh_management_bp
from dotenv import load_dotenv
from passlib.hash import scrypt
import os
from time import time
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

app.register_blueprint(user_management_bp, url_prefix='/user_management')
app.register_blueprint(estoque_bp, url_prefix='/storage')
app.register_blueprint(rh_management_bp, url_prefix='/rh')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/market')
def market():
    return render_template('market.html', time=int(time()))

if __name__ == "__main__":
    app.run(debug=True)
