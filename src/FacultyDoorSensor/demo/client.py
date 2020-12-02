from add_data import add_data
import requests


def client():
    names = ['coleman', 'bush', 'schaper', 'mota']
    url = 'http://localhost:8080/data?name='
    # Get door stats from server
    print('Original Data\n')
    for name in names:
        data = requests.get(f'{url}{name}')
        print(data.text, end='')
    # Update data
    add_data()
    # Get updated door stats from server
    print('\nUpdated Data\n')
    for name in names:
        data = requests.get(f'{url}{name}')
        print(data.text, end='')


if __name__ == '__main__':
    client()
