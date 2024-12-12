from flask import request, jsonify
from .services import get_gpa,get_infor
from . import infor_bp
from ..token.check import token_required

@infor_bp.route('/getGPA', methods=['GET'])
@token_required
def get_gpa_route():
    return get_gpa(request)

@infor_bp.route("/getInfor",methods=['GET'])
@token_required
def get_infor_route():
    return get_infor(request)