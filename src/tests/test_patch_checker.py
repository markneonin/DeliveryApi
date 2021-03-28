from services.checkers import patch_checker
import pytest

data_to_test = [
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01']}, 1, True
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01']}, 10, False
     ),
    ({'courier_type': None,
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': 'bi',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': ['bike'],
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': 1,
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1111111111111111111111111111111111111111111, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [],
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': None,
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': ['1, 2, 3, 4, 5, 6'],
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, '2', 3, 4, 5, 6],
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2.0, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 0, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 1, 1, 1, 1, 1],
      'working_hours': ['00:00-00:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': []}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': None}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': '00:00-00:01'}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': [{'00:00-00:01': 1}]}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:00']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['10:00-00:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['10:02-10:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:66']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-55:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['0:00-0:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:j0-00:01']}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01', 0]}, 1, False
     ),
    ({}, 1, False
     ),
    ({'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01'],
      'key':'value'}, 1, False
     ),
    ([{'courier_type': 'bike',
      'regions': [1, 2, 3, 4, 5, 6],
      'working_hours': ['00:00-00:01']}], 1, False
     ),

]


@pytest.mark.parametrize('patch_data, courier_id, result', data_to_test)
def test_patch_checker(patch_data, courier_id, result):
    assert patch_checker(patch_data, courier_id)[0] == result
