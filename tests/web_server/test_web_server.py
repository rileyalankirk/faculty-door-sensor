from add_data import add_data
from bs4 import BeautifulSoup
from FacultyDoorSensor.client_side import collect_data, create_server, WebServer
from mock_door_status import MockClientSideDoorStatus


def setup_test():
    # Create a server for testing
    server = WebServer()
    server.doors_status = MockClientSideDoorStatus()
    server = create_server(server)
    # Put the server into testing mode
    server.app.config['TESTING'] = True
    return server, server.app.test_client()


def test_website():
    # Get a test server and mock client
    server, client = setup_test()

    # Make get request to root endpoint
    result = client.get('/')

    # Make sure a webpage was successfully returned before converting the page into a soup object
    assert result.status_code == 200
    soup = BeautifulSoup(result.data, features='html.parser')

    # Select the style tag and split on # to get strings that contain each color.
    # The first item in the list does not contain a color.
    color_strings = soup.select_one('style').string.split('#')[1:]
    colors = []
    for color_string in color_strings:
        # Split the attribute name and color apart, second one is color, remove whitespace,
        # and remove the curly brace and beyond leaving us with the color
        colors.append(color_string.split(':')[1].strip().split('}')[0].lower())
    correct_colors = ['red', 'green', 'red', 'green']
    assert correct_colors == colors

    # Get the paragraph tags that contain the status for each door
    door_datas = soup.select('div .inner-div p')
    names, statuses = [], []
    for door_data in door_datas:
        # Split on colon to get a string containing the name and another that is the status
        name_string, status = door_data.getText().split(':')
        statuses.append(status)
        # Split off the "Dr. " start and the possessive "'s " to get the name
        names.append(name_string.split(' ')[1].split("'")[0].lower())
    correct_names = ['coleman', 'bush', 'schaper', 'mota']
    assert correct_names == names
    correct_statuses = ['CLOSED', 'OPEN', 'CLOSED', 'OPEN']
    assert correct_statuses == statuses

def test_get_stats():
    return # TODO: Remove when finished below todos

    # Get a test server and mock client
    server, client = setup_test()

    # Make get request to stats endpoint
    # TODO: need to mock out redis
    result = client.get('/stats')
    assert result.status_code == 200

    # TODO: finish testing stats endpoint

def test_get_data_no_params():
    # Get a test server and mock client
    server, client = setup_test()

    # Make get request to data endpoint
    result = client.get('/data')
    assert result.status_code == 400
    correct_response = 'Name parameter was missing'
    assert result.data.decode() == correct_response

def test_get_data_with_format_parameter():
    # Get a test server and mock client
    server, client = setup_test()

    # Make get request to data endpoint
    result = client.get('/data?format=normalized')
    assert result.status_code == 400
    correct_response = 'Name parameter was missing'
    assert result.data.decode() == correct_response

def test_get_data_with_name_parameter():
    # Get a test server and mock client
    server, client = setup_test()

    # Add data to redis database
    add_data(server.redis)

    # Make get request to data endpoint
    result = client.get('/data?name=coleman')
    assert result.status_code == 200
    # Test response
    correct_response = {'coleman': {'012': 10.0}}
    assert result.json == correct_response

    # Clear redis database
    server.redis.flushdb()

def test_get_data_with_name_and_format_parameters():
    # Get a test server and mock client
    server, client = setup_test()

    # Add data to redis database
    add_data(server.redis)

    # Make get request to data endpoint
    result = client.get('/data?name=coleman&format=normalized')
    assert result.status_code == 200
    # Test response
    correct_response = {'coleman': {'012': 100.0}}
    assert result.json == correct_response

    # Clear redis database
    server.redis.flushdb()
