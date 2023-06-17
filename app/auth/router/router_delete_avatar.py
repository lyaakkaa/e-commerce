
from fastapi import Depends, Response

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


@router.delete("/users/avatar", status_code=200)
def delete_avatar(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    svc.repository.delete_avatar(user_id=jwt_data.user_id)
    return Response(status_code=200)