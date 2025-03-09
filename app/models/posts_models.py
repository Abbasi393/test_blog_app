from sqlalchemy import (Column, String, Integer, ForeignKey, Text)

from app.models.base_model import BaseModel
from app.models.model_mixins import (AutoIdModelMixin, AuditModelMixin, SoftDeleteMixin)


class Post(BaseModel, AutoIdModelMixin, AuditModelMixin, SoftDeleteMixin):
    __tablename__ = "posts"

    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
