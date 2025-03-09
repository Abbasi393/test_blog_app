import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from app.core.config import settings
from app.routes import (index_router,  url_router)

app = FastAPI()
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(index_router)
app.include_router(url_router)

logger = logging.getLogger()
logger.info(f'App is running in environment {settings.environment}')
