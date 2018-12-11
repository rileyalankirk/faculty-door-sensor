
import requests
import json


def get_status(url):

    result = requests.get(url)
    door_status = json.loads(result.text)
    return door_status['state']


openHAB_IP = '10.76.100.166'
coleman_url = 'http://{}:8080/rest/items/ColemanDoor_BinarySensor'.format(openHAB_IP)
schaper_url = 'http://{}:8080/rest/items/SchaperDoor_BinarySensor'.format(openHAB_IP)
bush_url = 'http://{}:8080/rest/items/BushDoor_BinarySensor'.format(openHAB_IP)
mota_url = 'http://{}:8080/rest/items/MotaDoor_BinarySensor'.format(openHAB_IP)

urls = {'coleman': coleman_url,
        'schaper': schaper_url,
        'bush': bush_url,
        'mota': mota_url}


class DoorStatus:

    def get_status(self, name):

        if name not in urls and len(name) > 0:                 # Invalid Name
            return "Name not recognized: <" + name + ">";

        elif name == "":                                       # No name
            return "No name provided! Example: coleman";

        try:
            # Would we put the above if and elif right here?

            result = requests.get(urls[name])
            door_status = json.loads(result.text)

            if door_status['state'] != "CLOSED" and door_status['state'] != "OPEN":  # Valid Name, Door offline.
                return name + "'s door sensor is offline."

            else:
                return door_status['state']  # Valid Name, Valid Door Status

        except KeyError or TypeError:        # Generic Catch -- Do we need the try/except still?
            return                           # How will error codes and msg be together?

    def is_door_name(self, name):
        # Parameters passed at end of URL
        name = name.lower()
        f_in = open('config.txt', 'r')
        door_name = []
        for line in f_in:
            line = line.strip()
            door, link = line.split(',')
            door_name.append(door)
        f_in.close()

        if name in door_name:
            return True
        else:
            return False
