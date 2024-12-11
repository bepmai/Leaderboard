from flask import request, jsonify
from .services import login, logout
from . import auth_bp

@auth_bp.route('/login', methods=['POST'])
def login_route():
    return login(request)

@auth_bp.route('/logout', methods=['POST'])
def logout_route():
    return logout(request)
