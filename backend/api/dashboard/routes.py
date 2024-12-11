from flask import request
from .services import get_dashboard_admin, get_dashboard_users
from . import dashboard_bp

@dashboard_bp.route('/dashboard_info_admin', methods=['GET'])
def get_dashboard_admin_route():
    return get_dashboard_admin(request)

@dashboard_bp.route('/dashboard_users', methods=['GET'])
def get_dashboard_users_route():
    return get_dashboard_users(request)