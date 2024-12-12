import sqlite3
from flask import Flask, jsonify, request, Blueprint
from functools import wraps
app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect('./database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE access_token = ? or username = ?", (token,token))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            current_user = user
            return f(*args, **kwargs)
        return jsonify({"message": "Invalid token!"}), 401
    return decorated