from sqlalchemy import or_, between

from status_catalog import status_catalog
from .database import Session
from models import tables
from services import fabrics


# работал с ОРМ первый раз, не судите строго за кривую реализацию


def create_couriers(couriers):
    session = Session()

    couriers_objects = []
    regions_objects = []
    working_hours_objects = []

    for courier in couriers:
        courier_obj, regions, working_hours = fabrics.courier_to_write(courier)
        couriers_objects.append(courier_obj)
        regions_objects.extend(regions)
        working_hours_objects.extend(working_hours)

    try:
        session.add_all(couriers_objects)
        session.add_all(regions_objects)
        session.add_all(working_hours_objects)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_orders(orders):
    session = Session()

    orders_objects = []
    delivery_hours_objects = []

    for order in orders:
        order_obj, delivery_hours = fabrics.order_to_write(order)
        orders_objects.append(order_obj)
        delivery_hours_objects.extend(delivery_hours)

    try:
        session.add_all(orders_objects)
        session.add_all(delivery_hours_objects)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def is_courier_exist(courier_id):
    session = Session()
    courier = session.query(tables.Courier).filter(tables.Courier.courier_id == courier_id).first()
    session.close()
    if courier:
        return True, courier
    else:
        return False,


def is_order_exist(order_id):
    session = Session()
    order = session.query(tables.Orders).filter(tables.Orders.order_id == order_id).first()
    session.close()
    if order:
        return True, order
    else:
        return False,


def find_active_delivery(courier_id):
    session = Session()
    status = status_catalog['delivery_processing']

    active_delivery = session.query(tables.Delivery).filter(
        tables.Delivery.courier_id == courier_id).filter(
        tables.Delivery.status == status).first()

    session.close()

    return active_delivery


def find_active_orders(delivery_id):
    session = Session()
    assign_status = status_catalog['assign_actual']
    order_status = status_catalog['order_processing']

    sub_query_1 = session.query(tables.Assigning)

    active_orders = session.query(tables.Orders).distinct(tables.Orders.order_id).filter(
        sub_query_1.exists()).filter(
        tables.Orders.status == order_status).filter(
        tables.Assigning.delivery_id == delivery_id).filter(
        tables.Assigning.status == assign_status).filter(
        tables.Assigning.order_id == tables.Orders.order_id).all()

    session.close()

    return active_orders


def find_valid_orders(courier_id):
    session = Session()
    order_status = status_catalog['order_available']

    sub_query_1 = session.query(tables.CourierRegion)
    sub_query_2 = session.query(tables.Courier)
    sub_query_3 = session.query(tables.DeliveryHours)
    sub_query_4 = session.query(tables.WorkingHours)

    valid_orders = session.query(tables.Orders).distinct(tables.Orders.order_id).filter(
        sub_query_1.exists()).filter(
        sub_query_2.exists()).filter(
        sub_query_3.exists()).filter(
        sub_query_4.exists()).filter(
        tables.Orders.status == order_status).filter(   # ищем доступные заказы
        tables.CourierRegion.courier_id == courier_id).filter(  # у которых регион равен региону
        tables.CourierRegion.region == tables.Orders.region).filter(    # одной из записей регионов курьера
        tables.Courier.courier_id == courier_id).filter(
        tables.Courier.cargo >= tables.Orders.weight).filter(   # вес которых не превышает грузоподъемность курьера
        tables.DeliveryHours.order_id == tables.Orders.order_id).filter(
        tables.WorkingHours.courier_id == courier_id).filter(
        or_(between(tables.WorkingHours.stop, tables.DeliveryHours.start, tables.DeliveryHours.stop),
            between(tables.DeliveryHours.stop, tables.WorkingHours.start, tables.WorkingHours.stop))).all()
                                                    # у которых время доставки пересекается с рабочим временем курьера

    session.close()

    return valid_orders


def find_valid_active_orders(courier_id, active_orders):
    session = Session()
    order_status = status_catalog['order_processing']

    sub_query_1 = session.query(tables.CourierRegion)
    sub_query_2 = session.query(tables.Courier)
    sub_query_3 = session.query(tables.DeliveryHours)
    sub_query_4 = session.query(tables.WorkingHours)

    valid_active_orders = session.query(tables.Orders).distinct(tables.Orders.order_id).filter(
        sub_query_1.exists()).filter(
        sub_query_2.exists()).filter(
        sub_query_3.exists()).filter(
        sub_query_4.exists()).filter(
        tables.Orders.order_id.in_(active_orders)).filter(
        tables.Orders.status == order_status).filter(
        tables.CourierRegion.courier_id == courier_id).filter(
        tables.CourierRegion.region == tables.Orders.region).filter(
        tables.Courier.courier_id == courier_id).filter(
        tables.Courier.cargo >= tables.Orders.weight).filter(
        tables.DeliveryHours.order_id == tables.Orders.order_id).filter(
        tables.WorkingHours.courier_id == courier_id).filter(
        or_(between(tables.WorkingHours.stop, tables.DeliveryHours.start, tables.DeliveryHours.stop),
            between(tables.DeliveryHours.stop, tables.WorkingHours.start, tables.WorkingHours.stop))).all()

    session.close()

    return valid_active_orders


