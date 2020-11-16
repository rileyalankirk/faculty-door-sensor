from .add_data import add_data
import requests


def client():
    # Get door stats from server
    data = requests.get('localhost:8080')
    print(data)
    # Update data
    add_data()
    # Get updated door stats from server
    data = requests.get('localhost:8080')
    print(data)



if __name__ == '__main__':
    client()