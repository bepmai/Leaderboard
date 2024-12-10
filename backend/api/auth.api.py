from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os



import ssl
ssl_context = ssl.create_default_context()

# Controller Functions
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

        # Tạo payload gửi tới API
        payload = {
            "client_id": "education_client",
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_secret": "password"
        }

        hashed_password = generate_password_hash(password)
        
        # Kết nối cơ sở dữ liệu
        connection = get_db_connection()
        cursor = connection.cursor()

        # Gửi request tới API của trường
        try:
            response = requests.post(url, json=payload, timeout=10, verify=False)
            response.raise_for_status()
            token_data = response.json()

            access_token = token_data.get("access_token")
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            rows = cursor.fetchall()

            if rows:
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
            # Xử lý trường hợp không kết nối được API
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            rows = cursor.fetchall()

            if rows:
                is_match = check_password_hash(rows[0]["password"], password)
                if is_match:
                    query = "UPDATE users SET state = ? WHERE username = ?"
                    cursor.execute(query, ("online", username))
                    connection.commit()

                    return jsonify({
                        "message": "Login successful, data saved!",
                        "username": username,
                        "role": rows[0]["role"]
                    }), 200
                else:
                    return jsonify({"message": "Mật khẩu sai!"}), 400
            else:
                query = "INSERT INTO users (username, password, access_token, role, state) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(query, (username, hashed_password, "", role, "online"))
                connection.commit()

                return jsonify({
                    "message": "Login successful, data saved!",
                    "username": username,
                    "role": role
                }), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"Lỗi cơ sở dữ liệu: {e}"}), 500
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

        return jsonify({"message": "Đăng xuất thành công!"}), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"Có lỗi xảy ra khi đăng xuất: {e}"}), 500
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
            "Authorization": token
        }

        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        data = response.json()

        return jsonify({
            "message": "Get current user success",
            "gpa": data.get("mark4")
        }), 200

    except requests.RequestException as e:
        return jsonify({"message": f"Co loi xay ra: {e}"}), 500