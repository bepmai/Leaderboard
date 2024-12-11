from flask import Blueprint

# Tạo Blueprint cho phần auth
score_board_bp = Blueprint('score_board', __name__)

from . import routes
