import pytest
from sqlalchemy.orm import Session
from tests.config import client
from app.core.config import get_session
from app.schemas.posts_schema import PostCreateModel
from app.services.post_service import PostService
from app.models.user_models import User


@pytest.fixture(scope="function")
def session():
    db_generator = get_session()
    db = next(db_generator)
    try:
        yield db
    finally:
        next(db_generator, None)


@pytest.fixture
def auth_headers():
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpassword"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_user(session: Session):
    user = User(username="testuser", email="testuser@example.com", hashed_password="hashedpassword")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def test_post(session: Session, test_user: User):
    post_data = PostCreateModel(title="Test Post", content="Test Content")
    post = PostService.create_blog_post(session, test_user.id, post_data)
    return post


def test_create_post(auth_headers):
    response = client.post("/blog/posts/", json={
        "title": "New Post",
        "content": "This is a new post."
    }, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Post"
    assert data["content"] == "This is a new post."


def test_get_post(auth_headers, test_post):
    response = client.get(f"/blog/posts/{test_post.id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_post.title
    assert data["content"] == test_post.content


def test_update_post(auth_headers, test_post):
    response = client.put(f"/blog/posts/{test_post.id}", json={
        "title": "Updated Title",
        "content": "Updated Content"
    }, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated Content"


def test_delete_post(auth_headers, test_post):
    response = client.delete(f"/blog/posts/{test_post.id}", headers=auth_headers)

    assert response.status_code == 200

    get_response = client.get(f"/blog/posts/{test_post.id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_list_posts(auth_headers, test_post):
    response = client.get("/blog/posts/", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(post["title"] == test_post.title for post in data)
