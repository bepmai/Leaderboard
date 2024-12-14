from flask import Flask,render_template
from flask_socketio import SocketIO,emit, join_room, leave_room
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

@app.route('/')
def index():
    return render_template('sign-in.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/dashboarduser')
def dashboarduser():
    return render_template('dashboarduser.html')
@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/ranking')
def ranking():
    return render_template('Ranking.html')
@app.route('/attendance')
def attendance():
    return render_template('attendance.html')
@app.route('/attendanceuser')
def attendanceuser():
    return render_template('attendance-socreBoard-user.html')
@app.route('/scoreboard')
def scoreboard():
    return render_template('score-board.html')

users_rooms = {}
@socketio.on('join')
def on_join(data):
    msv = data['msv']
    room = f"{msv}"
    join_room(room)
    users_rooms[msv] = msv
    print(f"{msv} has entered the room")

@socketio.on('leave')
def on_leave(data):
    msv = data['msv']
    leave_room(users_rooms.get(msv, ""))
    del users_rooms[msv]
    print(f"{msv} has left the room")

if __name__ == '__main__':
    socketio.run(app,debug=True)