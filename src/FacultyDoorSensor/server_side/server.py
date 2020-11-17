from flask import Flask, request
from FacultyDoorSensor.server_side import DoorStatus
import logging

logging.basicConfig(filename='server_logs.log', format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.doors_status = DoorStatus()

def create_server():
    '''Create server, add endpoints, and return the server'''
    server = Server()

    @server.app.route('/get_status')
    def get_status():
        # Parameters are passed at the end of the URL as ?key=foo
        try:
            name = request.args.get('name', None)
            if name is None:
                logging.warning("Door missing name argument in get_status!")
                return "No name given", 400
            logging.info(f'Attempting to get status of door: {name}')
            status = server.doors_status.get_status(name)
            logging.info(f'Received status of door: {name}')
            return status, 200
        except KeyError:
            logging.error(f'{name} was not found in the system.')
            return "Name not found", 404


    @server.app.route('/is_door_name')
    def is_door_name():
        try:
            name = request.args.get('name', None)
            return str(server.doors_status.is_door_name(name))
        except KeyError:
            return "No name given", 404
    
    return server


if __name__ == '__main__':
    logging.info('Initializing server...')
    # Instantiate a server
    server = create_server()
    # Run the server
    logging.info('Server beginning to run...')
    server.app.run(host='0.0.0.0', debug=False)
    logging.info('Server successfully stopped.')


