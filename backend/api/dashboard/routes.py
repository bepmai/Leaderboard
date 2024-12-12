from . import dashboard_bp
from flask import request, jsonify
from .service import get_dashboard, get_dashboard_user

@dashboard_bp.route("/dashboard",methods=["GET"])
def get_dashboard():
    return 