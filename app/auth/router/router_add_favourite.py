from fastapi import Depends, HTTPException, Response
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from app.shanyraks.service import Service as Service1
from app.shanyraks.service import get_service as get_service1

@router.post('/users/favourites/shanyraks/{id}', status_code=200)
def add_to_favourites(
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    shanyrak_svc: Service1 = Depends(get_service1),
    auth_svc: Service = Depends(get_service),
) -> str:
    shanyrak = shanyrak_svc.repository.get_shanyrak(shanyrak_id=id)
    if not shanyrak:
        raise HTTPException(
            status_code=404,
            detail=f"Shanyrak with id {id} not found",
        )
    auth_svc.repository.add_to_favourites(user_id=jwt_data.user_id, shanyrak=shanyrak)
    return Response(status_code=200)