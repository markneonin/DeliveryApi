from services.checkers import assign_checker
import pytest

data_to_test = [
    ({'courier_id': 1}, True),
    ({'courier_id': 99}, False),
    ({'courier_id': 9999999999999999999999999999}, False),
    ({'courier_id': '1'}, False),
    ({'courier_id': None}, False),
    ({'courier_id': 1, 'key': 'value'}, False),
    ({}, False),
    ([], False),
    ({'key': 'value'}, False),
]


@pytest.mark.parametrize('assign_data, result', data_to_test)
def test_assign_checker(assign_data, result):
    assert assign_checker(assign_data, )[0] == result
