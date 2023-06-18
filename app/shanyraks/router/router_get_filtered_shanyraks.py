from typing import Any, List, Dict

from fastapi import Depends
from pydantic import Field
from app.utils import AppModel

from ..service import Service, get_service

from . import router


class GetShanyrakResponseItem(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    location: Dict = {}


class GetShanyrakResponse(AppModel):
    total: int = 0
    items: List[GetShanyrakResponseItem] = []


@router.get(
    "/",
    status_code=200,
    response_model=GetShanyrakResponse,
)
def get_filtered_shanyraks(
    limit: int,
    offset: int,
    type: str | None = None,
    rooms_count: int | None = None,
    price_from: int | None = None,
    price_until: int | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    radius: float | None = None,
    svc: Service = Depends(get_service),
) -> dict[str, Any]:
    response = svc.repository.get_filtered_shanyraks(
        limit=limit,
        offset=offset,
        type=type,
        rooms_count=rooms_count,
        price_from=price_from,
        price_until=price_until,
        latitude=latitude,
        longitude=longitude,
        radius=radius,
    )
    return response