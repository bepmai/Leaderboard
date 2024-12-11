from flask import Blueprint

# Tạo Blueprint cho phần auth
dashboard_bp = Blueprint('dashboard', __name__)

from . import routes
