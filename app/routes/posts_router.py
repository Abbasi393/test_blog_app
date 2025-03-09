from fastapi import (APIRouter, Depends, HTTPException)
from starlette import status
from sqlalchemy.orm import Session

from app.core.config import get_session
from app.core.security import get_current_user
from app.core.cache import redis_cache_result, invalidate_cache

from app.schemas.posts_schema import (PostModel, PostCreateModel, PostUpdateModel)
from app.models.user_models import User
from app.services.post_service import PostService

posts_router = APIRouter(prefix="/blog/posts", tags=["Blog Posts"])


@posts_router.get(
    "/",
    summary="Get all posts",
    status_code=status.HTTP_200_OK,
    response_model=list[PostModel]
)
@redis_cache_result
def list_posts(
        session: Session = Depends(get_session),
        ums_user: User = Depends(get_current_user),
):
    return PostService.get_all_blogs(session, ums_user.id)


@posts_router.post(
    "/",
    summary="Create a new post",
    status_code=status.HTTP_201_CREATED,
    response_model=PostModel
)
def create_post(
        post: PostCreateModel,
        session: Session = Depends(get_session),
        ums_user: User = Depends(get_current_user),
):
    blog_post = PostService.create_blog_post(session, ums_user.id, post)
    invalidate_cache(ums_user.id)
    return blog_post


@posts_router.get(
    "/{post_id}",
    summary="Get a post by id",
    status_code=status.HTTP_200_OK,
    response_model=PostModel
)
@redis_cache_result
def read_post(
        post_id: int,
        session: Session = Depends(get_session),
        ums_user: User = Depends(get_current_user),
):
    blog_post = PostService.get_blog_by_id(session, ums_user.id, post_id)
    if not blog_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return blog_post


@posts_router.delete(
    "/{post_id}",
    summary="Delete a post",
    status_code=status.HTTP_200_OK,
    response_model=PostModel
)
def delete_post(
        post_id: int,
        session: Session = Depends(get_session),
        ums_user: User = Depends(get_current_user),
):
    blog_post = PostService.delete_blog_post(session, ums_user.id, post_id)
    invalidate_cache(ums_user.id)
    return blog_post


@posts_router.put(
    "/{post_id}",
    summary="Update a post",
    status_code=status.HTTP_200_OK,
    response_model=PostModel
)
def update_post(
        post_id: int,
        post_update: PostUpdateModel,
        session: Session = Depends(get_session),
        ums_user: User = Depends(get_current_user),
):
    blog_post = PostService.update_blog_post(session, ums_user.id, post_id, post_update)
    invalidate_cache(ums_user.id)
    return blog_post
