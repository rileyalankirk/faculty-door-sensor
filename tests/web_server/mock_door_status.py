from FacultyDoorSensor.client_side import ClientSideDoorStatus, DoorState
import os


class MockClientSideDoorStatus(ClientSideDoorStatus):
    def __init__(self):
         super().__init__()

    # Override the function we want to mock
    def running_status(self):
        path = os.path.realpath('mock_status.txt')
        with open(path, 'r') as config:
            for door in config:
                door, status = door.strip().split(',')
                self.door_status[door] = status
        return self.door_status
