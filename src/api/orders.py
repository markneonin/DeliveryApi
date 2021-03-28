from fastapi import APIRouter, Response, status

import services.checkers as ch
import database.dbworking as db
from services import utils


router = APIRouter(
    prefix='/orders',
)


@router.post('/', status_code=201)
def create_couriers(data: dict, response: Response):

    result = ch.orders_validation(data)

    if result[0]:
        db.create_orders(result[2])
        return result[1]

    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result[1]


@router.post('/assign', status_code=200)
def assign_orders(data: dict, response: Response):

    result = ch.assign_checker(data)

    if result[0]:
        assign_data = utils.assign(result[1])
        return assign_data
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result[1]


@router.post('/complete', status_code=200)
def complete_order(data: dict, response: Response):

    result = ch.complete_checker(data)

    if result[0]:
        out = utils.complete_order(result[1], result[2])
        return out

    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result[1]
