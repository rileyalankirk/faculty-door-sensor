import requests
import os


class DoorStatus:
    def __init__(self):
        self.doors = []
        self.door_urls = {}
        self.load_config()
    
    def load_config(self):
        path = os.path.realpath('config.txt')
        with open(path, 'r') as config:
            for line in config:
                door, link = line.strip().lower().split(',')
                self.door_urls[door] = link
                self.doors.append(door)

    def get_status(self, name):
        """Get status of provided name"""
        # Invalid name
        if name == '':
            return "Name was not provided"
        if name not in self.door_urls:
            return "Name not recognized: <{}>".format(name)
        try:
            result = requests.get(self.door_urls[name])
            door_status = result.get_json()
            # Valid name, door is offline
            if door_status['state'] != "CLOSED" and door_status['state'] != "OPEN":
                return name + "'s door sensor is offline"
            else:
                return door_status['state']  # Valid name and door status
        # Generic exception catch
        except KeyError or TypeError:
            return

    def is_door_name(self, name):
        # Check if the name exists
        return name.lower() in self.doors