from fastapi import APIRouter, Response, status

from database import dbworking as db
from services import checkers as ch
from services import utils

router = APIRouter(
    prefix='/couriers',
)

"""""
Проще было бы сразу в дата классе request_models.CouriersData
указать, что по ключу "data" лежит лист с объектами request_models.Courier, а в параметрах данного роута
указать, что тело запроса это request_models.CouriersData, но из-за жестких ограничений на формат выходных
данных и статус-код при возникновении ошибок валидации, принимаем тело запроса в контейнер класса dict и
валидируем данные в модуле checkers, чтобы контроллировать процесс, это, в том числе, касается и остальных роутов
"""""


@router.post('', status_code=201)
def create_couriers(data: dict, response: Response):
    result, output, couriers_objects = ch.couriers_validation(data)

    if result:
        db.create_couriers(couriers_objects)
        return output

    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return output


@router.patch('/{courier_id}', status_code=200)
def patch_courier(data: dict, response: Response, courier_id: int):
    result, patch_data, output = ch.patch_checker(data, courier_id)

    if result:
        new_data = utils.patch_courier(patch_data, courier_id)
        return new_data

    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return output


@router.get('/{courier_id}', status_code=200)
def courier_info(response: Response, courier_id: int):
    result, _ = db.is_courier_exist(courier_id)

    if result:
        full_data = utils.courier_info_full(courier_id)
        return full_data

    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'courier with this id does not exist'}
