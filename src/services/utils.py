from database import dbworking as db
from models import response_models
from services import fabrics

from datetime import datetime


def orders_choice(cargo, orders):
    """
    Оптимальное заполнение курьера

    Инициализирует глобальные перменные, необходимые для работы process и generate_valid_combination
    вызывает generate_valid_combination, оптимальная комбинация сохраняется в best_combination или
    absolutely_best_combination, возвращает список с объектами отобранных заказов

    Parameters:
    argument1 (int): Грузоподъемность курьера
    argument2 (list): Лист с объектами заказов

    Returns:
    list: Лист отобранных заказов

    """
    global quantity_of_orders
    global courier_cargo
    global list_of_orders
    global best_result
    global global_quantity
    global best_combination
    global absolutely_best_combination

    quantity_of_orders = len(orders)
    courier_cargo = cargo
    list_of_orders = orders
    best_result = 0
    global_quantity = quantity_of_orders - 1
    best_combination = None
    absolutely_best_combination = None

    generate_valid_combinations(quantity_of_orders)

    out = []

    if absolutely_best_combination:
        for index in range(len(absolutely_best_combination)):
            if absolutely_best_combination[index] == 1:
                out.append(list_of_orders[index])
    else:
        for index in range(quantity_of_orders):
            if best_combination[index] == 1:
                out.append(list_of_orders[index])

    return out


def process(combination):
    """
    Обработчик комбинации

    Находит общий вес заказов в комбинации, сравнивает с лучшим, если найдена лучшая комбинация
    перезаписывает лучший результат и комбинацию

    Parameters:
    argument1 (list): Лист вида [0,1,0,1,0,1...]

    Returns:
    None

    """
    global best_combination, best_result
    total_weight = 0
    for index in range(len(combination)):
        if combination[index] == 1:
            total_weight += list_of_orders[index].weight
    if courier_cargo >= total_weight > best_result:
        best_result = total_weight
        best_combination = combination


def generate_valid_combinations(quantity, combination=[], local_sum=0):
    """
    Генератор валидных комбинаций

    Рекурсивно генерирует комбинацию 0 (не берем заказ) и 1 (берем заказ) заданной длины, при каждом вызове
    увеличивает локальную сумму, если очередной заказ был добавлен в комбинацию. Производит сравнение локальной суммы
    с грузоподъемностью курьера, чтобы не идти по тупиковым веткам

    Parameters:
    argument1 (int): Количество заказов

    Returns:
    None

    """

    global absolutely_best_combination

    if quantity == 0:
        process(combination)
    else:
        try:  # обернул в трай блок для первого вызова, чтобы не нагружать функцию дополнительной проверкой
            index = global_quantity - quantity

            if combination[index] == 1:
                local_sum += list_of_orders[index].weight

            if local_sum < courier_cargo:
                generate_valid_combinations(quantity - 1, combination + [0], local_sum)
                generate_valid_combinations(quantity - 1, combination + [1], local_sum)
            elif local_sum == courier_cargo:
                absolutely_best_combination = combination

        except IndexError:
            generate_valid_combinations(quantity - 1, combination + [0], local_sum)
            generate_valid_combinations(quantity - 1, combination + [1], local_sum)


