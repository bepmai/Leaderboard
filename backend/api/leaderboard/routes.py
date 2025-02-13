from flask import request, jsonify
from .services import get_point_class,get_point_group,get_full_name
from . import leaderboard_bp
from ..token.check import token_required
@leaderboard_bp.route('/getLeader')
@token_required
def get_leaderboard_group():
    return get_point_group(request)

@leaderboard_bp.route('/getLeaderClass')
@token_required
def get_leaderboard_class():
    return get_point_class(request)

@leaderboard_bp.route('/getFullName')
@token_required
def getFullName():
    return get_full_name(request)