from flask import request, jsonify
from .services import login, logout,checkRole
from . import auth_bp
from ..token.check import token_required

@auth_bp.route('/login', methods=['POST'])
def login_route():
    return login(request)

@auth_bp.route('/logout', methods=['POST'])
def logout_route():
    return logout(request)

@auth_bp.route('/role', methods=['POST'])
@token_required
def check_route():
    return checkRole(request)
