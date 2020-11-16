from FacultyDoorSensor.client_side import collect_data, create_server
from mock_door_status import MockDoorStatus



def setup_test():
    # Create a server for testing
    server = create_server()
    # Put the server into testing mode
    server.app.config['TESTING'] = True
    return server, server.app.test_client()

def test_example():
    # Get a test server and mock client
    server, client = setup_test()

    # Use the test client to get a value
    result = client.get('/')

    assert result.status_code == 200

# TODO: Write tests...