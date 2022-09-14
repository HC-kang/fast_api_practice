from fastapi import APIRouter

from app.api.api_v1.endpoints import branch, auth


api_router = APIRouter()
api_router.include_router(branch.router, prefix="/branches", tags=["branches"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
