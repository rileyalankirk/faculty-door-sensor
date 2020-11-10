from datetime import datetime
from flask import Flask, request, render_template
from FacultyDoorSensor.client_side import ClientSideDoorStatus, DoorState, WebServer
from redis import Redis
from time import sleep
from threading import Thread
import logging


logging.basicConfig(filename='webserver.log', format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
THREAD_ALIVE = True

def create_server():
    '''Create server, add endpoints, and return the server'''
    server = WebServer()

    @server.app.route('/')
    def website():
        try:
            # Update door states and retrieve them
            with open('test.txt', 'r') as test:
                doors = [val.split(',') for val in test.read().split('\n')]
            door_status = [DoorState(name, status) for name, status in doors]
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

def collect_data():
    with open('test.txt', 'r') as test:
        doors = [val.split(',') for val in test.read().split('\n')]
    door_status = [DoorState(name, status) for name, status in doors]
    # server.doors_status.running_status()
    # door_status = server.doors_status.status_as_door_states()

    redis = Redis()
    last_save = datetime.now()
    while THREAD_ALIVE:
        for door_state in door_status:
            if door_state.status == 'OPEN':
                time = datetime.now()
                if (time - last_save).seconds > 60:
                    redis.save()
                    last_save = time
                weekday = time.weekday() # 0 - 6 (0 is Monday)
                redis.incrby(f'{door_state.name}{weekday}{time.hour}', 5)
        sleep(5)


if __name__ == '__main__':
    logging.info('Initializing server...')
    # Instantiate a server
    server = create_server()
    # Run the server
    logging.info('Server beginning to run...')
    thread = Thread(target=collect_data)
    thread.start()
    try:
        server.app.run(host='0.0.0.0', port=8080, debug=False)
    finally:
        THREAD_ALIVE = False
        thread.join()
        server.redis.save()
        logging.info('Server successfully stopped.')