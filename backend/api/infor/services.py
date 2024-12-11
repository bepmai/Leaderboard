from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask import jsonify
import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite
def get_db_connection():
    connection = sqlite3.connect('./database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_gpa(request):
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Authorization token is required"}), 400

        url = "https://sinhvien1.tlu.edu.vn/education/api/studentsummarymark/getbystudent"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        data = response.json()

        return jsonify({
            "message": "GPA fetched successfully!",
            "gpa": data.get("mark4")
        }), 200

    except requests.RequestException as e:
        return jsonify({"message": f"Error occurred: {e}"}), 500
def get_infor(request):
    try:
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Authorization token is required"}), 400

        url = "https://sinhvien1.tlu.edu.vn/education/api/studentsummarymark/getbystudent"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        data = response.json()
        result = {
            "MSV":data.get("student").get("studentCode"),
            "fullname":data.get("student").get("displayName"),
            "class":data.get("student").get("enrollmentClass").get("className"),
            "department":data.get("student").get("enrollmentClass").get("department").get("name"),
            "courseyear":data.get("student").get("enrollmentClass").get("courseyear").get("code"),
            "gender":data.get("student").get("gender"),
            "gpa":data.get("mark4"),
            "speciality":data.get("student").get("enrollmentClass").get("speciality").get("name"),
            "phoneNumber":data.get("student").get("phoneNumber"),
            "dateOfBirth":data.get("student").get("birthDateString"),
            "address":data.get("student").get("birthPlace")
        }
        return jsonify({
            "message": "Fetched successfully!",
            "data": result
        }), 200

    except requests.RequestException as e:
        return jsonify({"message": f"Error occurred: {e}"}), 500
