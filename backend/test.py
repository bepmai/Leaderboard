from flask import Flask, render_template
from flask_socketio import SocketIO, send

# Tạo ứng dụng Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Khởi tạo SocketIO
socketio = SocketIO(app)

# Xử lý sự kiện khi client gửi tin nhắn
@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    send(f"Server echo: {msg}", broadcast=True)  # Gửi lại tin nhắn cho tất cả các client

@app.route('/')
def index():
    return render_template('index.html')  # Render trang HTML chứa client WebSocket

if __name__ == '__main__':
    socketio.run(app, debug=True)
