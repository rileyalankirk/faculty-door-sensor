import requests
import time

openHAB_IP = '10.76.100.166'
mock_get_status_url = 'http://0.0.0.0:5000/get_status?name='
mock_is_door_name_url = 'http://0.0.0.0:5000/is_door_name?name='
get_status_url = 'http://10.76.100.166:8080/get_status?name='
is_door_name_url = 'http://10.76.100.166:8080/is_door_name?name='


class ClientSideDoorSensor:

    def get_status(self, url):
        result = requests.get(url)
        return result.text  # The edge

    def is_door_name(self, url):
        result = requests.get(url)
        return result.text  # The edge, convert back to boolean

    def running_status(self):
        door_status = {}
        dct = {}
        infile = open('config.txt', 'r')
        for door_name in infile:
            if self.is_door_name(mock_is_door_name_url + door_name):
                door_name = door_name.strip()
                door_status[door_name] = mock_get_status_url + door_name
        infile.close()

        for door in door_status:
            status = self.get_status(door_status[door])
            dct[door] = status
        return dct
