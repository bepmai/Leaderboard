from flask import Flask, render_template, request 
import sqlite3
import requests

SHEETDB_URL = "https://sheetdb.io/api/v1/ma8opp1ci2oqd"

def get_score_board_admin():
    response = requests.get(SHEETDB_URL)
    if response.status_code == 200:
        data = response.json()
        return render_template('../pages/score-board.html',data = data) 
    else:
        return render_template('../pages/score-board.html',data = data,message = f"Yêu cầu thất bại: {response.status_code}")
    
def get_score_board_users(id):
    response = requests.get(SHEETDB_URL)
    if response.status_code == 200:
        data = response.json()
        student_data = [record for record in data if record.get("Mã sinh viên") == id]
    
        if student_data:
            return render_template('../pages/score-board.html',data = data) 
        else:
            return render_template('../pages/score-board.html',data = data,message = f"Không tìm thấy bản ghi") 
    else:
        return render_template('../pages/score-board.html',data = data,message = f"Yêu cầu thất bại: {response.status_code}")