from datetime import datetime
from redis import Redis
import random


def add_data():
    redis = Redis()
    names = ['bush', 'coleman', 'schaper', 'mota']
    choices = ['CLOSED', 'OPEN']
    now = datetime.now()
    weekday = now.weekday() # 0 - 6 (0 is Monday)
    hour = now.hour
    for name in names:
        redis.hincrbyfloat(name, f'{weekday}{hour}', 10*random.random())


if __name__ == "__main__":
    add_data()
