from datetime import datetime
from pydantic import ValidationError
import re

import database.dbworking as db
import models.request_models as rq_models


def couriers_validation(data):
    """
    Валидация данных курьеров

    Проверяет валидность данных курьеров в цикле, генерирует ответ клиенту

    Parameters:
    argument1 (Any): данные от клиента

    Returns:
    True OR False: результат проверки,
    dict: словарь готовый для упаковки в json
    List[request_models.Courier] OR None: лист объектов курьеров, если всё гуд

    """
    couriers_objects = []
    invalid_ids = []
    valid_ids = []
    messages = {}

    try:
        couriers_data = rq_models.CouriersData.parse_obj(data)
    except ValidationError as e:
        return False, {'validation_error': e.errors()[0]['msg']}, None

    if len(couriers_data.data) == 0:
        return False, {'validation_error': 'empty list of couriers'}, None

    for courier in couriers_data.data:
        try:

            c = rq_models.Courier.parse_obj(courier)
            couriers_objects.append(c)
            valid_ids.append({'id': c.courier_id})

        except ValidationError as e:

            if isinstance(courier, dict) and 'courier_id' in courier:
                courier_id = courier['courier_id']
            else:
                courier_id = '<unk>'

            invalid_ids.append({'id': courier_id})
            courier_id = 'courier_' + str(courier_id)
            messages[courier_id] = {}

            for err in e.errors():
                messages[courier_id][err['loc'][0]] = err['msg']

    if len(invalid_ids) == 0:
        return True, {'couriers': valid_ids}, couriers_objects
    else:
        return False, {'validation_error': {'couriers': invalid_ids, 'messages': messages}}, None


def orders_validation(data):
    """
    Валидация данных заказов

    Проверяет валидность данных заказов в цикле,

    Parameters:
    argument1 (Any): данные от клиента

    Returns:
    True OR False: результат проверки,
    dict: словарь готовый для упаков в json
    List[request_models.Order] OR None: лист объектов заказов, если всё гуд

    """
    orders_objects = []
    invalid_ids = []
    valid_ids = []
    messages = {}

    try:
        orders_data = rq_models.OrdersData.parse_obj(data)
    except ValidationError as e:
        return False, {'validation_error': e.errors()[0]['msg']}, None

    if len(orders_data.data) == 0:
        return False, {'validation_error': 'empty list of orders'}, None

    for order in orders_data.data:
        try:

            o = rq_models.Order.parse_obj(order)
            orders_objects.append(o)
            valid_ids.append({'id': o.order_id})

        except ValidationError as e:
            if isinstance(order, dict) and 'order_id' in order:
                order_id = order['order_id']
            else:
                order_id = '<unk>'

            invalid_ids.append({'id': order_id})
            order_id = 'order_' + str(order_id)
            messages[order_id] = {}

            for err in e.errors():
                messages[order_id][err['loc'][0]] = err['msg']

    if len(invalid_ids) == 0:
        return True, {'orders': valid_ids}, orders_objects
    else:
        return False, {'validation_error': {'orders': invalid_ids, 'messages': messages}}, None


def patch_checker(data, courier_id):
    is_courier_exist, _ = db.is_courier_exist(courier_id)
    if is_courier_exist:
        try:

            patch_data = rq_models.DataToPatch.parse_obj(data)
            return True, patch_data, None

        except ValidationError as e:
            out = {'messages': {}}

            for err in e.errors():
                out['messages'][err['loc'][0]] = err['msg']

            return False, None, out
    else:
        return False, None, {'messages': {'courier_' + str(courier_id): 'courier with this id does not exist'}}


def assign_checker(data):
    try:

        assign_data = rq_models.AssignData.parse_obj(data)
        return True, assign_data.courier_id, None

    except ValidationError as e:
        out = {'messages': {}}

        for err in e.errors():
            out['messages'][err['loc'][0]] = err['msg']

        return False, None, out


