from flask import Flask
from api.auth import auth_bp
from api.infor import infor_bp
from api.score_board import score_board_bp
from api.attendance import attendance_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(infor_bp, url_prefix='/api/infor')
app.register_blueprint(score_board_bp, url_prefix='/api/score_board')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')

if __name__ == '__main__':
    app.run(debug=True)
