from flask import Blueprint

# Tạo Blueprint cho phần auth
infor_bp = Blueprint('infor', __name__)

from . import routes
