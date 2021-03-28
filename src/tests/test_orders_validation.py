from services.checkers import orders_validation
import pytest

data_to_test = [
    ({
         'data':
             [{'order_id': 1,  # в базе уже существует (для тестов) заказ и курьер с id 1
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 0

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, True  # 1

    ),
    ({
         'data':
             [{'order_id': 99999999999999999999999999999999999999999999,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 3

    ),
    ({
         'data':
             [{'order_id': '99',
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 4

    ),
    ({
         'data':
             [{'order_id': None,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 5

    ),
    ({
         'data':
             [{'order_id': [99],
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 6

    ),
    ({
         'data':
             [{'order_id': 99.0,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 7

    ),
    ({
         'data':
             [{'order_id': 99,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 8

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.001,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 9

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 100.01,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 10

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 1,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 11

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': None,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 12

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 1.1111111111111111111,
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 13

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': [0.01],
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 14

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': '0.01',
               'region': 1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 15

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 16

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 111111111111111111111111111111111111111111,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 17

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1.1,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 18

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': '1',
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 19

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': [1],
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 20

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 0,
               'delivery_hours': ['11:00-13:00', '14:00-15:00']}]}, False  # 21

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1}]}, False  # 22

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': []}]}, False  # 23

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': '11:00-13:00'}]}, False  # 24

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': None}]}, False  # 25

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': {'11:00-13:00': '14:00-15:00'}}]}, False  # 26

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-11:00', '14:00-15:00']}]}, False  # 27

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-08:00', '14:00-15:00']}]}, False  # 28

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:01-11:00', '14:00-15:00']}]}, False  # 29

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-13:78', '14:00-15:00']}]}, False  # 30

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-55:00', '14:00-15:00']}]}, False  # 31

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['11:00-f3:00', '14:00-15:00']}]}, False  # 32

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['1:30-2:30', '14:00-15:00']}]}, False  # 33

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['1:30-2:30', '14:00-15:00'],
               'key': 'value'}]}, False  # 34

    ),
    ({
         'data':
             [{'order_id': 99,
               'weight': 0.01,
               'region': 1,
               'delivery_hours': ['1:30-2:30', '14:00-15:00']}],
         'key': 'value'}, False  # 35

    ),
    ({
         'data':
             {'order_id': 99,
              'weight': 0.01,
              'region': 1,
              'delivery_hours': ['1:30-2:30', '14:00-15:00']}}, False  # 36

    ),
    ({
         'data':
             []}, False  # 37

    ),
    ({
         'data':
             {}}, False  # 38

    ),
    ({
         'data':
             1}, False  # 39

    ),
    ({
         'data':
             'butt'}, False  # 40

    ),
    ({
         'data':
             None}, False  # 41

    ),
    ([
         'data', 'butt'], False  # 42

    ),
    ([], False),  # 43
    ({}, False),  # 44
]


@pytest.mark.parametrize('orders_data, result', data_to_test)
def test_orders_validation(orders_data, result):
    assert orders_validation(orders_data)[0] == result
