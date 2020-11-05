from flask import Flask, request
from FacultyDoorSensor.client_side import ClientSideDoorStatus
import logging

logging.basicConfig(filename='server_logs.log', format='%(asctime)s %(levelname)-8s %(message)s',
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
            door_status = server.doors_status.running_status()
            with open('base.html', 'r') as html:
                text = html.read()
            head, divs, end = text.strip().split('\n\n')
            divs = divs.split('\n')
            for i, (name, status) in enumerate(door_status.items()):
                if status == 'CLOSED':
                    color = 'red'
                elif status == 'OPEN':
                    color = 'green'
                else:
                    color = 'orange'
                    status = 'NULL'
                divs[i].replace('---', color, 1)
                divs[i].replace('---', name, 1)
                divs[i].replace('---', status, 1)
            divs = '\n'.join(divs)
            website = f'{head}\n{divs}\n{end}'
            return website, 200
        except IOError:
            logging.error('There was an issue when opening the base.html file.')
        except Exception:
            logging.error('An unexpected issue occurred while attempting to retrieve the website.')
        return "Website not retrieved", 404
    
    return server


if __name__ == '__main__':
    logging.info('Initializing server...')
    # Instantiate a server
    server = create_server()
    # Run the server
    logging.info('Server beginning to run...')
    server.app.run(host='localhost', port=8080, debug=False)
    logging.info('Server successfully stopped.')


