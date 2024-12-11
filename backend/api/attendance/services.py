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

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM attendances")

        for item in data:
            cursor.execute(
                "INSERT INTO attendances (id, name, score) VALUES (?, ?, ?)",
                (item['id'], item['name'], item['score']) 
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
        request_body = request.json
        id = request_body.get('id')
        student_data = [record for record in data if record.get("Mã sinh viên") == id]
    
        if student_data:
            connection = get_db_connection()
            cursor = connection.cursor()

            for item in student_data:
                # Kiểm tra xem bản ghi với ID đã tồn tại chưa
                cursor.execute("SELECT COUNT(*) FROM attendances WHERE id = ?", (item['id'],))
                exists = cursor.fetchone()[0]

                if exists:
                    # Cập nhật bản ghi nếu đã tồn tại
                    cursor.execute(
                        "UPDATE attendances SET name = ?, score = ? WHERE id = ?",
                        (item['name'], item['score'], item['id'])
                    )
                else:
                    # Thêm bản ghi nếu chưa tồn tại
                    cursor.execute(
                        "INSERT INTO attendances (id, name, score) VALUES (?, ?, ?)",
                        (item['id'], item['name'], item['score'])
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
