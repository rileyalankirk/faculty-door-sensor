
from flask import Flask, request
from door_status import DoorStatus


class Server:

    def __init__(self):
        self.app = Flask(__name__)
        self.doors = DoorStatus()


# Instantiating a server variable using the Server class.
server = Server()


@server.app.route('/get_status')
def get_status():
    # Parameters are passed at the end of the URL as ?key=foo
    try:
        name = request.args['name']
        if name is None:
            return "No name given", 404
        return server.doors.get_status(name), 200
    except KeyError:
        return "Name not found", 400


@server.app.route('/is_door_name')
def is_door_name():
    try:
        name = request.args['name']
        return str(server.doors.is_door_name(name))
    except KeyError:
        return "No name given", 404


if __name__ == '__main__':
    server.app.run(host='0.0.0.0', debug=True)
