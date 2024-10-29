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


class PageResponseSchema(BaseModel):
    id: str = Field(..., alias="_id")
    content: str
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


@router.put("/api/page/{page_id}", response_model=PageResponseSchema)
async def update_page_content(page_id: str, updated_page: PageUpdateSchema):
    page_data = {"content": updated_page.content}
    try:
        result = await db.pages.update_one({"_id": page_id}, {"$set": page_data})
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Page with ID: {page_id} not found",
            )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail=f"Page with ID: {page_id} was not updated",
            )

        updated_page = await db.pages.find_one({"_id": page_id})
        return updated_page
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {e}",
        )
