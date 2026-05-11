from flask_socketio import emit

def register_socket_events(socketio):

    @socketio.on('task_update')
    def handle_task_update(data):

        emit(
            'receive_update',
            data,
            broadcast=True
        )