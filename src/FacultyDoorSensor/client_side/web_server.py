from collections import defaultdict
from flask import Flask, jsonify, request, render_template
from FacultyDoorSensor.client_side import ClientSideDoorStatus
from redis import Redis
import logging


logging.basicConfig(filename='webserver.log', format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


class WebServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.doors_status = ClientSideDoorStatus()
        self.redis = Redis()


def create_server(server=WebServer()):
    '''Create server, add endpoints, and return the server'''

    def update_door_states():
        '''Update door states and retrieve them'''
        server.doors_status.running_status()
        return server.doors_status.status_as_door_states()
    
    def normalize_data(data):
        '''Normalizes data relative to each weekday'''
        sum_data = defaultdict(float, 0)
        # Sum all data
        for hour in data:
            day = hour[0]
            sum_data[day] += data[hour]
        # Normalize data as percentages
        for hour in data:
            day = hour[0]
            data[hour] /= sum_data[day]/100
        return data

    def retrieve_data(name):
        '''Retrieves redis data and converts its keys and values from bytestrings to strings and floats'''
        new_data = {}
        data = server.redis.hgetall(name)
        for key in data:
            new_data[key.decode()] = float(data[key].decode())
        return new_data

    @server.app.route('/', methods=['GET'])
    def website():
        try:
            # Update door states and retrieve them
            door_status = update_door_states()
            # Capitalize names
            for door in door_status:
                door.name = door.name.capitalize()
            return render_template('index.html', doors=door_status), 200
        except IOError:
            logging.error('There was an issue when opening the base.html file.')
        except Exception:
            logging.error('An unexpected issue occurred while attempting to retrieve the website.')
        # Website will be rendered without data if there is an error
        return render_template('index.html'), 200

    @server.app.route('/data', methods=['GET'])
    def get_data():
        '''Return statistics in a json format'''
        # Update door states and retrieve them
        door_status = update_door_states()
        # Check arguments
        name = request.args.get('name', None)
        if name is None:
            return 'Name parameter was missing', 400
        else:
            door_exists_for_name = False
            for door in door_status:
                if name.lower() == door.name:
                    door_exists_for_name = True
                    door_status = door.name
                    break
            if not door_exists_for_name:
                return f'Door for {name.lower()} does not exist', 404
        # Formats: None = unchanged; normalized
        formats = ['none', 'normalized']
        data_format = request.args.get('format', None)
        data_format = str(data_format).lower()
        if data_format not in formats:
            return f'Format {data_format} does not exist', 400
        
        # Calculate statistics
        data = retrieve_data(door_status)
        if data_format == 'normalized':
            data = normalize_data(data)

        return jsonify({door_status: data}), 200

    @server.app.route('/stats', methods=['GET'])
    def stats():
        door_status = update_door_states()
        data = []
        for door in door_status:
            data.append(retrieve_data(door.name))

        return '', 200

    return server


if __name__ == '__main__':
    logging.info('Initializing server...')
    # Instantiate server
    server = create_server()
    # Run the server
    logging.info('Server beginning to run...')
    server.app.run(host='0.0.0.0', port=8080, debug=False)
    logging.info('Server successfully stopped.')
