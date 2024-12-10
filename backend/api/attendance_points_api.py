from flask import Flask, render_template, request 
import sqlite3
import requests

SHEETDB_URL = "https://sheetdb.io/api/v1/ma8opp1ci2oqd"

def get_attendance_points_admin():
    response = requests.get(SHEETDB_URL)
    if response.status_code == 200:
        data = response.json()
        return render_template('../pages/attendance-points-admin.html',data = data) 
    else:
        return render_template('../pages/attendance-points-admin.html',data = data,message = f"Yêu cầu thất bại: {response.status_code}")
    
def get_attendance_points_users():
    response = requests.get(SHEETDB_URL)
    if response.status_code == 200:
        data = response.json()
        return render_template('../pages/attendance-points-admin.html',data = data) 
    else:
        return render_template('../pages/attendance-points-admin.html',data = data,message = f"Yêu cầu thất bại: {response.status_code}")