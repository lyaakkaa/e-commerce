from fastapi import Depends, Response

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


@router.delete("/users/favourites/shanyraks/{id}", status_code=200)
def delete_favourite_shanyrak(
    id: str,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    svc.repository.delete_user_favourite(user_id=jwt_data.user_id, shanyrak_id=id)
    return Response(status_code=200)