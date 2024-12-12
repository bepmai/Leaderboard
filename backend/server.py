from flask import Flask
from flask_socketio import SocketIO
from api.auth import auth_bp
from api.infor import infor_bp
from api.score_board import score_board_bp
from api.attendance import attendance_bp
from api.leaderboard import leaderboard_bp
from api.dashboard import dashboard_bp
from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)
socketio = SocketIO(app)
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(infor_bp, url_prefix='/api/infor')
app.register_blueprint(leaderboard_bp, url_prefix='/api/leaderboard')
app.register_blueprint(score_board_bp, url_prefix='/api/score_board')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

if __name__ == '__main__':
    socketio.run(app,debug=True)