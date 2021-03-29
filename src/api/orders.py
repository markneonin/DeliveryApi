from fastapi import APIRouter, Response, status

from database import dbworking as db
from services import checkers as ch
from services import utils


router = APIRouter(
    prefix='/orders',
)


@router.post('', status_code=201)
def create_orders(data: dict, response: Response):

    result, output, orders_objects = ch.orders_validation(data)

    if result:
        db.create_orders(orders_objects)
        return output
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return output


@router.post('/assign', status_code=200)
def assign_orders(data: dict, response: Response):

    result, courier_id, output = ch.assign_checker(data)

    if result:
        assign_data = utils.assign(courier_id)
        return assign_data
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return output


@router.post('/complete', status_code=200)
def complete_order(data: dict, response: Response):

    result, complete_data, delivery, output = ch.complete_checker(data)

    if result:
        comp_data = utils.complete_order(complete_data, delivery)
        return comp_data

    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return output
