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

def get_absent_student(request):
    connection = get_db_connection()
    cursor = connection.cursor()
    result_list = []
    
    cursor.execute("SELECT COUNT(MSV) as ALL_STD FROM attendances")
    total_student = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(MSV) as ABSEND_STD FROM ATTENDANCE_OF_DAY WHERE ABSENT = 'v'")
    absent_student = cursor.fetchone()[0]
    
    result_list.append(absent_student)
    result_list.append(total_student)
    cursor.close()

    return jsonify({
        "message": "Point fetched successfully!",
        "data": result_list
    }), 200

def get_absent_student_by_day(request):
    connection = get_db_connection()
    cursor = connection.cursor()
    result_list = []
    
    cursor.execute("SELECT COUNT(MSV) as ALL_STD FROM ATTENDANCE_OF_DAY WHERE ABSENT != 'v' and day =?",(request,))
    total_student = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(MSV) as ABSEND_STD FROM ATTENDANCE_OF_DAY WHERE ABSENT = 'v' and day = ?",(request,))
    absent_student = cursor.fetchone()[0]
    
    result_list.append(absent_student)
    result_list.append(total_student)
    cursor.close()

    return jsonify({
        "message": "Point fetched successfully!",
        "data": result_list
    }), 200
    
def get_stated_all_student_by_day(request):
    connection = get_db_connection()
    cursor = connection.cursor()
    result_list = []
    
    cursor.execute("SELECT COUNT(MSV) as ALL_STD FROM ATTENDANCE_of_day WHERE STATED = '1' and day =?",(request,))
    total_student = cursor.fetchone()[0]

    result_list.append(total_student)
    cursor.close()

    return jsonify({
        "message": "Point fetched successfully!",
        "data": result_list
    }), 200
    
def get_stated_student_by_day(day,request):
    connection = get_db_connection()
    cursor = connection.cursor()
    result_list = []
    msv = request.args.get("MSV")
    cursor.execute("SELECT stated FROM ATTENDANCE_of_day WHERE MSV = ? and day =?",(msv,day))
    total_student = cursor.fetchone()[0]

    result_list.append(total_student)
    cursor.close()

    return jsonify({
        "message": "Point fetched successfully!",
        "data": result_list
    }), 200
    
def get_stated_all_student_by_day(day,request):
    connection = get_db_connection()
    cursor = connection.cursor()
    result_list = []
    msv = request.args.get("MSV")
    cursor.execute("SELECT SUM(stated) FROM ATTENDANCE_of_day WHERE and day =?",(msv,day))
    total_student = cursor.fetchone()[0]

    result_list.append(total_student)
    cursor.close()

    return jsonify({
        "message": "Point fetched successfully!",
        "data": result_list
    }), 200