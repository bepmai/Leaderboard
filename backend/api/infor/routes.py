from flask import request, jsonify
from .services import get_gpa
from . import infor_bp

@infor_bp.route('/getGPA', methods=['GET'])
def get_gpa_route():
    return get_gpa(request)

@infor_bp.route("/helloworld",methods=['GET'])
def helloworldl():
    return "hello world!"