import requests
import os


openHAB_IP = '172.31.228.44' # oldOpenHAB_IP = '10.76.100.166'
base_url = f'http://{openHAB_IP}:5000/'
get_status_url = base_url + 'get_status?name='
is_door_name_url = base_url + 'is_door_name?name='


class DoorState():
    def __init__(self, name, status):
        self.name = name
        if status in ['CLOSED', 'OPEN']:
            self.status = status
            self.color = 'red' if status == 'CLOSED' else 'green'
        else:
            self.status = 'NULL'
            self.color = 'orange'


class ClientSideDoorStatus:
    def __init__(self):
        self.doors = []
        self.door_status = {}
        self.load_config()

    def load_config(self):
        path = os.path.realpath('config.txt')
        with open(path, 'r') as config:
            for door in config:
                door = door.strip()
                self.doors.append(door)
                self.door_status[door] = 'NULL'

    def running_status(self):
        for door in self.doors:
            status = requests.get(get_status_url + door).text
            self.door_status[door] = status
        return self.door_status

    def status_as_door_states(self, status=None):
        new_status = []
        if status == None:
            status = self.door_status
        for name, state in status.items():
            new_status.append(DoorState(name, state))
        return new_status
