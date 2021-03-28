from services.checkers import couriers_validation
import pytest

data_to_test = [
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-23:00']}]}, True),  # 0
    ({
         'data':
             [{'courier_id': 1,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-23:00']}]}, False),  # 1
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'caar',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-23:00']}]}, False),  # 2
    ({
         'data':
             [{'courier_id': '10',
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-23:00']}]}, False),  # 3
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': ['car'],
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-23:00']}]}, False),  # 4
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6]
               }]}, False),  # 5
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'working_hours': ['00:00-23:00']}]}, False),  # 6
    ({
         'data':
             [{'courier_id': 10,
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-23:00']}]}, False),  # 7
    ({
         'data':
             [{
                 'courier_id': -5,
                 'courier_type': 'car',
                 'regions': [1, 2, 3, 4, 5, 6],
                 'working_hours': ['00:00-23:00']}]}, False),  # 8
    ({
         'data':
             [{'courier_id': None,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-23:00']}]}, False),  # 9
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': None,
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-23:00']}]}, False),  # 10
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [],
               'working_hours': ['00:00-23:00']}]}, False),  # 11
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, '2', 3, 4, 5, 6],
               'working_hours': ['00:00-23:00']}]}, False),  # 12
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, -1, 3, 4, 5, 6],
               'working_hours': ['00:00-23:00']}]}, False),  # 13
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5.0, 6],
               'working_hours': ['00:00-23:00']}]}, False),  # 14
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': {1: 2},
               'working_hours': ['00:00-23:00']}]}, False),  # 15
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': '1, 2, 3, 4, 5, 6',
               'working_hours': ['00:00-23:00']}]}, False),  # 16
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': None}]}, False),  # 17
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': []}]}, False),  # 18
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': {'00:00-23:00': 1}}]}, False),  # 19
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-3:00']}]}, False),  # 20
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-23:68']}]}, False),  # 21
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['23:00-22:00']}]}, False),  # 22
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['22:00-22:00']}]}, False),  # 23
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['22:40-22:00']}]}, False),  # 24
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-23:00', '12:00']}]}, False),  # 25
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-22:00'],
               'key': 'value'}]}, False),  # 26
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-22:00']}],
         'key': 'value'}, False),  # 27
    ({}, False),  # 28

    ({
         'data':
             {'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-22:00']}}, False),  # 29

    ({
         'dat':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-22:00']}]}, False),  # 30
({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-22:00']}, 'butt']}, False),  # 31
({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-22:00']}, {}]}, False),  # 32
({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-22:00']}, []]}, False),  # 33
({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-22:00']}, None]}, False),  # 34
({
         'data':
             []}, False),  # 35
({
         'data':
             [{'courier_id': 1000000000000000000000000000000000000,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-22:00']}]}, False),  # 36
({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [10000000000000000000000000000000000000, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-22:00']}]}, False),  # 37
({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 1, 1, 1, 1, 1],
               'working_hours': ['00:00-22:00']}]}, False),  # 38
    ({
         'data':
             [{'courier_id': 10,
               'courier_type': 'car',
               'regions': [1, 2, 3, 4, 5, 6],
               'working_hours': ['00:00-53:59']}]}, False),  # 39
    ({
         'data': None}, False),  # 40
    ({
         'data': []}, False),  # 41

    ({
         'data': {}}, False),  # 42
    ({
         'data': 'butt'}, False),  # 43
    ({
         'data': 1}, False),  # 44
    ({
         'data': {'key': 'value'}}, False),  # 45
    ({}, False),  # 46
    (['data'], False),  # 47
    ([], False),  # 48




]


@pytest.mark.parametrize('couriers_data, result', data_to_test)
def test_couriers_validation(couriers_data, result):
    assert couriers_validation(couriers_data)[0] == result
