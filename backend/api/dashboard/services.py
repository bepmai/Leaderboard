from flask import Flask, render_template, request 
from flask import jsonify
import sqlite3
import requests
from api.attendance.services import update_attendace_table

score_board_URL = "https://sheetdb.io/api/v1/hxr0hvr4g1ftk"
attendance_URL = "https://sheetdb.io/api/v1/ki61n94i86kj3"

def get_db_connection():
    connection = sqlite3.connect('./database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_dashboard_info_admin(request):
    try:
        response = requests.get(attendance_URL)
        if response.status_code == 200:
            data = response.json()

            if data:
                del data[0]  # Hoặc: data.pop(0)

            update_attendace_table(data)
        else:
            return jsonify({"message": f"Error occurred: {response.status_code}"}), 500
    
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM attendances WHERE absent <= 3")
        school_attendance_rate = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM attendances WHERE absent > 3")
        break_rate = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(stated) FROM attendances")
        number_of_speeches = cursor.fetchone()[0]

        connection.close()
        
        return jsonify({
            "message": "Dashboard info fetched successfully!",
            "School_attendance_rate": school_attendance_rate,
            "Break_rate": break_rate,
            "number_of_speeches": number_of_speeches
        }), 200
    except Exception as e:
        return jsonify({
            "message": "An error occurred while fetching dashboard info.",
            "error": str(e)
        }), 500
    
def get_dashboard_info_users(request):
    try:
        id = request.args.get('id')
        response = requests.get(score_board_URL)
        if response.status_code == 200:
            data = response.json()

            student_data = [record for record in data if record.get("Mã sinh viên") == id]
        
            if student_data:
                connection = get_db_connection()
                cursor = connection.cursor()

                for item in student_data:
                    cursor.execute("SELECT * FROM score_boards WHERE msv = ?", (item['Mã sinh viên'],))
                    exists = cursor.fetchone()

                    if exists:
                        cursor.execute(
                            "UPDATE score_boards SET stt = ?, first_name = ?,last_name = ?,class = ?,Go_to_the_board = ?,Summarize_Mindmap = ?,code_sytem = ?,Total = ? WHERE msv = ?",
                            (item['STT'], item['Họ '],item['Tên'], item['Lớp'], item['Lên bảng'],item['Mindmap tổng hợp'], item['Code hệ thống'],item['Tổng điểm tích cực'],item['Mã sinh viên']) 
                        )
                    else:
                        cursor.execute(
                            "INSERT INTO score_boards (msv, stt, first_name,last_name,class,Go_to_the_board,Summarize_Mindmap,code_sytem,Total) VALUES (?, ?, ?,?, ?, ?,?, ?, ?)",
                            (item['Mã sinh viên'], item['STT'], item['Họ '],item['Tên'], item['Lớp'], item['Lên bảng'],item['Mindmap tổng hợp'], item['Code hệ thống'],item['Tổng điểm tích cực']) 
                        )

                connection.commit()
                connection.close()
            else:
                return jsonify({"message": f"Error occurred: Không tìm thấy dữ liệu"}), 500
        else:
            return jsonify({"message": f"Error occurred: {response.status_code}"}), 500
        
        response = requests.get(attendance_URL)
        if response.status_code == 200:
            data = response.json()

            student_data = [record for record in data if record.get("Mã sinh viên") == id]
        
            if student_data:
                update_attendace_table(student_data)
            else:
                return jsonify({"message": f"Error occurred: Không tìm thấy dữ liệu"}), 500
        else:
            return jsonify({"message": f"Error occurred: {response.status_code}"}), 500

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM attendance_of_day WHERE absent != ? AND msv = ?", ('v', id))
        number_of_school_attendance = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM attendance_of_day WHERE absent == ? AND msv = ?", ('v', id))
        number_of_break = cursor.fetchone()[0]
        
        cursor.execute("SELECT Total FROM score_boards WHERE msv = ?", (id,))
        number_of_speeches_cluster = cursor.fetchone()[0]
        
        cursor.execute("SELECT stated FROM attendances WHERE msv = ?", (id,))
        number_of_speeches_class = cursor.fetchone()[0]

        cursor.execute("SELECT MSV, absent, volunteer_group, point_group, point_project FROM point ORDER BY point_group DESC")
        result = cursor.fetchall()

        rank = 1
        for item in result:
            msv = item['MSV'] if isinstance(item, dict) else item[0]
            if msv == id:
                break
            rank += 1

        if rank > len(result):
            rank = 0

        connection.close()
        
        return jsonify({
            "message": "Dashboard info fetched successfully!",
            "number_of_school_attendance": number_of_school_attendance,
            "number_of_break": number_of_break,
            "Number_of_speeches_cluster": number_of_speeches_cluster,
            "Number_of_speeches_class": number_of_speeches_class,
            "rank": rank
        }), 200
    except Exception as e:
        return jsonify({
            "message": "An error occurred while fetching dashboard info.",
            "error": str(e)
        }), 500


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

def get_absent_student_by_msv(msv,request):
    connection = get_db_connection()
    cursor = connection.cursor()
    result_list = []
    
    cursor.execute("SELECT COUNT(MSV) as ABSEND_STD FROM ATTENDANCE_OF_DAY WHERE ABSENT = 'v' and MSV = ?",(msv,))
    absent_student = cursor.fetchone()[0]
    
    result_list.append(absent_student)
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

def get_absent_student_by_day_by_msv(msv,request):
    connection = get_db_connection()
    cursor = connection.cursor()
    result_list = []
    
    cursor.execute("SELECT COUNT(MSV) as ALL_STD FROM ATTENDANCE_OF_DAY WHERE ABSENT != 'v' and day =? and MSV= ?",(request,msv,))
    total_student = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(MSV) as ABSEND_STD FROM ATTENDANCE_OF_DAY WHERE ABSENT = 'v' and day = ? and MSV= ?",(request,msv,))
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
    
def get_stated_all_student_by_day_by_msv(day,request):
    connection = get_db_connection()
    cursor = connection.cursor()
    result_list = []
    msv = request.args.get("MSV")
    cursor.execute("SELECT SUM(stated) FROM ATTENDANCE_of_day WHERE msv = ? and day =?",(msv,day))
    total_student = cursor.fetchone()[0]

    result_list.append(total_student)
    cursor.close()

    return jsonify({
        "message": "Point fetched successfully!",
        "data": result_list
    }), 200

def get_stated_of_user_in_group(student):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT GO_TO_the_board,Summarize_Mindmap,code_sytem FROM SCORE_BOARDS WHERE MSV = ?",(student,))
    state = cursor.fetchone()
    result = dict(state)
    return jsonify({
        "message":"Point fetched successfully!",
        "data":result
    }),200
    
def get_name_of_user_in_group(request):
    connection = get_db_connection()
    cursor= connection.cursor()
    cursor.execute("SELECT msv,last_name FROM SCORE_BOARDS")
    names = cursor.fetchall()
    result = [row[1] for row in names]
    resultMSV = [row[0] for row in names]
    return jsonify({
        "message":"Point fetched successfully!",
        "data":[resultMSV,result]
    }),200


