from flask import Flask, render_template, request 
from flask import jsonify
import sqlite3
import requests

def get_db_connection():
    connection = sqlite3.connect('./database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_dashboard_info_admin(request):
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
    
def get_dashboard_info_users(request):
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
