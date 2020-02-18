from server import server
from mock_door_status import MockDoorStatus

# TODO: test_no_name & test_bad_url


def test_valid_door_door_online():
    # Put the server into testing mode
    server.app.config['TESTING'] = True
    # Get a mock client
    client = server.app.test_client()

    # Mock out the status object
    server.doors = MockDoorStatus({'schaper': "OPEN"})

    # Use the test client to get a value
    result = client.get('/get_status?name=schaper')
    # Flask returns data as a byte-string (ASCII, not Unicode)

    assert result.data == b"OPEN"
    assert result.status_code == 200


def test_invalid_name():
    # Put the server into testing mode
    server.app.config['TESTING'] = True
    # Get a mock client
    client = server.app.test_client()

    # Mock out the status object
    server.doors = MockDoorStatus({'schaper': "OPEN"})

    result = client.get('/get_status?name=NOONE')
    assert result.data == b'Name not found'
    assert result.status_code == 404


def test_no_name():
    # Put the server into testing mode
    server.app.config['TESTING'] = True
    # Get a mock client
    client = server.app.test_client()

    # Mock out the status object
    server.doors = MockDoorStatus({'schaper': "NULL"})

    # Think this is 400 because of syntax error in querying url
    result = client.get('/get_status')

    assert str(result.data) == "No name given"
    assert result.status_code == 404


def test_bad_url():
    # Put the server into testing mode
    server.app.config['TESTING'] = True
    # Get a mock client
    client = server.app.test_client()

    # Mock out the status object
    server.doors = MockDoorStatus({'schaper': "NULL"})

    result = client.get('/get_some_door_status_for_me/')

    assert result.data == b"404 Error: Wrong url"
    assert result.status_code == 200


def test_door_offline():
    # Put the server into testing mode
    server.app.config['TESTING'] = True
    # Get a mock client
    client = server.app.test_client()

    # Mock out the status object
    server.doors = MockDoorStatus({'schaper': "NULL"})

    result = client.get('/get_status?name=schaper')

    assert result.data == b"NULL"
    assert result.status_code == 200
    # 404


def test_extra_param():
    # Put the server into testing mode
    server.app.config['TESTING'] = True
    # Get a mock client
    client = server.app.test_client()

    # Mock out the status object
    server.doors = MockDoorStatus({'schaper': "OPEN", 'coleman': 'OPEN'})

    result = client.get('/get_status?name=schaper&name=coleman')  # is this the correct way to check extra param?

    # Flask returns data as a byte-string (ASCII, not Unicode)
    assert result.data == b"OPEN"
    assert result.status_code == 200


def test_is_door_name_true():
    # Put the server into testing mode
    server.app.config['TESTING'] = True
    # Get a mock client
    client = server.app.test_client()

    # Try to read door list for name parameter
    result = client.get('/is_door_name?name=schaper')
    print(result.data)

    assert result.data == b"True"
    assert result.status_code == 200


def test_is_door_name_false():
    # Put the server into testing mode
    server.app.config['TESTING'] = True
    # Get a mock client
    client = server.app.test_client()

    # Try to read door list for name parameter
    if client.get('/is_door_name?name=talbot'):
        result_value = True

    assert result_value is True
