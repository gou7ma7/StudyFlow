from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.blog import BlogPost, BlogPostCreate

router = APIRouter(prefix="/blog", tags=["blog"])

@router.get("/", response_model=List[BlogPost])
async def get_blog_posts(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 10
):
    """获取博客文章列表"""
    return []

@router.post("/", response_model=BlogPost)
async def create_blog_post(
    post: BlogPostCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """创建新的博客文章"""
    return post 