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
    cursor.execute("SELECT point.MSV,attendances.first_name,attendances.last_name,point.absent,point.volunteer_group,point.point_group,point.point_project FROM point inner join attendances where point.msv = attendances.msv ORDER BY point_class DESC")
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
    cursor.execute("SELECT point.MSV,attendances.first_name,attendances.last_name,point.absent,point.volunteer_class,point.point_class,point.point_project FROM point inner join attendances where point.msv = attendances.msv ORDER BY point_class DESC")
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    result_list = [dict(row) for row in result]
    return jsonify({
        "message": "Point fetched successfully!",
        "data": result_list
    }), 200
    
def get_full_name(request):
    msv = request.args.get("MSV")
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT first_name,last_name from attendances where msv = ?",(msv,))
    result = cursor.fetchone()
    connection.commit()
    connection.close()
    return jsonify({
        "message": "Name fetched successfully!",
        "data": result[0] +" "+ result[1]
    }), 200

