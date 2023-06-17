from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service

from . import router


class UpdateCommentRequest(AppModel):
    content: str


@router.patch("/{id}/comments/{comment_id}")
def update_comment(
    id: str,
    comment_id: str,
    input: UpdateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.repository.update_comment_by_id(jwt_data.user_id, id, comment_id, input.content)
    return Response(status_code=200)
