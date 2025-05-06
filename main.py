from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

# Configuración de la base de datos
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',  # Cambia esto por tu usuario de la base de datos
        password='123456',  # Cambia esto por tu contraseña
        database='DB_Proyecto_1',
        cursorclass=pymysql.cursors.DictCursor
    )

app = Flask(__name__)
CORS(app)

@app.route('/testConnection', methods=['GET'])
def test_connection():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
        return jsonify({"version": version}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Endpoint: POST /register
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    print(data)
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO Usuarios (name, lastname, username, email, phone, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data['name'], data['lastname'], data['username'],
                data['email'], data['phone'], data['password']
            ))
            connection.commit()
        return jsonify({"message": "usuario registrado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Endpoint: POST /login
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT id FROM Usuarios WHERE username = %s AND password = %s
            """
            cursor.execute(sql, (data['username'], data['password']))
            user = cursor.fetchone()
            if user:
                return jsonify({"message": "Login exitoso", "id_user": user['id']}), 200
            else:
                return jsonify({"error": "Credenciales incorrectas"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Endpoint: GET /currentBudget/<user_id>
@app.route('/currentBudget/<int:user_id>', methods=['GET'])
def current_budget(user_id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT type, date, description, amount
                FROM Gastos
                WHERE user_id = %s AND MONTH(date) = MONTH(CURRENT_DATE()) AND YEAR(date) = YEAR(CURRENT_DATE())
            """
            cursor.execute(sql, (user_id,))
            expenses = cursor.fetchall()
        return jsonify(expenses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Endpoint: GET /billsList/<user_id>
@app.route('/billsList/<int:user_id>', methods=['GET'])
def bills_list(user_id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT id, type, date, description, amount, bill_url AS url
                FROM Gastos
                WHERE user_id = %s AND bill_url IS NOT NULL
            """
            cursor.execute(sql, (user_id,))
            bills = cursor.fetchall()
            print(bills)
        return jsonify(bills), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


# Endpoint: GET /pastExpenses/<user_id>
@app.route('/pastExpenses/<int:user_id>', methods=['GET'])
def past_expenses(user_id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT type, date, description, amount
                FROM Gastos
                WHERE user_id = %s
            """
            cursor.execute(sql, (user_id,))
            expenses = cursor.fetchall()
        return jsonify(expenses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Endpoint: POST /addExpense/<user_id>
@app.route('/addExpense/<int:user_id>', methods=['POST'])
def add_expense(user_id):
    data = request.json
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO Gastos (user_id, type, description, amount, date)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                user_id, data['type'], data['description'],
                data['amount'], data['date']
            ))
            connection.commit()
        return jsonify({"message": "gasto agregado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Endpoint: POST /addBill/<user_id>
@app.route('/addBill/<int:user_id>', methods=['POST'])
def add_bill(user_id):
    data = request.json
    print(data)
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO Gastos (user_id, type, description, amount, date, bill_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                user_id, data['type'], data['description'],
                data['amount'], data['date'], data['url']
            ))
            connection.commit()
        return jsonify({"message": "gasto agregado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Endpoint: GET /reports/expenses/<user_id>
@app.route('/reports/expenses/<int:user_id>', methods=['GET'])
def expenses_report(user_id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT 
                    DATE_FORMAT(`date`, '%%Y-%%m') AS value,
                    DATE_FORMAT(MIN(`date`), '%%M %%Y') AS label,
                    SUM(amount) AS total
                FROM Gastos
                WHERE user_id = %s
                GROUP BY DATE_FORMAT(`date`, '%%Y-%%m')
                ORDER BY DATE_FORMAT(`date`, '%%Y-%%m')
            """
            cursor.execute(sql, (user_id,))
            report = cursor.fetchall()
        return jsonify(report), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Endpoint: GET /reports/expensesByType/<user_id>
@app.route('/reports/expensesByType/<int:user_id>', methods=['GET'])
def expenses_by_type_report(user_id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT type, SUM(amount) AS total
                FROM Gastos
                WHERE user_id = %s
                GROUP BY type
            """
            cursor.execute(sql, (user_id,))
            report = cursor.fetchall()
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)