def assign(courier_id):
    """
    Назначение заказов курьеру

    Проверяет наличие незакрытой доставки у курьера,
    если таковая есть, вернет время её создания и незакрытые заказы из этой доставки.
    Если активной доставки нет, попытается найти заказы и если найдёт,
    по максимуму заполнит курьера ими и создаст доставку и назанчения для отобранных заказов.

    Parameters:
    argument1 (int): ID курьера

    Returns:
    response_models.AssignData: Объект готовый к отправке клиенту

    """
    active_delivery = db.find_active_delivery(courier_id)

    if not active_delivery:

        orders = db.find_valid_orders(courier_id)
        _, courier = db.is_courier_exist(courier_id)

        if orders:
            orders = sorted(orders, key=lambda i: i.weight, reverse=True)

            if len(orders) <= 60:  # если заказов больше 60, время выполнения order_choice может превышать одну секунду
                assigned_orders = orders_choice(cargo=courier.cargo,
                                                orders=orders)
            else:  # поэтому используем примитивный алгоритм выборки заказов для большого количества
                total_weight = 0
                assigned_orders = []
                while total_weight < courier.cargo and orders:
                    order = orders.pop(0)
                    if total_weight + order.weight <= courier.cargo:
                        total_weight += order.weight
                        assigned_orders.append(order)

            delivery = fabrics.create_delivery(courier=courier)
            delivery = db.create_delivery(delivery=delivery)

            assignments = []
            ids_for_out = []

            for order in assigned_orders:
                assigning = fabrics.create_assigning(order_id=order.order_id,
                                                     delivery_id=delivery.delivery_id)
                assignments.append(assigning)
                ids_for_out.append({'id': order.order_id})

            db.create_assignments(assignments)

            assigned_orders_ids = []
            for order in assigned_orders:
                assigned_orders_ids.append(order.order_id)

            db.orders_status_up(orders_ids=assigned_orders_ids,
                                status_key='order_processing')

            out = response_models.AssignData(assign_time=delivery.assign_time,
                                             orders=ids_for_out)

            return out

        else:
            out = response_models.AssignData(orders=[])
            return out

    else:
        active_orders = db.find_active_orders(active_delivery.delivery_id)
        ids_for_out = []

        for order in active_orders:
            ids_for_out.append({'id': order.order_id})

        out = response_models.AssignData(assign_time=active_delivery.assign_time,
                                         orders=ids_for_out)
        return out


def patch_courier(patch_data, courier_id):
    """
    Изменение данных курьера

    Меняет параметры курьера в БД, проверяет наличие активной доставки у курьера
    если таковая имеется отменяет назначения заказов, не подходящих под новые параметры курьера,
    если в результате отмены в доставке больше нет активных заказов, меняет статус доставки на complete.
    Возвращает новую информацию о курьере

    Parameters:
    argument1 (int): ID курьера

    Returns:
    response_models.Courier: Объект готовый к отправке клиенту

    """
    active_delivery = db.find_active_delivery(courier_id)

    if active_delivery:
        active_orders = db.find_active_orders(active_delivery.delivery_id)
        active_orders_ids = []
        for order in active_orders:
            active_orders_ids.append(order.order_id)

        cargo, regions_objects, working_hours_objects = fabrics.create_patch_data(patch_data=patch_data,
                                                                                  courier_id=courier_id)
        if regions_objects:
            db.delete_regions(courier_id)
        if working_hours_objects:
            db.delete_working_hours(courier_id)

        db.patch_courier(cargo=cargo,
                         regions_objects=regions_objects,
                         working_hours_objects=working_hours_objects,
                         courier_id=courier_id)

        valid_active_orders = db.find_valid_active_orders(courier_id=courier_id,
                                                          active_orders=active_orders_ids)
        if valid_active_orders:
            _, courier = db.is_courier_exist(courier_id)

            assigned_orders = orders_choice(cargo=courier.cargo,
                                            orders=valid_active_orders)
            assigned_orders_ids = []
            for order in assigned_orders:
                assigned_orders_ids.append(order.order_id)

            canceled_orders_ids = set(active_orders_ids) - set(assigned_orders_ids)

            db.orders_status_up(orders_ids=list(canceled_orders_ids),
                                status_key='order_available')
            db.assign_status_up(orders_ids=list(canceled_orders_ids),
                                delivery=active_delivery)

        else:
            db.orders_status_up(orders_ids=active_orders_ids,
                                status_key='order_available')
            db.assign_status_up(orders_ids=active_orders_ids,
                                delivery=active_delivery)
            db.delivery_status_up(delivery_id=active_delivery.delivery_id)

    else:
        cargo, regions_objects, working_hours_objects = fabrics.create_patch_data(patch_data=patch_data,
                                                                                  courier_id=courier_id)

        if regions_objects:
            db.delete_regions(courier_id)
        if working_hours_objects:
            db.delete_working_hours(courier_id)

        db.patch_courier(cargo=cargo,
                         regions_objects=regions_objects,
                         working_hours_objects=working_hours_objects,
                         courier_id=courier_id)

    courier_obj, regions_objs, hours_objs = db.courier_data(courier_id)

    courier = fabrics.courier_to_client(courier=courier_obj,
                                        regions=regions_objs,
                                        working_hours=hours_objs)

    return courier


