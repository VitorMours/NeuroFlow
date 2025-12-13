from fastapi import APIRouter 
from .routes import email_routes
router = APIRouter(prefix="/api/v1")


router.include_router(email_routes.router, tags=["Email"])