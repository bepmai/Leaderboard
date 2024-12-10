from flask import request, jsonify
from .services import login, logout, get_gpa
from . import auth_bp

@auth_bp.route('/login', methods=['POST'])
def login_route():
    return login(request)

@auth_bp.route('/logout', methods=['POST'])
def logout_route():
    return logout(request)

@auth_bp.route('/getGPA', methods=['GET'])
def get_gpa_route():
    return get_gpa(request)

@auth_bp.route("/helloworld",methods=['GET'])
def helloworldl():
    return "hello world!"