def complete_checker(data):
    """
    Валидация данных заверешения заказа

    Проверяет валидность данных по типам и значенияем, пытается найти доставку для этого курьера,
    для которой существует актуальное назначение этого заказа, статус которого "order_processing",
    если доставка найдена сравнивает время её создания со временем завершения заказа

    Parameters:
    argument1 (Any): данные от клиента

    Returns:
    True OR False: результат проверки,
    request_models.CompleteOrder OR None : объект данных для завершения, если всё гуд
    tables.Delivery OR None: объект доставки, если всё гуд
    None OR dict: словарь с ошибками, если всё не гуд

    """
    try:
        complete_data = rq_models.CompleteOrder.parse_obj(data)
    except ValidationError as e:
        out = {'messages': {}}
        for err in e.errors():
            out['messages'][err['loc'][0]] = err['msg']
        return False, None, None, out  # унифицируем вывод функции, дабы не возникло проблем при распаковке в переменные

    delivery = db.find_assign_time(courier_id=complete_data.courier_id,
                                   order_id=complete_data.order_id)
    if delivery:
        if delivery.assign_time >= complete_data.complete_time:
            return False, None, None, {'messages': {'invalid_time': 'complete time can not be less or equal than '
                                                                    'assign time'}}
        else:
            return True, complete_data, delivery, None
    else:
        return False, None, None, {'messages': {'invalid_request': 'assignment was canceled or order is already '
                                                                   'complete'}}


def weight_checker(weight):
    if isinstance(weight, float):
        if 0.01 <= weight <= 50:
            _, behind_dot = str(weight).split('.')
            if len(behind_dot) > 2:
                return False, 'too many characters behind the dot'
            else:
                return True, None
        else:
            return False, 'weight value must be more than 0.01 kg and less than 50 kg'
    else:
        return False, 'weight value must be float'


def times_checker(times):
    """
    Валидация временных интервалов

    Проверяет каждое время по шаблону, бьёт на часы и минуты, проверяет корректность значений и порядка

    Parameters:
    argument1 (List): список временных интервалов

    Returns:
    True OR False: результат проверки,
    None OR str : сообщение, если есть

    """
    template = r'\d\d:\d\d[–—-]\d\d:\d\d'
    if len(times) != 0:
        for time in times:
            result = re.findall(template, time)
            if len(result) == 1:
                points = re.split(r'[:—–-]', time)

                hours = [int(i) for i in [points[0], points[2]]]
                mins = [int(i) for i in [points[1], points[3]]]

                for hour in hours:
                    if hour < 0 or hour > 23:
                        return False, 'wrong hours value, it must be less than 24 and more than 00'

                for min in mins:
                    if min < 0 or min > 59:
                        return False, 'wrong minutes value, it must be less than 60 and more than 00'

                flag = False
                if hours[0] > hours[1]:
                    flag = True

                elif hours[0] == hours[1] and mins[0] >= mins[1]:
                    flag = True

                if flag:
                    return False, 'wrong order of time presentation or no distance between time points'

            else:
                return False, f'time data must be presented like this: 10:00–11:00 meanwhile your is "{time}"'
        return True, None
    else:
        return False, 'empty list of times'


def courier_id_checker(courier_id):
    """
    Валидация ID курьера

    Проверяет валидность значения и существование курьера с таким ID

    Parameters:
    argument1 (Any): ID курьера

    Returns:
    True OR False OR None: результат проверки,
                    (None - невалидное значение, False - курьер существует, True - курьера не существует)
    str : сообщение

    """
    if isinstance(courier_id, int) and 0 < courier_id < 10 ** 18:
        result, _ = db.is_courier_exist(courier_id)
        if result:
            return False, 'courier with this id already exist'
        else:
            return True, 'courier with this id does not exist'
    else:
        return None, 'courier id must be positive integer less than 10^18'


def order_id_checker(order_id):
    """
    Валидация ID заказа

    Проверяет валидность значения и существование заказа с таким ID

    Parameters:
    argument1 (Any): ID заказа

    Returns:
    True OR False OR None: результат проверки,
                    (None - невалидное значение, False - заказ существует, True - заказа не существует)
    str: сообщение

    """
    if isinstance(order_id, int) and 0 < order_id < 10 ** 18:
        result, _ = db.is_order_exist(order_id)
        if result:
            return False, 'order with this id already exist'
        else:
            return True, 'order with this id does not exist'
    else:
        return None, 'order id must be positive integer less than 10^18'


def regions_checker(regions):
    if len(regions) != 0:
        for region in regions:

            if not isinstance(region, int) or region < 1 or region > 10**18:
                return False, 'region value must be positive integer less than 10^18'
            elif regions.count(region) > 1:
                return False, 'regions value must be different'

        return True, None
    else:
        return False, 'empty list of regions'


def complete_time_checker(time):
    template = r'\d\d\d\d[—–-]\d\d[—–-]\d\dT\d\d:\d\d:\d\d\.\d\dZ'
    result = re.findall(template, time)
    if len(result) == 1:
        new_time = re.sub(r'[—–-]', '-', time)
        try:
            time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            _ = datetime.strptime(new_time, time_format)
            return True, None
        except ValueError:
            return False, 'wrong time value'
    else:
        return False, 'wrong format of time presentation'
