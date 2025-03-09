from contextlib import contextmanager

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class Settings(BaseSettings):
    environment: str = None
    version: str = None


class BlogPostSettings(Settings):
    base_url: str = None
    api_url_prefix: str = None
    database_url: str = None
    secret_key: str = None
    algorithm: str = None
    access_token_expire_minutes: int = None

    model_config = SettingsConfigDict(env_file='.env')

    def get_engine(self):
        try:
            assert self.database_url
            return create_engine(self.database_url)
        except AssertionError as e:
            print(e)

    @staticmethod
    def get_session(db_engine):
        return scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
        )


settings = BlogPostSettings()

engine = settings.get_engine()


@contextmanager
def get_session_ctx():
    db_session = settings.get_session(db_engine=engine)
    try:
        yield db_session
    finally:
        db_session.remove()


def get_session():
    with get_session_ctx() as db:
        yield db
