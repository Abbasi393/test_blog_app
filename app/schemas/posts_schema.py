from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

class PostCreateModel(PostBase):
    pass

class PostUpdateModel(PostBase):
    pass

class PostModel(PostBase):
    id: int

    class Config:
        form_attributes = True