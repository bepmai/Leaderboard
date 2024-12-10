from flask import Flask
from api.auth import auth_bp
from api.infor import infor_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(infor_bp, url_prefix='/api/infor')

if __name__ == '__main__':
    app.run(debug=True)