def orders_status_up(orders_ids, status_key):
    session = Session()
    status = status_catalog[status_key]

    try:
        session.query(tables.Orders).filter(
            tables.Orders.order_id.in_(orders_ids)).update(
            {'status': status})
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_delivery(delivery):
    session = Session()

    try:
        session.add(delivery)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    delivery = get_last_delivery()

    return delivery


def get_last_delivery():
    session = Session()
    last_delivery = session.query(tables.Delivery).order_by(tables.Delivery.delivery_id.desc()).first()
    session.close()

    return last_delivery


def create_assignments(assignments):
    session = Session()

    try:
        session.add_all(assignments)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_regions(courier_id):
    session = Session()
    try:
        session.query(tables.CourierRegion).filter(
            tables.CourierRegion.courier_id == courier_id).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_working_hours(courier_id):
    session = Session()
    try:
        session.query(tables.WorkingHours).filter(
            tables.WorkingHours.courier_id == courier_id).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def patch_courier(cargo, regions_objects, working_hours_objects, courier_id):
    session = Session()
    try:
        if cargo:
            session.query(tables.Courier).filter(
                tables.Courier.courier_id == courier_id).update({'cargo': cargo})
        if regions_objects:
            session.add_all(regions_objects)
        if working_hours_objects:
            session.add_all(working_hours_objects)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def assign_status_up(orders_ids, delivery):
    session = Session()
    status = status_catalog['assign_canceled']

    try:
        session.query(tables.Assigning).filter(
            tables.Assigning.delivery_id == delivery.delivery_id).filter(
            tables.Assigning.order_id.in_(orders_ids)).update({'status': status})
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delivery_status_up(delivery_id):
    session = Session()
    status = status_catalog['delivery_complete']

    try:
        session.query(tables.Delivery).filter(
            tables.Delivery.delivery_id == delivery_id).update({'status': status})
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def courier_data(courier_id):
    session = Session()

    courier_obj = session.query(tables.Courier).filter(tables.Courier.courier_id == courier_id).first()

    regions_objs = session.query(tables.CourierRegion).filter(tables.CourierRegion.courier_id == courier_id).all()

    wh_objs = session.query(tables.WorkingHours).filter(tables.WorkingHours.courier_id == courier_id).all()

    session.close()

    return courier_obj, regions_objs, wh_objs


def find_assign_time(courier_id, order_id):
    session = Session()
    order_status = status_catalog['order_processing']
    assign_status = status_catalog['assign_actual']

    sub_query_1 = session.query(tables.Orders)
    sub_query_2 = session.query(tables.Assigning)

    delivery = session.query(tables.Delivery).filter(
        sub_query_1.exists()).filter(
        sub_query_2.exists()).filter(
        tables.Delivery.courier_id == courier_id).filter(
        tables.Assigning.delivery_id == tables.Delivery.delivery_id).filter(
        tables.Assigning.order_id == order_id).filter(
        tables.Assigning.status == assign_status).filter(
        tables.Orders.status == order_status).filter(
        tables.Orders.order_id == order_id).all()

    session.close()

    if delivery:
        return delivery[0]
    else:
        return None


def complete_order(order_id, complete_time):
    session = Session()
    order_status = status_catalog['order_complete']

    try:
        session.query(tables.Orders).filter(
            tables.Orders.order_id == order_id).update({'status': order_status,
                                                        'complete_time': complete_time})
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def find_complete_deliveries(courier_id):
    session = Session()
    delivery_status = status_catalog['delivery_complete']
    assign_status = status_catalog['assign_actual']

    sub_query_1 = session.query(tables.Assigning)

    deliveries = session.query(tables.Delivery).distinct(tables.Delivery.delivery_id).filter(
        sub_query_1.exists()).filter(
        tables.Delivery.status == delivery_status).filter(
        tables.Delivery.courier_id == courier_id).filter(
        tables.Assigning.delivery_id == tables.Delivery.delivery_id).filter(
        tables.Assigning.status == assign_status).all()

    session.close()

    return deliveries


def find_complete_orders(delivery_id):
    session = Session()
    assign_status = status_catalog['assign_actual']

    sub_query_1 = session.query(tables.Assigning)

    orders = session.query(tables.Orders).distinct(tables.Orders.order_id).filter(
        sub_query_1.exists()).filter(
        tables.Assigning.status == assign_status).filter(
        tables.Assigning.delivery_id == delivery_id).filter(
        tables.Assigning.order_id == tables.Orders.order_id).all()

    session.close()

    return orders
