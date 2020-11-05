from flask import Flask, request, render_template
from FacultyDoorSensor.client_side import ClientSideDoorStatus
import logging


logging.basicConfig(filename='webserver.log', format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


class WebServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.doors_status = ClientSideDoorStatus()

def create_server():
    '''Create server, add endpoints, and return the server'''
    server = WebServer()

    @server.app.route('/')
    def website():
        try:
            # Update door states and retrieve them
            server.doors_status.running_status()
            door_status = server.doors_status.status_as_door_states()
            # Capitalize names
            for i in range(len(door_status)):
                door_status[i].name = door_status[i].name.capitalize()
            return render_template('index.html', doors=door_status), 200
        except IOError:
            logging.error('There was an issue when opening the base.html file.')
        except Exception:
            logging.error('An unexpected issue occurred while attempting to retrieve the website.')
        return render_template('index.html'), 200
    
    return server


if __name__ == '__main__':
    logging.info('Initializing server...')
    # Instantiate a server
    server = create_server()
    # Run the server
    logging.info('Server beginning to run...')
    server.app.run(host='0.0.0.0', port=8080, debug=False)
    logging.info('Server successfully stopped.')