def complete_order(complete_data, delivery):
    """
    Завершение заказа

    Апдейтит статус и complete_time заказа в БД. Проверяет был ли он последним в доставке,
    если да, апдейтит статус доставки

    Parameters:
    argument1 (request_models.CompleteOrder): Объект полученный от клиента
    argument2 (tables.Delivery): Объект доставки полученный из БД во время валидации

    Returns:
    dict: словарь вида - {'order_id': (int)}, готовый к упаковке в json

    """
    db.complete_order(order_id=complete_data.order_id,
                      complete_time=complete_data.complete_time)

    active_orders = db.find_active_orders(delivery.delivery_id)

    if not active_orders:
        db.delivery_status_up(delivery.delivery_id)

    return {'order_id': complete_data.order_id}


def courier_info_full(courier_id):
    """
    Полная информация о курьере

    Находит основные параметры курьера, вызывает функции расчета заработка и рейтинга,
    вызывает fabrics.courier_info_full со всеми параметрами

    Parameters:
    argument1 (int): ID курьера

    Returns:
    response_models.FullCourierInfo: объект готовый к отправке клиенту

    """
    courier_obj, regions_objs, hours_objs = db.courier_data(courier_id)

    rating = calculate_rating(courier_id)
    earnings = calculate_earnings(courier_id)

    out = fabrics.courier_info_full(courier=courier_obj,
                                    regions=regions_objs,
                                    working_hours=hours_objs,
                                    rating=rating,
                                    earnings=earnings)
    return out


def calculate_earnings(courier_id):
    """
    Расчёт заработка

    Находит валидные закрытые доставки, считает заработок на основе
    информации о типе курьера на момент создания доставки

    Parameters:
    argument1 (int): ID курьера

    Returns:
    int: Заработок

    """
    earnings = 0

    complete_deliveries = db.find_complete_deliveries(courier_id)

    if complete_deliveries:
        for delivery in complete_deliveries:
            if delivery.cargo == 10:
                earnings += (500 * 2)
            elif delivery.cargo == 15:
                earnings += (500 * 5)
            else:
                earnings += (500 * 9)

    return earnings


def calculate_rating(courier_id):
    """
    Расчёт рейтинга

    Находит валидные закрытые доставки, считает время выполнения заказов из них,
    формируя листы с длительностю для каждого региона, считает рейтинг

    Parameters:
    argument1 (int): ID курьера

    Returns:
    float: рейтинг
    OR
    None: расёт рейтинга невозможен

    """
    complete_deliveries = db.find_complete_deliveries(courier_id)

    if complete_deliveries:

        orders_for_calculate = {}

        for delivery in complete_deliveries:
            complete_orders = db.find_complete_orders(delivery.delivery_id)
            complete_orders = sorted(complete_orders, key=lambda x: x.complete_time)
            orders_for_calculate[delivery.assign_time] = complete_orders

        regions_with_durations = {}

        for orders in orders_for_calculate.values():
            for order in orders:
                regions_with_durations[order.region] = []

        template = "%Y-%m-%dT%H:%M:%S.%fZ"

        for assign_time, orders in orders_for_calculate.items():

            t1 = datetime.strptime(orders[0].complete_time, template)
            t2 = datetime.strptime(assign_time, template)

            duration_of_first = t1 - t2
            regions_with_durations[orders[0].region].append(duration_of_first.total_seconds())

            for i in range(1, len(orders)):
                t1 = datetime.strptime(orders[i].complete_time, template)
                t2 = datetime.strptime(orders[i - 1].complete_time, template)
                duration = t1 - t2
                regions_with_durations[orders[i].region].append(duration.total_seconds())

        average_durations = []
        for durations in regions_with_durations.values():
            a = sum(durations)
            b = len(durations)
            average_durations.append(a / b)

        rating = ((3600 - min(min(average_durations), 3600)) / 3600) * 5
        rating = round(rating, 2)

        return rating

    else:
        return None
