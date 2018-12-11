from door_status import DoorStatus


class MockDoorStatus:

    def __init__(self, states):
        self.states = states
        self.doors = DoorStatus()

    def get_status(self, name):
        return self.states[name]

    def is_door_name(self, name):
        return self.doors.is_door_name(name)
