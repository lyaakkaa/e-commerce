from typing import Any, List

from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from ..service import Service, get_service

from . import router


class GetShanyrakResponse(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: Any
    media: List[str] = []


@router.get("/{shanyrak_id:str}", response_model=GetShanyrakResponse)
def get_shanyrak(
    shanyrak_id: str,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)
    if shanyrak is None:
        return Response(status_code=404)
    return GetShanyrakResponse(**shanyrak)