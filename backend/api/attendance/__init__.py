from flask import Blueprint

# Tạo Blueprint cho phần auth
attendance_bp = Blueprint('attendance', __name__)

from . import routes
