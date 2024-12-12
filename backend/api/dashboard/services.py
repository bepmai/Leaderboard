from flask import Flask, render_template, request 
from flask import jsonify
import sqlite3
import requests

def get_db_connection():
    connection = sqlite3.connect('./database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_dashboard_info_admin(request):
    try:
        with get_db_connection() as connection:  # Context manager for connection
            cursor = connection.cursor()  # Manually manage the cursor
            try:
                # Fetch school attendance rate
                cursor.execute("SELECT COUNT(*) FROM attendances WHERE absent <= 3")
                school_attendance_rate = cursor.fetchone()[0]
                
                # Fetch break rate
                cursor.execute("SELECT COUNT(*) FROM attendances WHERE absent > 3")
                break_rate = cursor.fetchone()[0]
                
                # Fetch number of speeches (cluster)
                cursor.execute("SELECT SUM(Total) FROM score_boards")
                number_of_speeches_cluster = cursor.fetchone()[0]
                
                # Fetch number of speeches (class)
                cursor.execute("SELECT SUM(stated) FROM attendances")
                number_of_speeches_class = cursor.fetchone()[0]
            finally:
                connection.close()  # Ensure the cursor is closed after use
        
        return jsonify({
            "message": "Dashboard info fetched successfully!",
            "School_attendance_rate": school_attendance_rate,
            "Break_rate": break_rate,
            "Number_of_speeches_cluster": number_of_speeches_cluster,
            "Number_of_speeches_class": number_of_speeches_class
        }), 200
    except Exception as e:
        return jsonify({
            "message": "An error occurred while fetching dashboard info.",
            "error": str(e)
        }), 500
    
def get_dashboard_info_users(request):
    try:
        id = request.args.get('id')
        with get_db_connection() as connection:  # Context manager for connection
            cursor = connection.cursor()  # Manually manage the cursor
            try:
                # Fetch school attendance rate
                cursor.execute("SELECT COUNT(*) FROM attendance_of_day WHERE absent != ? AND msv = ?", ('v', id))
                number_of_school_attendance = cursor.fetchone()[0]
                
                # Fetch break rate
                cursor.execute("SELECT COUNT(*) FROM attendance_of_day WHERE absent == ? AND msv = ?", ('v', id))
                number_of_break = cursor.fetchone()[0]
                
                # Fetch number of speeches (cluster)
                cursor.execute("SELECT Total FROM score_boards WHERE msv = ?", (id,))
                number_of_speeches_cluster = cursor.fetchone()[0]
                
                # Fetch number of speeches (class)
                cursor.execute("SELECT stated FROM attendances WHERE msv = ?", (id,))
                number_of_speeches_class = cursor.fetchone()[0]

                # Fetch all ranking data
                cursor.execute("SELECT MSV, absent, volunteer_group, point_group, point_project FROM point ORDER BY point_group DESC")
                result = cursor.fetchall()

                rank = 1
                for item in result:
                    # Use dictionary indexing or tuple indexing based on fetch style
                    msv = item['MSV'] if isinstance(item, dict) else item[0]
                    if msv == id:
                        break
                    rank += 1

                # Handle case where user is not found in result
                if rank > len(result):
                    rank = 0

            finally:
                connection.close()  # Ensure the cursor is closed after use
        
        return jsonify({
            "message": "Dashboard info fetched successfully!",
            "number_of_school_attendance": number_of_school_attendance,
            "number_of_break": number_of_break,
            "Number_of_speeches_cluster": number_of_speeches_cluster,
            "Number_of_speeches_class": number_of_speeches_class,
            "rank": rank
        }), 200
    except Exception as e:
        return jsonify({
            "message": "An error occurred while fetching dashboard info.",
            "error": str(e)
        }), 500