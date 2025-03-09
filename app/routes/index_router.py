from fastapi import APIRouter

index_router = APIRouter(tags=["index"])


@index_router.get("/")
async def root():
    return {"message": "Hello World"}
