from flask import Flask, render_template, request 
from flask import jsonify
import sqlite3
import requests

score_board_URL = "https://sheetdb.io/api/v1/ma8opp1ci2oqd"

def get_db_connection():
    connection = sqlite3.connect('./database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_score_board_admin(request):
    response = requests.get(score_board_URL)
    if response.status_code == 200:
        data = response.json()

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM score_boards")

        for item in data:
            cursor.execute(
                "INSERT INTO score_boards (msv, stt, first_name,last_name,class,Go_to_the_board,Summarize_Mindmap,code_sytem,Total) VALUES (?, ?, ?,?, ?, ?,?, ?, ?)",
                (item['Mã sinh viên'], item['STT'], item['Họ '],item['Tên'], item['Lớp'], item['Lên bảng'],item['Mindmap tổng hợp'], item['Code hệ thống'],item['Tổng điểm tích cực']) 
            )

        connection.commit()
        connection.close()

        return jsonify({
            "message": "Score board fetched successfully!",
            "data": data
        }), 200
    else:
        return jsonify({"message": f"Error occurred: {response.status_code}"}), 500
    
def get_score_board_users(request):
    response = requests.get(score_board_URL)
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
                cursor.execute("SELECT COUNT(*) FROM score_boards WHERE id = ?", (item['id'],))
                exists = cursor.fetchone()[0]

                if exists:
                    # Cập nhật bản ghi nếu đã tồn tại
                    cursor.execute(
                        "UPDATE score_boards SET stt = ?, first_name = ?,last_name = ?,class = ?,Go_to_the_board = ?,Summarize_Mindmap = ?,code_sytem = ?,Total = ? WHERE msv = ?",
                        (item['STT'], item['Họ '],item['Tên'], item['Lớp'], item['Lên bảng'],item['Mindmap tổng hợp'], item['Code hệ thống'],item['Tổng điểm tích cực'],item['Mã sinh viên']) 
                    )
                else:
                    # Thêm bản ghi nếu chưa tồn tại
                    cursor.execute(
                        "INSERT INTO score_boards (msv, stt, first_name,last_name,class,Go_to_the_board,Summarize_Mindmap,code_sytem,Total) VALUES (?, ?, ?,?, ?, ?,?, ?, ?)",
                        (item['Mã sinh viên'], item['STT'], item['Họ '],item['Tên'], item['Lớp'], item['Lên bảng'],item['Mindmap tổng hợp'], item['Code hệ thống'],item['Tổng điểm tích cực']) 
                    )

            connection.commit()
            connection.close()

            return jsonify({
            "message": "Score board fetched successfully!",
            "data": student_data
        }), 200
        else:
            return jsonify({"message": f"Error occurred: Không tìm thấy dữ liệu"}), 500
    else:
        return jsonify({"message": f"Error occurred: {response.status_code}"}), 500
