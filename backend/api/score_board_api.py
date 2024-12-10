from flask import Flask, render_template, request 
import sqlite3
import requests

score_board_URL = "https://sheetdb.io/api/v1/ma8opp1ci2oqd"

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_score_board_admin():
    response = requests.get(score_board_URL)
    if response.status_code == 200:
        data = response.json()

        # connection = get_db_connection()
        # cursor = connection.cursor()

        # cursor.execute("DELETE FROM score_boards")

        # for item in data:
        #     cursor.execute(
        #         "INSERT INTO score_boards (id, name, score) VALUES (?, ?, ?)",
        #         (item['id'], item['name'], item['score']) 
        #     )

        # connection.commit()
        # connection.close()

        return render_template('../pages/score-board.html',data = data) 
    else:
        return render_template('../pages/score-board.html',data = None,message = f"Yêu cầu thất bại: {response.status_code}")
    
def get_score_board_users(id):
    response = requests.get(score_board_URL)
    if response.status_code == 200:
        data = response.json()
        student_data = [record for record in data if record.get("Mã sinh viên") == id]
    
        if student_data:
            # connection = get_db_connection()
            # cursor = connection.cursor()

            # for item in student_data:
            #     # Kiểm tra xem bản ghi với ID đã tồn tại chưa
            #     cursor.execute("SELECT COUNT(*) FROM score_boards WHERE id = ?", (item['id'],))
            #     exists = cursor.fetchone()[0]

            #     if exists:
            #         # Cập nhật bản ghi nếu đã tồn tại
            #         cursor.execute(
            #             "UPDATE score_boards SET name = ?, score = ? WHERE id = ?",
            #             (item['name'], item['score'], item['id'])
            #         )
            #     else:
            #         # Thêm bản ghi nếu chưa tồn tại
            #         cursor.execute(
            #             "INSERT INTO score_boards (id, name, score) VALUES (?, ?, ?)",
            #             (item['id'], item['name'], item['score'])
            #         )

            # connection.commit()
            # connection.close()

            return render_template('../pages/score-board.html', data=student_data)
        else:
            return render_template('../pages/score-board.html', data=None, message="Không tìm thấy bản ghi")
    else:
        return render_template('../pages/score-board.html', data=None, message=f"Yêu cầu thất bại: {response.status_code}")
