from flask import request, jsonify
from .services import get_dashboard_info_admin, get_dashboard_info_users
from . import dashboard_bp

@dashboard_bp.route('/dashboard_info_admin', methods=['GET'])
def dashboard_info_admin_route():
    return get_dashboard_info_admin(request)

@dashboard_bp.route('/dashboard_info_users', methods=['GET'])
def dashboard_info_users_route():
    return get_dashboard_info_users(request)
