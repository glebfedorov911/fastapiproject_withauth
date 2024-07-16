from fastapi import APIRouter

from core.config import settings

from .users.views import router as user_router


router = APIRouter(prefix=settings.api)
router.include_router(user_router)