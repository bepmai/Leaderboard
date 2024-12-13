from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask import jsonify,make_response
import sqlite3
from datetime import datetime,timedelta
# Kết nối đến cơ sở dữ liệu SQLite
def get_db_connection():
    connection = sqlite3.connect('./database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Đăng nhập
def login(request):
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        url = 'https://sinhvien1.tlu.edu.vn/education/oauth/token'
        role = "normal"
        state = "online"

        if username == "2151160519" or username == "2151163724":
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
            connection.close()
            resp = make_response(jsonify({"message": "Login successful!",
                "data": token_data,
                "username": username,
                "role": role}))
            expires = datetime.utcnow() + timedelta(seconds=token_data.get("expires_in"))
            resp.set_cookie('token', access_token, httponly=False,samesite='None',secure=True,path='/',domain=".localhost")
            resp.set_cookie('msv', username, httponly=False,samesite = 'None',secure=True,path='/',domain=".localhost")
            return resp

        except requests.RequestException:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user["password"], password):
                query = "UPDATE users SET state = ? WHERE username = ?"
                cursor.execute(query, ("online", username))
                connection.commit()
                resp = make_response(jsonify({"message": "Offline login successful!",
                    "username": username,
                    "role": user["role"]}))
                expires = datetime.utcnow() + timedelta(seconds=86400)
                resp.set_cookie('token', username, httponly=False,samesite='None',secure=True,path='/',domain=".localhost")
                resp.set_cookie('msv', username, httponly=False,samesite='None',secure=True,path='/',domain=".localhost")
                return resp
            else:
                return jsonify({"message": "Invalid credentials!"}), 400

    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500

# Đăng xuất
def logout(request):
    try:
        data = request.json
        username = data.get('username')

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "UPDATE users SET state = ? WHERE username = ?"
        cursor.execute(query, ("offline", username))
        connection.commit()
        resp = make_response(jsonify({"message": "Logout successful!"}))
        resp.set_cookie('token', "", httponly=False,expires=0,samesite='None',secure=True,path='/',domain=".localhost")
        resp.set_cookie('msv', '', httponly=False,expires=0,samesite='None',secure=True,path='/',domain=".localhost")
        return resp

    except sqlite3.Error as e:
        return jsonify({"message": f"Error during logout: {e}"}), 500

        
def checkRole(request):
    try:
        data = request.json
        username = data.get('username')
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "select role from users WHERE username = ?"
        cursor.execute(query, (username,))
        role = cursor.fetchone()
        connection.commit()
        resp = make_response(jsonify({"message": "Login successful!","data":role[0]}))
        resp.set_cookie('role',role[0], httponly=False,samesite='None',secure=True,path='/',domain=".localhost")
        return resp

    except sqlite3.Error as e:
        return jsonify({"message": f"Error during logout: {e}"}), 500


