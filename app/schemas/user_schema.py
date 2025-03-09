from pydantic import BaseModel, EmailStr, Field


class UserCreateModel(BaseModel):
    username: str = Field(..., title="Username", description="User's unique username", example="john_doe")
    email: EmailStr = Field(..., title="Email Address", description="Valid user email", example="john@example.com")
    password: str = Field(
        ..., title="Password", description="User password (min 8 characters)", example="securePa$$123"
    )


class UserLoginModel(BaseModel):
    username: str = Field(
        ...,
        title="Username/Email",
        description="User's unique username or email", example="john_doe/john@example.com"
    )
    password: str = Field(
        ..., title="Password", description="User password (min 8 characters)", example="securePa$$123"
    )


class TokenResponseModel(BaseModel):
    access_token: str
    token_type: str
