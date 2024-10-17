from flask import Flask, render_template
from flask_mysqldb import MySQL
from user_management import user_management_bp
from estoque import estoque_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Fortrek.1'
app.config['MYSQL_DB'] = 'users_db'

mysql = MySQL(app)


app.register_blueprint(user_management_bp, url_prefix='/user_management')
app.register_blueprint(estoque_bp, url_prefix='/estoque')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    return render_template('recovery.html')

@app.route('/rh', methods=['GET', 'POST'])
def rh():
    return render_template('rh.html')

@app.route('/storage', methods=['GET', 'POST'])
def storage():
    return render_template('storage.html')

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template('market.html')

if __name__ == "__main__":
    app.run(debug=True)
