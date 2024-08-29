from flask import Blueprint,jsonify,request
from flask_socketio import SocketIO,emit

chat_bp =Blueprint('chat',__name__)
socketio=None

@chat_bp.before_app_first_request
def setup_socket():
    global socketio
    from app import socketio
    socketio.on_event('message',handle_message)
    socketio.on_event('connect', handle_connect)


def handle_message(data):
    emit('response',{'data':data['message']},broadcast=True)

def handle_connect():
    emit('response', {'data': 'User connected'}, broadcast=True)



@chat_bp.route('/send', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    if message:
        socketio.emit('message', {'message': message})
        return jsonify({'status': 'Message sent'}), 200
    return jsonify({'error': 'Message is required'}), 400

@chat_bp.route('/receive', methods=['GET'])
def receive_message():
    # This endpoint assumes you have some way to track messages.
    # In a real application, you might need to implement a system to store and fetch messages.
    # This is a placeholder for demonstration purposes.
    return jsonify({'message': 'This would return a list of received messages.'})



