from typing import  Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Post, Tag, User
from ..database import get_db
from typing import List 
from sqlalchemy.orm import joinedload,selectinload
from typing import Type, Optional, Dict, Any
from fastapi import Depends, HTTPException
from sqlalchemy.orm import selectinload


user_router = APIRouter(prefix="/api") 


async def generic_query(
    model: Type,
    filters: Optional[Dict[str, Any]] = None,
    includes: Optional[List[str]] = None,
    db: AsyncSession = Depends(get_db),
    single: bool = False,
):
    query = select(model)

    # Apply filters
    if filters:
        for key, value in filters.items():
            query = query.filter(getattr(model, key) == value)

    # Apply includes
    if includes:
        for include in includes:
            if include == "tags" and hasattr(model, "tags"):
                query = query.options(selectinload(model.tags))
            if include == "user" and hasattr(model, "post_owner"):
                query = query.options(selectinload(model.post_owner))
            if include == "comments" and hasattr(model, "comments"):
                query = query.options(selectinload(model.comments))
            if include == "posts" and hasattr(model, "posts"):
                query = query.options(selectinload(model.posts))
            if include == "comments" and hasattr(model, "comments"):
                query = query.options(selectinload(model.comments))

    result = await db.execute(query)

    if single:
        item = result.scalars().first()
        if item is None:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        return item

    return result.scalars().all()

@user_router.get("/posts")
async def get_posts(
    status: Optional[str] = Query(None),
    include: Optional[str] = Query(None),  
    db: AsyncSession = Depends(get_db)
):
    filters = {"status": status} if status else {}
    includes = include.split(",") if include else []

    posts = await generic_query(Post, filters=filters, includes=includes, db=db)

    return {
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "status": post.status,
                "tags": [{"id": tag.id, "name": tag.tag_name} for tag in post.tags] if "tags" in includes else None,
                "user": {"id": post.post_owner.id, "username": post.post_owner.username} if "user" in includes else None,
            } for post in posts
        ]
    }

@user_router.get("/posts/{id}")
async def get_post(
    id: int,
    include: Optional[str] = Query(None),  
    db: AsyncSession = Depends(get_db)
):
    includes = include.split(",") if include else []

    post = await generic_query(Post, filters={"id": id}, includes=includes, single=True, db=db)

    post_data = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "status": post.status,
        "tags": [{"id": tag.id, "name": tag.tag_name} for tag in post.tags] if "tags" in includes else None,
        "user": {"id": post.post_owner.id, "username": post.post_owner.username} if "user" in includes else None,
        "comments": [{"id": comment.id, "content": comment.content} for comment in post.comments] if "comments" in includes else None
    }

    return {"post": post_data}

@user_router.get("/users/{id}")
async def get_user(
    id: int,
    include: Optional[str] = Query(None),  
    db: AsyncSession = Depends(get_db)
):
    includes = include.split(",") if include else []

    user = await generic_query(User, filters={"id": id}, includes=includes, single=True,db=db)

    user_data = {
        "id": user.id,
        "username": user.username,
        "posts": [{"id": post.id, "title": post.title, "content": post.content} for post in user.posts] if "posts" in includes else None,
        "comments": [{"id": comment.id, "content": comment.content} for comment in user.comments] if "comments" in includes else None
    }

    return {"user": user_data}


