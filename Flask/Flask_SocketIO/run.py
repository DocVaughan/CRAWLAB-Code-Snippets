#!flask/bin/python
from app import app
from flask.ext.socketio import SocketIO

socketio = SocketIO(app)

socketio.run(app)
