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

def test_website_no_params():
    # Get a test server and mock client
    server, client = setup_test()

    # Use the test client to get a value
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


# TODO: Write tests...
    # endpoints with no params
    # endpoints with bad params
    # endpoints with good params
    # test that values in html are correct
    # test nonexistent endpoints