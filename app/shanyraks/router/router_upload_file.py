from fastapi import Depends, Response, UploadFile
from typing import List


from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router

@router.post("/{id}/media", status_code=200)
def upload_images(
    input: List[UploadFile],
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    media = []
    for image in input:
        url = svc.s3_service.upload_file(file=image.file, filename=image.filename)
        media.append(url)
        # svc.repository.upload_images(id=id, user_id=jwt_data.user_id, image_url=url)
    return media
