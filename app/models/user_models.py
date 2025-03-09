from sqlalchemy import (Column, String)
from app.models import (BaseModel, AutoIdModelMixin, AuditModelMixin, SoftDeleteMixin)


class User(BaseModel, AutoIdModelMixin, AuditModelMixin, SoftDeleteMixin):
    __tablename__ = 'users'

    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
