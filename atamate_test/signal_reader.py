import struct

from dataclasses import dataclass


@dataclass
class MessageOptions:
    """Dataclass with options for message parsing
    """
    # possible codes
    code_heartbeat: int = 0x0031
    code_reading: int = 0x0021
    # structure format
    code_board_format: str = '>hh'
    reading_count_format: str = '>h'
    sensor_reading_format: str = '>hh'
    # can be moved to post_init if using class instances
    sensor_reading_size: int = struct.calcsize(sensor_reading_format)
    # message blocks positions
    code_board_start: int = 0
    code_board_end: int = 4
    reading_count_start: int = 4
    reading_count_end: int = 6
    sensor_reading_start: int = 6
    # allowed sensor reading values
    sensor_value_min: int = 0
    sensor_value_max: int = 1000


def _handle_message(message: bytes) -> str:
    """Parses message bytes and returns result or error

    Args:
        message (bytes): message

    Returns:
        str: parsed message or error string
    """
    # only bytes-like objects can be unpacked by struct.unpack
    if not isinstance(message, bytes):
        return f'Expected bytes, got {type(message)} instead'

    # if first part of the messages is malformed, including lack of board id, return error
    try:
        msg_code, board_id = struct.unpack(MessageOptions.code_board_format,
                                           message[MessageOptions.code_board_start:
                                                   MessageOptions.code_board_end])
    except struct.error as error:
        return f'Malformed message: {error}'

    # heartbeat message parsing — only checks the code
    if msg_code == MessageOptions.code_heartbeat:
        return f'Received HEARTBEAT message from circuit board: {board_id}'

    # readings message parsing
    elif msg_code == MessageOptions.code_reading:
        # too short of a message means lack of reading data, return error
        if len(message) <= MessageOptions.reading_count_end:
            return 'Malformed message: no sensor data found'

        # if counter part of the messages is malformed, return error
        try:
            reading_count, = struct.unpack(MessageOptions.reading_count_format,
                                           message[MessageOptions.reading_count_start:
                                                   MessageOptions.reading_count_end])
        except struct.error as error:
            return f'Malformed message: cannot unpack sensor reading count. {error}'

        sensor_data = message[MessageOptions.sensor_reading_start:]
        # readings part of the messages can't be split into format-correct chunks, return error
        if len(sensor_data) % MessageOptions.sensor_reading_size:
            return 'Malformed message: sensor data is wrong size'
        # readings part of the messages is not sized according to counter, return error
        elif reading_count != len(sensor_data)/MessageOptions.sensor_reading_size:
            return 'Malformed message: expected sensor reading count does not match actual'

        # if readings part of the messages is malformed, return error
        try:
            readings = [f'Received READINGS message from circuit board: {board_id}',
                        f'- Number of readings: {reading_count}']
            for sensor_id, sensor_value in struct.iter_unpack(MessageOptions.sensor_reading_format,
                                                              sensor_data):
                # invalid sensor value, return error
                if (sensor_value < MessageOptions.sensor_value_min or
                        sensor_value > MessageOptions.sensor_value_max):
                    readings.append(f'Wrong value on sensor {sensor_id}: {sensor_value}')
                else:
                    # collect all parsed messages in a single list
                    readings.append(f'Sensor {sensor_id}, reads: {sensor_value} (units)')
        except struct.error as error:
            return f'Malformed sensor readings: {error}'
        # join parsed messages into a single string & return
        return '\n'.join(readings)

    else:
        return 'Unrecognized message code'


def handle_message(message: bytes) -> None:
    """Prints parsed message

    Args:
        message (bytes): message
    """
    print(_handle_message(message))
