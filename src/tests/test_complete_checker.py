from services.checkers import complete_checker
import pytest

data_to_test = [
    ({
         'courier_id': 1,
         'order_id': 1,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, True),
    ({
         'order_id': 1,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': 1111111111111111111111111111111111111,
         'order_id': 1,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': -1,
         'order_id': 1,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': 1.0,
         'order_id': 1,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': None,
         'order_id': 1,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': [1],
         'order_id': 1,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': '1',
         'order_id': 1,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': [],
         'order_id': 1,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': 1,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': 1,
         'order_id': -2,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': 1,
         'order_id': 999999999999999999999999999999999999999999999999999,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': 1,
         'order_id': None,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': 1,
         'order_id': 1.0,
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': 1,
         'order_id': [1],
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': 1,
         'order_id': '1',
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': 1,
         'order_id': [],
         'complete_time': '2022-03-28T17:51:38.53Z'
     }, False),
    ({
         'courier_id': 1,
         'order_id': 1,
     }, False),
    ({
         'courier_id': 1,
         'order_id': 1,
         'complete_time': '2020-03-28T12:51:38.53Z'
     }, False),
    ({
         'courier_id': 1,
         'order_id': 1,
         'complete_time': ['2022-03-28T17:51:38.53Z']
     }, False),
    ({
         'courier_id': 1,
         'order_id': 1,
         'complete_time': '202103sdgsdgsdgsdg'
     }, False),
    ({
         'courier_id': 1,
         'order_id': 1,
         'complete_time': None
     }, False),
    ({
         'courier_id': 1,
         'order_id': 1,
         'complete_time': 0
     }, False),
    ({
         'courier_id': 1,
         'order_id': 1,
         'complete_time': []
     }, False),
    ({
         'courier_id': 1,
         'order_id': 1,
         'complete_time': '2022-03-28T17:51:38.53Z',
         'key': 'value'
     }, False),
    ({}, False),
    ([], False),
    (1, False),
]


@pytest.mark.parametrize('complete_data, result', data_to_test)
def test_complete_checker(complete_data, result):
    assert complete_checker(complete_data, )[0] == result
