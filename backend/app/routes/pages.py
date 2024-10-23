from fastapi import APIRouter, HTTPException, status
from uuid import uuid4
from datetime import datetime, timezone
from app.db import db
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()


class PageCreateSchema(BaseModel):
    content: str


class PageUpdateSchema(BaseModel):
    content: Optional[str] = None
    qr_code: Optional[str] = None


class PageResponseSchema(BaseModel):
    id: str = Field(..., alias="_id")
    content: str
    qr_code: Optional[str] = None
    created_at: datetime


@router.post(
    "/api/page/", response_model=PageResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_page(page: PageCreateSchema):
    try:
        page_id = str(uuid4())
        new_page = {
            "_id": page_id,
            "content": page.content,
            "created_at": datetime.now(timezone.utc),
            "qr_code": None,
        }
        await db.pages.insert_one(new_page)
        return new_page
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {e}",
        )


@router.get("/api/page/{id}", response_model=PageResponseSchema)
async def get_page_by_id(id: str):
    try:
        page = await db.pages.find_one({"_id": id})
        if not page:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )
        return page
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {e}",
        )


@router.put("/api/page/{page_id}/content", response_model=PageResponseSchema)
async def update_page_content(page_id: str, content: str):
    try:
        result = await db.pages.update_one(
            {"_id": page_id}, {"$set": {"content": content}}
        )
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )

        updated_page = await db.pages.find_one({"_id": page_id})
        return updated_page
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {e}",
        )


@router.put("/api/page/{page_id}/qr_code", response_model=PageResponseSchema)
async def update_qr_code(page_id: str, qr_code: str):
    try:
        result = await db.pages.update_one(
            {"_id": page_id}, {"$set": {"qr_code": qr_code}}
        )
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )

        updated_page = await db.pages.find_one({"_id": page_id})
        return updated_page
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {e}",
        )
