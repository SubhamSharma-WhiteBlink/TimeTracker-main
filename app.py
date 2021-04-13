from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketIO = SocketIO(app, cors_allowed_origins="*")


@socketIO.on('time')
def handle_timestamp(data):
    print(data)


if __name__ == '__main__':
    socketIO.run(app)
