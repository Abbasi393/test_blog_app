from typing import List, Type, Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.posts_models import Post
from app.schemas.posts_schema import PostCreateModel, PostUpdateModel


class PostService:

    @staticmethod
    def get_all_blogs(session: Session, user_id: int) -> List[Type[Post]]:
        return session.query(Post).filter(Post.user_id == user_id).all()

    @staticmethod
    def get_blog_by_id(session: Session, user_id, blog_id: int) -> Union[Type[Post], None]:
        blog = session.query(Post).filter(Post.id == blog_id, Post.user_id == user_id).first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return blog

    @staticmethod
    def create_blog_post(session: Session, user_id: int, post: PostCreateModel) -> [Post]:
        db_post = Post(**post.model_dump(), user_id=user_id)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        return db_post

    @staticmethod
    def update_blog_post(session: Session, user_id: int, post_id: int, post_update: PostUpdateModel) -> Type[Post]:
        post = session.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        for key, value in post_update.model_dump().items():
            setattr(post, key, value)

        session.commit()
        session.refresh(post)
        return post

    @staticmethod
    def delete_blog_post(session: Session, user_id: int, post_id: int) -> Type[Post]:
        post = session.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        session.delete(post)
        session.commit()
        return post