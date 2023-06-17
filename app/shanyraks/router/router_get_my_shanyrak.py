from typing import Any, List

from fastapi import Depends
from pydantic import Field
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service

from . import router


class GetMyShanyraksShanyrak(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: Any
    location: Any
    media: List[str] = []


class GetMyShanyraksResponse(AppModel):
    shanyraks: List[GetMyShanyraksShanyrak]


@router.get("/my_shanyraks", response_model=GetMyShanyraksResponse)
def get_my_shanyraks(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    shanyraks = svc.repository.get_my_shanyraks(user_id=user_id)
    resp = {'shanyraks': shanyraks}
    return resp