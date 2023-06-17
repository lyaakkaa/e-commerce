
from fastapi import Depends, Response
from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


class CreateCommentRequest(AppModel):
    content: str


@router.post("/{id}/comments", status_code=201)
def create_comment(
    id: str,
    input: CreateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    svc.repository.create_comment_by_id(id, jwt_data.user_id, input.content)
    return Response(status_code=201)
