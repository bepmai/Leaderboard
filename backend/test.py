from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__,template_folder="templates1")
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app,cors_allowed_origins="*")

# Lưu trữ thông tin người dùng và phòng của họ
users_rooms = {}

# Khi người dùng kết nối
@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")
@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnect: {request.sid}")

# Khi người dùng gửi tin nhắn
@socketio.on('send_message')
def handle_message(data):
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message = data['message']

    print(f"Received message from {sender_id} to {receiver_id}: {message}")

    # Kiểm tra nếu người nhận có kết nối
    if receiver_id in users_rooms:
        receiver_room = users_rooms[receiver_id]
        # Gửi tin nhắn đến phòng của người nhận
        emit('receive_message', {
            'sender_id': sender_id,
            'message': message
        }, room=receiver_room)
    
    # Gửi tin nhắn đến phòng của người gửi (nếu muốn người gửi cũng thấy tin nhắn của mình)
    if sender_id in users_rooms:
        sender_room = users_rooms[sender_id]
        emit('receive_message', {
            'sender_id': sender_id,
            'message': message
        }, room=sender_room)

# Khi người dùng tham gia vào một phòng (để nhận tin nhắn)
@socketio.on('join')
def on_join(data):
    user_id = data['user_id']
    room = f"room_{user_id}"
    join_room(room)
    users_rooms[user_id] = room
    print(f"{user_id} has entered the room")

# Khi người dùng rời khỏi phòng
@socketio.on('leave')
def on_leave(data):
    user_id = data['user_id']
    leave_room(users_rooms.get(user_id, ""))
    del users_rooms[user_id]
    print(f"{user_id} has left the room")

@app.route('/')
def index():
    return render_template('index.html')  # Giao diện web

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4000, debug=True)
