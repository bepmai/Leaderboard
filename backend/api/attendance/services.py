from flask import Flask, render_template, request 
from flask import jsonify
import sqlite3
import requests

attendance_URL = "https://sheetdb.io/api/v1/tgpag8379teow"

def get_db_connection():
    connection = sqlite3.connect('./database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_attendance_admin(request):
    response = requests.get(attendance_URL)
    if response.status_code == 200:
        data = response.json()

        if data:
            del data[0]  # Hoặc: data.pop(0)

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM attendances")
        cursor.execute("DELETE FROM attendance_of_day")

        for item in data:
            cursor.execute(
                "INSERT INTO attendances (msv, stt, first_name,last_name,class,project_point,note,absent,stated) VALUES (?, ?, ?,?, ?, ?,?, ?, ?)",
                (item['Mã sinh viên'], item['STT'], item['Họ'],item['Tên'], item['Lớp'], item['Điểm project'],item['Ghi chú'], item['Vắng'],item['Phát biểu']) 
            )
            for i in range(1,16):
                if (item[f'{i}']=='v' or item[f'{i}']=='pb'):
                    if (item[f'{i}']=='pb'):
                        cursor.execute(
                            "INSERT INTO attendance_of_day (msv, day,stated,absent) VALUES (?, ?, ?,?)",
                            (item['Mã sinh viên'], i, 1,'') 
                        )
                    else:
                        cursor.execute(
                            "INSERT INTO attendance_of_day (msv, day,stated,absent) VALUES (?, ?, ?,?)",
                            (item['Mã sinh viên'], i, '',item[f'{i}']) 
                        )
                else:
                    cursor.execute(
                            "INSERT INTO attendance_of_day (msv, day,stated,absent) VALUES (?, ?, ?,?)",
                            (item['Mã sinh viên'], i, '','') 
                        )

        connection.commit()
        connection.close()
        return jsonify({
            "message": "Attendance fetched successfully!",
            "data": data
        }), 200
    else:
        return jsonify({"message": f"Error occurred: {response.status_code}"}), 500
    
def get_attendance_users(request):
    response = requests.get(attendance_URL)
    if response.status_code == 200:
        data = response.json()

        id = request.args.get('id')

        student_data = [record for record in data if record.get("Mã sinh viên") == id]
    
        if student_data:
            connection = get_db_connection()
            cursor = connection.cursor()

            for item in student_data:
                # Kiểm tra xem bản ghi với ID đã tồn tại chưa
                cursor.execute("SELECT COUNT(*) FROM attendances WHERE msv = ?", (item['Mã sinh viên'],))
                exists = cursor.fetchone()[0]

                cursor.execute("DELETE FROM attendance_of_day WHERE msv = ?", (item['Mã sinh viên'],))

                if exists:
                    # Cập nhật bản ghi nếu đã tồn tại
                    cursor.execute(
                        "UPDATE attendances SET stt = ?, first_name = ?,last_name = ?,class = ?,project_point = ?,note = ?,absent = ?,stated = ? WHERE msv = ?",
                        (item['STT'], item['Họ'],item['Tên'], item['Lớp'], item['Điểm project'],item['Ghi chú'], item['Vắng'],item['Phát biểu'],item['Mã sinh viên']) 
                    )
                    for i in range(1,16):
                        if (item[f'{i}']=='v' or item[f'{i}']=='pb'):
                            if (item[f'{i}']=='pb'):
                                cursor.execute(
                                    "INSERT INTO attendance_of_day (msv, day,stated,absent) VALUES (?, ?, ?,?)",
                                    (item['Mã sinh viên'], i, 1,'') 
                                )
                            else:
                                cursor.execute(
                                    "INSERT INTO attendance_of_day (msv, day,stated,absent) VALUES (?, ?, ?,?)",
                                    (item['Mã sinh viên'], i, '',item[f'{i}']) 
                                )
                        else:
                            cursor.execute(
                                    "INSERT INTO attendance_of_day (msv, day,stated,absent) VALUES (?, ?, ?,?)",
                                    (item['Mã sinh viên'], i, '','') 
                                )
                else:
                    cursor.execute(
                        "INSERT INTO attendances (msv, stt, first_name,last_name,class,project_point,note,absent,stated) VALUES (?, ?, ?,?, ?, ?,?, ?, ?)",
                        (item['Mã sinh viên'], item['STT'], item['Họ'],item['Tên'], item['Lớp'], item['Điểm project'],item['Ghi chú'], item['Vắng'],item['Phát biểu']) 
                    )
                    cursor.execute("DELETE FROM attendance_of_day WHERE msv = ?", (item['Mã sinh viên'],))
                    
                    for i in range(1,16):
                        if (item[f'{i}']=='v' or item[f'{i}']=='pb'):
                            if (item[f'{i}']=='pb'):
                                cursor.execute(
                                    "INSERT INTO attendance_of_day (msv, day,stated,absent) VALUES (?, ?, ?,?)",
                                    (item['Mã sinh viên'], i, 1,'') 
                                )
                            else:
                                cursor.execute(
                                    "INSERT INTO attendance_of_day (msv, day,stated,absent) VALUES (?, ?, ?,?)",
                                    (item['Mã sinh viên'], i, '',item[f'{i}']) 
                                )
                        else:
                            cursor.execute(
                                    "INSERT INTO attendance_of_day (msv, day,stated,absent) VALUES (?, ?, ?,?)",
                                    (item['Mã sinh viên'], i, '','') 
                                )

            connection.commit()
            connection.close()

            return jsonify({
            "message": "Attendance fetched successfully!",
            "data": student_data
        }), 200
        else:
            return jsonify({"message": f"Error occurred: Không tìm thấy dữ liệu"}), 500
    else:
        return jsonify({"message": f"Error occurred: {response.status_code}"}), 500
