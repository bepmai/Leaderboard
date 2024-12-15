from flask import request, jsonify
from .services import get_dashboard_info_admin, get_dashboard_info_users,get_absent_student,get_absent_student_by_day,get_stated_student_by_day,get_stated_all_student_by_day,get_stated_of_user_in_group,get_absent_student_by_msv,get_absent_student_by_day_by_msv,get_name_of_user_in_group
from . import dashboard_bp
from ..token.check import token_required

@dashboard_bp.route('/dashboard_info_admin', methods=['GET'])
@token_required
def dashboard_info_admin_route():
    return get_dashboard_info_admin(request)

@dashboard_bp.route('/dashboard_info_users', methods=['GET'])
@token_required
def dashboard_info_users_route():
    return get_dashboard_info_users(request)

@dashboard_bp.route('/chart/absent',methods=['GET'])
@token_required
def dashboard_get_absent():
    return get_absent_student(request)

@dashboard_bp.route('/chart/absent/<int:day>',methods=['GET'])
@token_required
def dashboard_get_absent_by_day(day):
    return get_absent_student_by_day(day)

@dashboard_bp.route('/chart/absent_msv/<string:msv>',methods=['GET'])
@token_required
def dashboard_get_absent_by_msv(msv):
    return get_absent_student_by_msv(msv,request)

@dashboard_bp.route('/chart/absent_msv/<string:msv>/<int:day>',methods=['GET'])
@token_required
def dashboard_get_absent_by_day_by_msv(msv,day):
    return get_absent_student_by_day_by_msv(msv,day)

@dashboard_bp.route('/chart/stated/<int:day>',methods=['GET'])
@token_required
def dashboard_get_stated_all_by_day(day):
    return get_stated_all_student_by_day(day)

@dashboard_bp.route('/chart/stated/<int:day>/id',methods=['GET'])
@token_required
def dashboard_get_stated_by_day(day):
    return get_stated_student_by_day(day,request)

@dashboard_bp.route('/chart/stated/group/<string:student>',methods=['GET'])
@token_required
def dashboard_get_stated_group_by_msv(student):
    return get_stated_of_user_in_group(student)

@dashboard_bp.route('/chart/namestd_of_group',methods=['GET'])
@token_required
def get_name_of_group():
    return get_name_of_user_in_group(request)
