from FacultyDoorSensor.client_side import ClientSideDoorStatus, DoorState
import random


class MockClientSideDoorStatus(ClientSideDoorStatus):
    def __init__(self):
         super().__init__()
         self.choices = ['CLOSED', 'OPEN']


    # Override the function we want to mock
    def running_status(self):
        for door in self.doors:
            status = random.choice(self.choices)
            self.door_status[door] = status
        return self.door_status
