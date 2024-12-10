from flask import Blueprint, request, jsonify
import requests

gpa_bp = Blueprint('gpa', __name__)

@gpa_bp.route('/get', methods=['GET'])
def getGPA():
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
