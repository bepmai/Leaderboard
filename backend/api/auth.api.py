from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import ssl

app = Flask(__name__)

# ssl_context = ssl.create_default_context()

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Đăng nhập
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        url = 'https://sinhvien1.tlu.edu.vn/education/oauth/token'
        role = "normal"
        state = "online"

        if username == "2151160519":
            role = "admin"

        payload = {
            "client_id": "education_client",
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_secret": "password"
        }

        hashed_password = generate_password_hash(password)
        
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            response = requests.post(url, json=payload, timeout=10, verify=False)
            response.raise_for_status()
            token_data = response.json()

            access_token = token_data.get("access_token")
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                query = "UPDATE users SET access_token = ?, state = ? WHERE username = ?"
                cursor.execute(query, (access_token, state, username))
            else:
                query = "INSERT INTO users (username, password, access_token, role, state) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(query, (username, hashed_password, access_token, role, state))

            connection.commit()

            return jsonify({
                "message": "Login successful, data saved!",
                "data": token_data,
                "username": username,
                "role": role
            }), 200

        except requests.RequestException:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user["password"], password):
                query = "UPDATE users SET state = ? WHERE username = ?"
                cursor.execute(query, ("online", username))
                connection.commit()

                return jsonify({
                    "message": "Offline login successful!",
                    "username": username,
                    "role": user["role"]
                }), 200
            else:
                return jsonify({"message": "Invalid credentials!"}), 400

    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    finally:
        connection.close()

@app.route('/logout', methods=['POST'])
def logout():
    try:
        data = request.json
        username = data.get('username')

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "UPDATE users SET state = ? WHERE username = ?"
        cursor.execute(query, ("offline", username))
        connection.commit()

        return jsonify({"message": "Logged out successfully!"}), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"Error during logout: {e}"}), 500
    finally:
        connection.close()

@app.route('/getGPA', methods=['GET'])
def getGPA():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Authorization token is required"}), 400

        url = "https://sinhvien1.tlu.edu.vn/education/api/studentsummarymark/getbystudent"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        data = response.json()

        return jsonify({
            "message": "GPA fetched successfully!",
            "gpa": data.get("mark4")
        }), 200

    except requests.RequestException as e:
        return jsonify({"message": f"Error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
