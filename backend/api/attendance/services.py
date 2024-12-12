from flask_socketio import emit
from flask import jsonify
import sqlite3
import requests
from datetime import datetime

attendance_URL = "https://sheetdb.io/api/v1/tgpag8379teow"

def get_db_connection():
    connection = sqlite3.connect('./database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_attendance_info_admin(request):
    try:
        date_strings = ["12/11/2024", "15/11/2024", "22/11/2024", "26/11/2024","29/11/2024","03/12/2024","06/12/2024","10/12/2024","13/12/2024","17/12/2024","20/12/2024","24/12/2024","27/12/2024","31/12/2024","03/12/2024"]
        data = request.json
        day_request = data.get('date')
        if day_request:
            if day_request in date_strings:
                day = date_strings.index(day_request) + 2
            else:
                date_objects = [datetime.strptime(date, "%d/%m/%Y") for date in date_strings]

                today = datetime.now()
                day = 1
                for date in date_objects:
                    if today > date:
                        day+=1
                    else:
                        break
        else:
            date_objects = [datetime.strptime(date, "%d/%m/%Y") for date in date_strings]

            today = datetime.now()
            day = 1
            for date in date_objects:
                if today > date:
                    day+=1
                else:
                    break

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM attendance_of_day WHERE absent != ? AND day = ?", ('v', day))
        number_of_attendance = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM attendance_of_day WHERE absent = ? AND day = ?", ('v', day))
        number_of_break = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(stated) FROM attendance_of_day WHERE absent != ? AND day = ?", ('v', day))
        number_of_speeches = cursor.fetchone()[0]

        connection.close()
        
        return jsonify({
            "message": "Dashboard info fetched successfully!",
            "number_of_attendance": number_of_attendance,
            "number_of_break": number_of_break,
            "number_of_speeches": number_of_speeches
        }), 200
    except Exception as e:
        return jsonify({
            "message": "An error occurred while fetching dashboard info.",
            "error": str(e)
        }), 500

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

# def handle_fetch_attendance():
#     try:
#         response = requests.get(attendance_URL)
#         if response.status_code == 200:
#             data = response.json()

#             if data:
#                 del data[0]  # Remove the first item if required

#             connection = get_db_connection()
#             cursor = connection.cursor()

#             # Clear old data
#             cursor.execute("DELETE FROM attendances")
#             cursor.execute("DELETE FROM attendance_of_day")

#             # Insert new data
#             for item in data:
#                 cursor.execute(
#                     """
#                     INSERT INTO attendances 
#                     (msv, stt, first_name, last_name, class, project_point, note, absent, stated) 
#                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#                     """,
#                     (item['Mã sinh viên'], item['STT'], item['Họ'], item['Tên'], item['Lớp'], 
#                      item['Điểm project'], item['Ghi chú'], item['Vắng'], item['Phát biểu'])
#                 )

#                 for i in range(1, 16):
#                     if item[f'{i}'] == 'v' or item[f'{i}'] == 'pb':
#                         if item[f'{i}'] == 'pb':
#                             cursor.execute(
#                                 """
#                                 INSERT INTO attendance_of_day (msv, day, stated, absent) 
#                                 VALUES (?, ?, ?, ?)
#                                 """,
#                                 (item['Mã sinh viên'], i, 1, '')
#                             )
#                         else:
#                             cursor.execute(
#                                 """
#                                 INSERT INTO attendance_of_day (msv, day, stated, absent) 
#                                 VALUES (?, ?, ?, ?)
#                                 """,
#                                 (item['Mã sinh viên'], i, '', item[f'{i}'])
#                             )
#                     else:
#                         cursor.execute(
#                             """
#                             INSERT INTO attendance_of_day (msv, day, stated, absent) 
#                             VALUES (?, ?, ?, ?)
#                             """,
#                             (item['Mã sinh viên'], i, '', '')
#                         )

#             connection.commit()
#             connection.close()

#             # Emit success response with data
#             emit('attendance_fetched', {
#                 "message": "Attendance fetched successfully!",
#                 "data": data
#             })
#         else:
#             # Emit error response if the API call fails
#             emit('attendance_error', {
#                 "message": f"Error occurred: {response.status_code}"
#             })
#     except Exception as e:
#         # Emit error response in case of an exception
#         emit('attendance_error', {
#             "message": f"An error occurred: {str(e)}"
#         })