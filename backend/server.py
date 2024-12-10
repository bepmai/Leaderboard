from flask import Flask
from api.auth import auth_bp
from api.infor import infor_bp
from api.score_board import score_board_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(infor_bp, url_prefix='/infor')
app.register_blueprint(score_board_bp, url_prefix='/score_board')

if __name__ == '__main__':
    app.run(debug=True)
