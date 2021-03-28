from fastapi import APIRouter

from .couriers import router as couriers_router
from .orders import router as orders_router


router = APIRouter()

router.include_router(couriers_router)
router.include_router(orders_router)