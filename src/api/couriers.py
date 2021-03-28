from fastapi import APIRouter, Response, status

import services.checkers as ch
import database.dbworking as db
from services import utils


router = APIRouter(
    prefix='/couriers',
)


@router.post('/', status_code=201)
def create_couriers(data: dict, response: Response):  # проще было бы сразу в дата классе request_models.CouriersData
    # указать, что по ключу "data" лежит лист с объектами request_models.Courier, а в параметрах данного роута
    # указать, что тело запроса это request_models.CouriersData, но из-за жестких ограничений на формат выходных
    # данных и статус-код при возникновении ошибок валидации, принимаем тело запроса в контейнер класса dict и
    # валидируем данные в модуле checkers, чтобы контроллировать процесс, это в том числе касается и всех остальных
    # роутов

    result = ch.couriers_validation(data)
    if result[0]:
        db.create_couriers(result[2])
        return result[1]

    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result[1]


@router.patch('/{courier_id}', status_code=200)
def patch_courier(patch_data: dict, response: Response, courier_id: int):

    result = ch.patch_checker(patch_data, courier_id)

    if result[0]:
        new_data = utils.patch_courier(result[1], courier_id)
        return new_data

    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result[1]


@router.get('/{courier_id}', status_code=200)
def complete_order(response: Response, courier_id: int):

    result = db.is_courier_exist(courier_id)

    if result[0]:
        full_data = utils.courier_info_full(courier_id)
        return full_data

    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'courier with this id does not exist'}


