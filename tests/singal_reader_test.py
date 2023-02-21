from atamate_test import signal_reader


def test_handle_message_heartbeat():
    msg = b'\x00\x31\x00\x01'
    assert signal_reader._handle_message(msg) == 'Received HEARTBEAT message from circuit board: 1'


def test_handle_message_reading():
    msg = b'\x00\x21\x00\x01\x00\x01\x00\x40\x01\xf4'
    assert signal_reader._handle_message(msg) == '''Received READINGS message from circuit board: 1
- Number of readings: 1
Sensor 64, reads: 500 (units)'''
    msg = b'\x00\x21\x00\x02\x00\x02\x00\x4a\x01\x90\x00\x66\x03\xe8'
    assert signal_reader._handle_message(msg) == '''Received READINGS message from circuit board: 2
- Number of readings: 2
Sensor 74, reads: 400 (units)
Sensor 102, reads: 1000 (units)'''


def test_handle_message_not_bytes():
    msg = '\x00\x31\x00\x01'
    assert signal_reader._handle_message(msg) == 'Expected bytes, got <class \'str\'> instead'


def test_handle_message_no_board_id():
    msg = b'\x00\x31'
    assert signal_reader._handle_message(msg) == 'Malformed message: unpack requires a buffer of 4 bytes'


def test_handle_message_no_sensor_data():
    msg = b'\x00\x21\x00\x02\x00\x02'
    assert signal_reader._handle_message(msg) == 'Malformed message: no sensor data found'


def test_handle_message_wrong_reading_count():
    msg = b'\x00\x21\x00\x02\x00\x02\x00\x4a\x01\x90'
    assert signal_reader._handle_message(msg) == 'Malformed message: expected sensor reading count does not match actual'


def test_handle_message_wrong_reading_size():
    msg = b'\x00\x21\x00\x02\x00\x02\x00\x4a\x01\x90\x00\x66\x03'
    assert signal_reader._handle_message(msg) == 'Malformed message: sensor data is wrong size'


def test_handle_message_wrong_sensor_value():
    msg = b'\x00\x21\x00\x02\x00\x02\x00\x4a\x01\x90\x00\x66\x03\xe9'
    assert signal_reader._handle_message(msg) == '''Received READINGS message from circuit board: 2
- Number of readings: 2
Sensor 74, reads: 400 (units)
Wrong value on sensor 102: 1001'''


def test_handle_message_unknown_code():
    msg = b'\x00\x41\x00\x01'
    assert signal_reader._handle_message(msg) == 'Unrecognized message code'