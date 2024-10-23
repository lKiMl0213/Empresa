from flask import Blueprint, request, jsonify, render_template
from flask_mysqldb import MySQL
from passlib.hash import scrypt
import datetime

rh_management_bp = Blueprint('rh_management', __name__)

mysql = MySQL()

@rh_management_bp.route('/', methods=['GET', 'POST'])
def manage_employee():
    return render_template('rh.html')
