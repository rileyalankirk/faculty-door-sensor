
from flask import Flask, request
from door_status import DoorStatus
import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)

logging.info('Preparing to start server...')


class Server:

    def __init__(self):
        self.app = Flask(__name__)
        self.doors = DoorStatus()


server = Server()


@server.app.route('/get_status')
def get_status():
    # Parameters are passed at the end of the URL as ?key=foo
    try:
        name = request.args['name']
        logging.info('Attempting to get status of ' + name + ' door...')
        if name is None:
            return "No name given", 404
#       if page_not_found():
#            return "404 Error: Wrong url", 404
        logging.info('Received status of ' + name + '\'s door.')
        return server.doors.get_status(name), 200
    except KeyError:
        logging.error('Failed to receive status of ' + name + '\'s door.')
        return "Name not found", 400


@server.app.route('/is_door_name')
def is_door_name():
    try:
        name = request.args['name']
        logging.info('Validating ' + name + '\'s door...')
        return str(server.doors.is_door_name(name))
    except KeyError:
        return "No name given", 404


if __name__ == '__main__':
    server.app.run(host='0.0.0.0', debug=True)
    logging.info('Server successfully started.')
else:
    logging.critical('Server failed to start.')

