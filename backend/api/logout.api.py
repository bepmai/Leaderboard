from flask import Blueprint, request, jsonify
import sqlite3

user_bp = Blueprint('user', __name__)

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

@user_bp.route('/logout', methods=['POST'])
def logout():
    try:
        data = request.json
        username = data.get('username')

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "UPDATE users SET state = ? WHERE username = ?"
        cursor.execute(query, ("offline", username))
        connection.commit()

        return jsonify({"message": "Logged out successfully!"}), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"Error during logout: {e}"}), 500
    finally:
        connection.close()
