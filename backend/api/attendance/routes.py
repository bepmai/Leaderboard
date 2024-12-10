from flask import request
from .services import get_attendance_admin, get_attendance_users
from . import attendance_bp

@attendance_bp.route('/attendance_admin', methods=['GET'])
def get_attendance_admin_route():
    return get_attendance_admin(request)

@attendance_bp.route('/attendance_users', methods=['GET'])
def get_attendance_users_route():
    return get_attendance_users(request)