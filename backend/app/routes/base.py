from fastapi import APIRouter
from app.routes import pages

main_router = APIRouter()

main_router.include_router(pages.router)
