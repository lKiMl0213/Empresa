from flask import Blueprint, request, jsonify, render_template
from flask_mysqldb import MySQL
from passlib.hash import scrypt
import datetime

rh_management_bp = Blueprint('rh_management', __name__)

mysql = MySQL()

def get_cursor():
    return mysql.connection.cursor()

def close_cursor(cursor):
    cursor.close()

@rh_management_bp.route('/', methods=['GET', 'POST'])
def manage_employee():
    if request.method == 'GET':
        action = request.args.get('action')
        if not action:
            return render_template('rh.html')
        if action == 'check_code':
            code = request.args.get('code')
            cursor = get_cursor()
            cursor.execute("SELECT * FROM employees WHERE code = %s", (code,))
            employee = cursor.fetchone()
            close_cursor(cursor)
            if employee:
                birth_date = employee[8]
                birth_month = str(birth_date.month).zfill(2)
                birth_year = str(birth_date.year)
                birth_day = str(birth_date.day).zfill(2)
                admission_date = employee[27]
                admission_month = str(admission_date.month).zfill(2)
                admission_year = str(admission_date.year)
                admission_day = str(admission_date.day).zfill(2)
                date_of_dismissal_date = employee[29]
                date_of_dismissal_month = str(date_of_dismissal_date.month).zfill(2)
                date_of_dismissal_year = str(date_of_dismissal_date.year)
                date_of_dismissal_day = str(date_of_dismissal_date.day).zfill(2)
                return jsonify({
                    'exists': True,
                    'photo': employee[1],
                    'code': employee[2],
                    'login': employee[3],
                    'name': employee[4],
                    'phone': employee[5],
                    'email': employee[6],
                    'cpf': employee[7],
                    'birth_day': birth_day,
                    'birth_month': birth_month,
                    'birth_year': birth_year,
                    'gender': employee[9],
                    'marital_status': employee[10],
                    'address': employee[11],
                    'cep': employee[12],
                    'academic_formation': employee[13],
                    'salary': employee[14],
                    'department': employee[15],
                    'position': employee[16],
                    'benefits1': employee[17],
                    'benefits2': employee[18],
                    'benefits3': employee[19],
                    'benefits4': employee[20],
                    'benefits5': employee[21],
                    'benefits6': employee[22],
                    'benefits7': employee[23],
                    'benefits8': employee[24],
                    'benefits9': employee[25],
                    'benefits10': employee[26],
                    'admission_day': admission_day,
                    'admission_month': admission_month,
                    'admission_year': admission_year,
                    'status': employee[27],
                    'inactive_status': employee[28],
                    'date_of_dismissal_day': date_of_dismissal_day,
                    'date_of_dismissal_month': date_of_dismissal_month,
                    'date_of_dismissal_year': date_of_dismissal_year
                })
            else:
                return jsonify({'exists': False})
        if action == 'list_employees':
            cursor = get_cursor()
            cursor.execute("SELECT * FROM employees order by name")
            employees = cursor.fetchall()
            close_cursor(cursor)
            return jsonify(employees=employees)
            employee_list = []
            for employee in employees:
                employee_list.append({
                    'photo': employee[1],
                    'code': employee[2],
                    'login': employee[3],
                    'name': employee[4],
                    'department': employee[15],
                    'position': employee[16],
                    'status': employee[27]
                })
            return jsonify(employees=employee_list)
    elif request.method == 'POST':
        action = request.args.get('action')
        if not action:
            return render_template('rh.html')
        if action == 'add_employee':
            data = request.form
            code = data.get('code')
            login = data.get('login')
            password = data.get('password')
            name = data.get('name')
            phone = data.get('phone')
            email = data.get('email')
            cpf = data.get('cpf')
            birth_day = data.get('birth_day').strip()
            birth_month = data.get('birth_month').strip()
            birth_year = data.get('birth_year').strip()
            birth_date = f"{birth_year}-{birth_month}-{birth_day}.zfill(2)"
            gender = data.get('gender')
            marital_status = data.get('marital_status')
            address = data.get('address')
            cep = data.get('cep')
            academic_formation = data.get('academic_formation')
            salary = data.get('salary')
            department = data.get('department')
            position = data.get('position')
            benefits1 = data.get('benefits1')
            benefits2 = data.get('benefits2')
            benefits3 = data.get('benefits3')
            benefits4 = data.get('benefits4')
            benefits5 = data.get('benefits5')
            benefits6 = data.get('benefits6')
            benefits7 = data.get('benefits7')
            benefits8 = data.get('benefits8')
            benefits9 = data.get('benefits9')
            benefits10 = data.get('benefits10')
            admission_day = data.get('admission_day').strip()
            admission_month = data.get('admission_month').strip()
            admission_year = data.get('admission_year').strip()
            admission_date = f"{admission_year}-{admission_month}-{admission_day}.zfill(2)"
            status = data.get('status')
            inactive_status = data.get('inactive_status')
            date_of_dismissal_day = data.get('date_of_dismissal_day').strip()
            date_of_dismissal_month = data.get('date_of_dismissal_month').strip()
            date_of_dismissal_year = data.get('date_of_dismissal_year').strip()
            date_of_dismissal_date = f"{date_of_dismissal_year}-{date_of_dismissal_month}-{date_of_dismissal_day}.zfill(2)"
            birth_date_obj = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
            admission_date_obj = datetime.datetime.strptime(admission_date, '%Y-%m-%d')
            date_of_dismissal_date_obj = datetime.datetime.strptime(date_of_dismissal_date, '%Y-%m-%d')

            if not all([code, login, password, name, cpf]):
                return jsonify(success=False, message="Todos os campos são obrigatórios.")
            
            cursor = get_cursor()
            cursor.execute("SELECT * FROM employees WHERE code = %s", (code,))
            employee = cursor.fetchone()
            close_cursor(cursor)
            if employee:
                cursor.execute("""
                    update employees
                    set code = %s,
                    login = %s,
                    password = %s,
                    name = %s,
                    phone = %s,
                    email = %s,
                    cpf = %s,
                    birth_date = %s,
                    gender = %s,
                    marital_status = %s,
                    address = %s,
                    cep = %s,
                    academic_formation = %s,
                    salary = %s,
                    department = %s,
                    position = %s,
                    benefits1 = %s,
                    benefits2 = %s,
                    benefits3 = %s,
                    benefits4 = %s,
                    benefits5 = %s,
                    benefits6 = %s,
                    benefits7 = %s,
                    benefits8 = %s,
                    benefits9 = %s,
                    benefits10 = %s,
                    admission_date = %s,
                    status = %s,
                    inactive_status = %s,
                    date_of_dismissal_date = %s
                """, (login, password, name, phone, email, cpf, birth_date_obj, gender, marital_status, address, cep, academic_formation, salary, department, position, benefits1, benefits2, benefits3, benefits4, benefits5, benefits6, benefits7, benefits8, benefits9, benefits10, admission_date_obj, status, inactive_status, date_of_dismissal_date_obj))
                mysql.connection.commit()
                close_cursor(cursor)
                return jsonify(success=True, message="Funcionário atualizado com sucesso.")
            else:
                cursor.execute("""
                    INSERT INTO employees (code, login, password, name, phone, email, cpf, birth_date, gender, marital_status, address, cep, academic_formation, salary, department, position, benefits1, benefits2, benefits3, benefits4, benefits5, benefits6, benefits7, benefits8, benefits9, benefits10, admission_date, status, inactive_status, date_of_dismissal_date)
                """, (code, login, password, name, phone, email, cpf, birth_date_obj, gender, marital_status, address, cep, academic_formation, salary, department, position, benefits1, benefits2, benefits3, benefits4, benefits5, benefits6, benefits7, benefits8, benefits9, benefits10, admission_date_obj, status, inactive_status, date_of_dismissal_date_obj))
                mysql.connection.commit()
                close_cursor(cursor)
                return jsonify(success=True, message="Funcionário cadastrado com sucesso.")
        
