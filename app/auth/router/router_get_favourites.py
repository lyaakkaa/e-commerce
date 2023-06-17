from typing import Any, List, Dict
from fastapi import Depends

from app.utils import AppModel
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from pydantic import Field


class Shanyrak(AppModel):
    id: Any = Field(alias="_id")
    address: str


class GetFavouritesResponse(AppModel):
    shanyraks: List[Shanyrak]




@router.get("/users/favourites/shanyraks", status_code=200, response_model=GetFavouritesResponse)
def get_favourites_shanyraks(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
) -> GetFavouritesResponse:
    favourites = svc.repository.get_user_favourites(user_id=jwt_data.user_id)
    return {"shanyraks": favourites}