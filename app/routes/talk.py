from flask import Blueprint,request
from ..socket import socketio
from flask_socketio import emit
chat_bp=Blueprint('chat',__name__)

@socketio.on('message')
def handle_message(msg):
    print("----------------------------------------------------->")
    print("msg received",type(msg))