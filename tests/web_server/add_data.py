from datetime import datetime
import random


def add_data(redis):
    names = ['bush', 'coleman', 'schaper', 'mota']
    choices = ['CLOSED', 'OPEN']
    for name in names:
        redis.hincrbyfloat(name, f'012', 10)
