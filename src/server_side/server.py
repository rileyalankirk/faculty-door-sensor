
from flask import Flask, request
from door_status import DoorStatus
import logging

logging.basicConfig(filename='server_logs.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


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
            logging.warning("Door missing name argument in get_status!")
            return "No name given", 404
        logging.info('Attempting to get status of door: {}'.format(name))
        status = server.doors.get_status(name)
        logging.info('Received status of door: {}'.format(name))
        return status, 200
    except KeyError:
        logging.error('{} was not found in the system.'.format(name))
        return "Name not found", 400


@server.app.route('/is_door_name')
def is_door_name():
    try:
        name = request.args['name']
        return str(server.doors.is_door_name(name))
    except KeyError:
        return "No name given", 404


logging.info('Initializing server...')
if __name__ == '__main__':
    logging.info('Server beginning to run...')
    server.app.run(host='0.0.0.0', debug=False)
    logging.info('Server successfully stopped.')


