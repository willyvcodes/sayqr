from fastapi import APIRouter
from routes import pages, auth

main_router = APIRouter()
main_router.include_router(auth.router)
main_router.include_router(pages.router)
