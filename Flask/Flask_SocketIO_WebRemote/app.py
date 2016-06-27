import time
import logging
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, disconnect, send

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, engineio_options={'logger': False})
thread = None

global x_velocity, y_velocity


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        count += 1
        emit('my response',
             {'data': 'Server generated event', 'count': count},
             namespace='/CRAWLAB')


@app.route('/')
def index():
#     global thread
#     if thread is None:
#         thread = Thread(target=background_thread)
#         thread.start()
    return render_template('index.html')

@app.route('/joystick')
def joystick():
    return render_template('joystick.html')

@app.route('/receiver')
def receive():
    return render_template('receiver.html')


@socketio.on('connections', namespace='/CRAWLAB')
def connections(message):
    logging.debug(message['data'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('velocity_commands', namespace='/CRAWLAB')
def receive_velocity(json):
    global x_velocity, y_velocity
    x_velocity = json['vel']['x']
    y_velocity = json['vel']['y']
    print('x_velocity = {}, y_velocity = {}\r\n'.format(x_velocity, y_velocity))

    # For now, just echo the sent velocities back, instead of real sensor data
    emit('sensor_data', {'data_x': x_velocity, 'data_y': y_velocity}, broadcast=True)


# @socketio.on('my broadcast event', namespace='/CRAWLAB')
# def test_broadcast_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     print(message['data'])
#     emit('my response',
#          {'data': message['data'], 'count': session['receive_count']},
#          broadcast=True)

# # No room based events yet
# @socketio.on('join', namespace='/CRAWLAB')
# def join(message):
#     join_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my response',
#          {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
#           'count': session['receive_count']})
# 
# 
# @socketio.on('leave', namespace='/CRAWLAB')
# def leave(message):
#     leave_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my response',
#          {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
#           'count': session['receive_count']})
# 
# 
# @socketio.on('close room', namespace='/CRAWLAB')
# def close(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
#                          'count': session['receive_count']},
#          room=message['room'])
#     close_room(message['room'])
# 
# 
# @socketio.on('my room event', namespace='/CRAWLAB')
# def send_room_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my response',
#          {'data': message['data'], 'count': session['receive_count']},
#          room=message['room'])


@socketio.on('disconnect request', namespace='/CRAWLAB')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/CRAWLAB')
def connect():
    emit('connect_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/CRAWLAB')
def disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
