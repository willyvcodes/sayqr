from fastapi import APIRouter, HTTPException, status, Depends
from uuid import uuid4
from datetime import datetime, timezone
from db import db, User
from pydantic import BaseModel, Field
from typing import Optional, List
from routes.users import current_active_user

router = APIRouter()


class PageCreateSchema(BaseModel):
    content: str
    images: Optional[list[str]] = []


class PageUpdateSchema(BaseModel):
    content: Optional[str] = None
    images: Optional[list[str]] = None


class PageResponseSchema(BaseModel):
    id: str = Field(..., alias="_id")
    content: str
    images: Optional[list[str]] = []
    created_at: datetime
    user_id: str


@router.post(
    "/api/page/", response_model=PageResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_page(
    page: PageCreateSchema, user: User = Depends(current_active_user)
):
    try:
        page_id = str(uuid4())
        new_page = {
            "_id": page_id,
            "content": page.content,
            "images": page.images or [],
            "created_at": datetime.now(timezone.utc),
            "user_id": str(user.id),
        }
        await db.pages.insert_one(new_page)
        return new_page
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/api/page/{page_id}", response_model=PageResponseSchema)
async def update_page_content(
    page_id: str,
    updated_page: PageUpdateSchema,
    user: User = Depends(current_active_user),
):
    existing_page = await db.pages.find_one({"_id": page_id})
    if not existing_page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Page with ID: {page_id} not found",
        )

    if existing_page.get("user_id") != str(user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this page",
        )

    page_data = {}
    if updated_page.content is not None:
        page_data["content"] = updated_page.content
    if updated_page.images is not None:
        page_data["images"] = updated_page.images

    try:
        result = await db.pages.update_one({"_id": page_id}, {"$set": page_data})
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail=f"Page with ID: {page_id} was not updated",
            )

        updated_page = await db.pages.find_one({"_id": page_id})
        return updated_page
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/api/pages/my", response_model=List[PageResponseSchema])
async def get_my_pages(user: User = Depends(current_active_user)):
    try:
        pages = await db.pages.find({"user_id": str(user.id)}).to_list(length=None)
        return pages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/api/page/{page_id}")
async def delete_page(page_id: str, user: User = Depends(current_active_user)):
    try:
        page = await db.pages.find_one({"_id": page_id})
        if not page:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )

        if str(page["user_id"]) != str(user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this page",
            )

        await db.pages.delete_one({"_id": page_id})
        return {"message": "Page deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
