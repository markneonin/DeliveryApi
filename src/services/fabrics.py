import re
from models import response_models
from datetime import datetime
from status_catalog import status_catalog
from models import tables
from models.request_models import CourierType


def courier_to_write(courier):
    courier_id = courier.courier_id

    if courier.courier_type == CourierType.CAR:
        cargo = 50
    elif courier.courier_type == CourierType.BIKE:
        cargo = 15
    elif courier.courier_type == CourierType.BIKE:
        cargo = 10

    courier_object = tables.Courier(courier_id=courier_id,
                                    cargo=cargo)

    courier_regions = []
    working_hours = []

    for region in courier.regions:
        courier_regions.append(tables.CourierRegion(courier_id=courier_id,
                                                    region=region))

    for time in courier.working_hours:
        start, stop = re.split(r'[-—–]', time)
        working_hours.append(tables.WorkingHours(courier_id=courier_id,
                                                 start=start,
                                                 stop=stop))

    return courier_object, courier_regions, working_hours


def courier_to_client(courier, regions, working_hours):
    list_of_regions = []
    time = []

    for hours in working_hours:
        t = hours.start + '–' + hours.stop
        time.append(t)

    for region in regions:
        list_of_regions.append(region.region)

    if courier.cargo == 50:
        courier_type = 'car'
    elif courier.cargo == 15:
        courier_type = 'bike'
    elif courier.cargo == 10:
        courier_type = 'foot'

    courier_obj = response_models.Courier(courier_id=courier.courier_id,
                                          courier_type=courier_type,
                                          regions=list_of_regions,
                                          working_hours=time)

    return courier_obj


def courier_info_full(courier, regions, working_hours, rating, earnings):
    list_of_regions = []
    time = []

    for hours in working_hours:
        t = hours.start + '–' + hours.stop
        time.append(t)

    for region in regions:
        list_of_regions.append(region.region)

    if courier.cargo == 50:
        courier_type = 'car'
    elif courier.cargo == 15:
        courier_type = 'bike'
    elif courier.cargo == 10:
        courier_type = 'foot'

    full_info = response_models.FullCourierInfo(courier_id=courier.courier_id,
                                                courier_type=courier_type,
                                                regions=list_of_regions,
                                                working_hours=time,
                                                rating=rating,
                                                earnings=earnings)

    return full_info


def order_to_write(order):
    order_id = order.order_id
    delivery_hours = []
    status = status_catalog['order_available']

    order_object = tables.Orders(order_id=order_id,
                                 region=order.region,
                                 weight=order.weight,
                                 status=status)

    for time in order.delivery_hours:
        start, stop = re.split(r'[-—–]', time)
        delivery_hours.append(tables.DeliveryHours(order_id=order_id,
                                                   start=start,
                                                   stop=stop))

    return order_object, delivery_hours


def create_delivery(courier):
    status = status_catalog['delivery_processing']
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4] + 'Z'

    delivery_object = tables.Delivery(courier_id=courier.courier_id,
                                      assign_time=now,
                                      cargo=courier.cargo,
                                      status=status)

    return delivery_object


def create_assigning(order_id, delivery_id):
    status = status_catalog['assign_actual']

    assigning_object = tables.Assigning(order_id=order_id,
                                        delivery_id=delivery_id,
                                        status=status)

    return assigning_object


def create_patch_data(patch_data, courier_id):
    cargo = None
    working_hours_objects = []
    regions_objects = []

    if patch_data.courier_type == CourierType.FOOT:
        cargo = 10
    elif patch_data.courier_type == CourierType.BIKE:
        cargo = 15
    elif patch_data.courier_type == CourierType.CAR:
        cargo = 50

    if patch_data.working_hours:
        for time in patch_data.working_hours:
            start, stop = re.split(r'[-—–]', time)
            working_hours_objects.append(tables.WorkingHours(courier_id=courier_id,
                                                             start=start,
                                                             stop=stop))
    if patch_data.regions:
        for region in patch_data.regions:
            regions_objects.append(tables.CourierRegion(courier_id=courier_id,
                                                        region=region))

    return cargo, regions_objects, working_hours_objects
