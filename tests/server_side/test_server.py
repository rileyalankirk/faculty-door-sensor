from FacultyDoorSensor.server_side import create_server
from mock_door_status import MockDoorStatus


# TODO: test_no_name & test_bad_url


def setup_test():
    # Create a server for testing
    server = create_server()
    # Put the server into testing mode
    server.app.config['TESTING'] = True
    return server, server.app.test_client()


def test_valid_door_door_online():
    # Get a test server and mock client
    server, client = setup_test()

    # Mock out the status object
    server.doors_status = MockDoorStatus({'schaper': 'OPEN'})

    # Use the test client to get a value
    result = client.get('/get_status?name=schaper')
    # Flask returns data as a byte-string (ASCII, not Unicode)

    assert result.data == b'OPEN'
    assert result.status_code == 200


def test_invalid_name():
    # Get a test server and mock client
    server, client = setup_test()

    # Mock out the status object
    server.doors_status = MockDoorStatus({'schaper': 'OPEN'})

    result = client.get('/get_status?name=NOONE')
    assert result.data == b'Name not found'
    assert result.status_code == 404


def test_no_name():
    # Get a test server and mock client
    server, client = setup_test()

    # Mock out the status object
    server.doors_status = MockDoorStatus({'schaper': 'NULL'})

    result = client.get('/get_status')

    assert result.data == b'No name given'
    assert result.status_code == 400


def test_bad_url():
    # Get a test server and mock client
    server, client = setup_test()

    # Mock out the status object
    server.doors_status = MockDoorStatus({'schaper': 'NULL'})

    result = client.get('/get_some_door_status_for_me/')

    # Endpoint does not exist so we get a 404
    assert result.status_code == 404


def test_door_offline():
    # Get a test server and mock client
    server, client = setup_test()

    # Mock out the status object
    server.doors_status = MockDoorStatus({'schaper': 'NULL'})

    result = client.get('/get_status?name=schaper')

    assert result.data == b'NULL'
    assert result.status_code == 200
    # 404


def test_extra_param():
    # Get a test server and mock client
    server, client = setup_test()

    # Mock out the status object
    server.doors_status = MockDoorStatus({'schaper': 'OPEN', 'coleman': 'CLOSED'})
    # Extra parameter is ignored 
    result = client.get('/get_status?name=schaper&name=coleman')

    # Flask returns data as a byte-string (ASCII, not Unicode)
    assert result.data == b'OPEN'
    assert result.status_code == 200


def test_is_door_name_true():
    # Get a test server and mock client
    server, client = setup_test()

    # Try to read door list for name parameter
    result = client.get('/is_door_name?name=schaper')

    assert result.data == b'True'
    assert result.status_code == 200


def test_is_door_name_false():
    # Get a test server and mock client
    server, client = setup_test()

    # Try to read door list for name parameter
    result = client.get('/is_door_name?name=talbot')
    
    assert result.data == b'False'
    assert result.status_code == 200
