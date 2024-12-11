import requests
from flask import jsonify
import sqlite3

def get_db_connection():
    connection = sqlite3.connect('./database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_point_group(request):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT MSV,absent,volunteer_group,point_group,point_project FROM point ORDER BY point_group DESC")
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    result_list = [dict(row) for row in result]
    return jsonify({
        "message": "Point fetched successfully!",
        "data": result_list
    }), 200

def get_point_class(request):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT MSV,absent,volunteer_class,point_class,point_project FROM point ORDER BY point_class DESC")
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    result_list = [dict(row) for row in result]
    return jsonify({
        "message": "Point fetched successfully!",
        "data": result_list
    }), 200

