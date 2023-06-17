from fastapi import Depends, Response
from typing import List
from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


class DeleteImagesRequest(AppModel):
    media: List[str]


@router.delete("/{id: str}/media", status_code=200)
def delete_images(
    id: str,
    input: DeleteImagesRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):
    images_dict = input.dict()
    images_urls = images_dict['media']
    for image in images_urls:
        image_list = image.split('/')
        image_filename = image_list[-1]
        print(image_filename)
        svc.s3_service.delete_file(id=id, filename=image_filename)
        svc.repository.delete_images(id=id, user_id=jwt_data.user_id, image_url=image)
    return Response(status_code=200)
