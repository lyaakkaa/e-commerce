from typing import Any

from fastapi import Depends
from pydantic import Field
from app.utils import AppModel

from ..service import Service, get_service

from . import router


class Comment(AppModel):
    id: Any = Field(alias="_id")
    author_id: Any
    content: str
    created_at: str


class GetCommentsResponse(AppModel):
    comments: list[Comment]


@router.get("/{id}/comments", response_model=GetCommentsResponse)
def get_comments(
    id: str,
    svc: Service = Depends(get_service),
):
    comments = svc.repository.get_comments_by_id(id)

    comments_data = []
    for comment in comments:
        comment_data = Comment(
            id=str(comment["_id"]),
            author_id=comment["author_id"],
            content=comment["content"],
            created_at=str(comment["created_at"]),
        )
        comments_data.append(comment_data)

    response = GetCommentsResponse(comments=comments_data)
    return response
