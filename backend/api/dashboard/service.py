from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask import jsonify
import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite
def get_db_connection():
    connection = sqlite3.connect('./database/database.db')
    connection.row_factory = sqlite3.Row
    return connection
def get_dashboard(request):
    return
def get_dashboard_user(request):
    return