from fastapi import APIRouter

from app.api.api_v1.endpoints import recipe, auth, branch


api_router = APIRouter()
# api_router.include_router(recipe.router, prefix="/recipes", tags=["recipes"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(branch.router, prefix="/branches", tags=["branches"])
