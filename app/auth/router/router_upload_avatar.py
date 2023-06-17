
from fastapi import Depends, Response, UploadFile

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from app.shanyraks.service import Service as Service1
from app.shanyraks.service import get_service as get_service1


@router.post("/users/avatar", status_code=200)
def upload_avatar(
    avatar_img: UploadFile,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    auth_svc: Service = Depends(get_service),
    shanyraks_svc: Service1 = Depends(get_service1)
):
    avatar_url = shanyraks_svc.s3_service.upload_avatar(user_id=jwt_data.user_id, file=avatar_img.file, filename=avatar_img.filename)
    auth_svc.repository.upload_avatar(user_id=jwt_data.user_id, avatar_url=avatar_url)
    return Response(status_code=200)