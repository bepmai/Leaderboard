from flask import request
from .services import get_score_board_admin, get_score_board_users
from . import score_board_bp

@score_board_bp.route('/score_board_admin', methods=['GET'])
def get_score_board_admin_route():
    return get_score_board_admin(request)

@score_board_bp.route('/score_board_users', methods=['GET'])
def get_score_board_users_route():
    return get_score_board_users(request)