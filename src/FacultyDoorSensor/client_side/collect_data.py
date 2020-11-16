from datetime import datetime
from FacultyDoorSensor.client_side import ClientSideDoorStatus
from redis import Redis
from time import sleep


def collect_data(redis):
    # Create door status client
    doors_status = ClientSideDoorStatus()

    last_save = datetime.now()
    prev_incr = {}
    while True:
        # Save redis every hour
        now = datetime.now()
        if (now - last_save).seconds > 3600:
            redis.save()
            last_save = now
        # Update door states and retrieve them
        doors_status.running_status()
        door_status = doors_status.status_as_door_states()
        # For each door, if door is open add the time it has been open to the total
        for door_state in door_status:
            now = datetime.now()
            if door_state.status == 'OPEN':
                weekday = now.weekday() # 0 - 6 (0 is Monday)
                if door_state.name not in prev_incr:
                    prev_incr[door_state.name] = datetime.now()
                time_open = (now - prev_incr[door_state.name]).total_seconds()
                redis.hincrbyfloat(door_state.name, f'{weekday}{now.hour}', time_open)
            prev_incr[door_state.name] = now
        sleep(5)


if __name__ == "__main__":
    redis = Redis()
    try:
        collect_data(redis)
    except Exception:
        # Save redis if an unknown exception occurs
        redis.save()
