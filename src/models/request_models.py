from pydantic import BaseModel, validator, root_validator
from enum import Enum
from typing import List, Optional, Any
import re

import services.checkers as ch


class CourierType(Enum):
    FOOT = 'foot'
    BIKE = 'bike'
    CAR = 'car'


class Courier(BaseModel):
    class Config:
        extra = 'forbid'

    """""
    Не смотря на использование педантика, из-за жестких ограничений по валидации входных
    данных по типам, принимаем многие поля как Any и валидируем лапками
    """""

    courier_id: Any = ...
    courier_type: CourierType
    regions: List[Any]
    working_hours: List[str]

    @validator('courier_id')
    def check_courier_id(cls, v):
        result, message = ch.courier_id_checker(v)
        if not result:
            raise ValueError(message)
        return v

    @validator('regions')
    def check_regions(cls, v):
        result, message = ch.regions_checker(v)
        if not result:
            raise ValueError(message)
        return v

    @validator('working_hours')  # Не использую рут валидатор, чтобы была корректная информация о локации ошибок
    def check_working_hours(cls, v):
        result, message = ch.times_checker(v)
        if not result:
            raise ValueError(message)
        return v


class CouriersData(BaseModel):
    class Config:
        extra = 'forbid'

    data: List[Any]


class DataToPatch(BaseModel):
    class Config:
        extra = 'forbid'

    courier_type: Optional[CourierType]
    regions: Optional[List[Any]]
    working_hours: Optional[List[str]]

    @validator('courier_type')
    def check_type(cls, v):
        if v is None:
            raise ValueError('invalid courier type it can not be None')
        return v

    @validator('regions')
    def check_regions(cls, v):
        if v is None:
            raise ValueError('invalid regions it can not be None')
        else:
            result, message = ch.regions_checker(v)
            if not result:
                raise ValueError(message)
        return v

    @validator('working_hours')
    def check_hours(cls, v):
        if v is None:
            raise ValueError
        else:
            result, message = ch.times_checker(v)
            if not result:
                raise ValueError(message)
        return v

    @root_validator  # по скольку все поля Optional, вводим дополнительную проверку рут валидатором
    def is_empty(cls, values):
        counter = 0
        for value in values.values():
            if value is None:
                counter += 1
        if counter == 3:
            raise ValueError('empty data')
        return values


class Order(BaseModel):
    class Config:
        extra = 'forbid'

    order_id: Any = ...
    weight: Any = ...
    region: Any = ...
    delivery_hours: List[str]

    @validator('order_id')
    def check_order_id(cls, v):
        result, message = ch.order_id_checker(v)
        if not result:
            raise ValueError(message)
        return v

    @validator('region')
    def check_region(cls, v):
        if not isinstance(v, int) or v < 1 or v > 10 ** 18:
            raise ValueError('region value must be positive integer less than 10^18')
        return v

    @validator('weight')
    def check_weight(cls, v):
        result, message = ch.weight_checker(v)
        if not result:
            raise ValueError(message)
        return v

    @validator('delivery_hours')
    def check_delivery_hours(cls, v):
        result, message = ch.times_checker(v)
        if not result:
            raise ValueError(message)
        return v


class OrdersData(BaseModel):
    class Config:
        extra = 'forbid'

    data: List[Any]


class AssignData(BaseModel):
    class Config:
        extra = 'forbid'

    courier_id: Any = ...

    @validator('courier_id')
    def check_courier_id(cls, v):
        result, message = ch.courier_id_checker(v)
        if result != False:
            raise ValueError(message)
        return v


class CompleteOrder(BaseModel):
    class Config:
        extra = 'forbid'

    courier_id: Any = ...
    order_id: Any = ...
    complete_time: str

    @validator('courier_id')
    def cour_id(cls, v):
        result, message = ch.courier_id_checker(v)
        if result == False:  # чекер возвращает три флага (True, False, None), нас устроит только False
            return v
        else:
            raise ValueError(message)

    @validator('order_id')
    def order(cls, v):
        result, message = ch.order_id_checker(v)
        if result == False:
            return v
        else:
            raise ValueError(message)

    @validator('complete_time')
    def complete(cls, v):
        result, message = ch.complete_time_checker(v)
        if not result:
            raise ValueError(message)
        else:
            new_time = re.sub(r'[—–-]', '-', v)  # на всякий случай
        return new_time
