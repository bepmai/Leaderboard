from flask import Blueprint

# Tạo Blueprint cho phần auth
auth_bp = Blueprint('auth', __name__)

from . import routes
