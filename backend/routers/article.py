from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from schemas import *
from models import User, Category, Article
from database import get_db
from utils.dependencies import get_current_user
from sqlalchemy import desc

router = APIRouter(tags=["文章管理"])

# ==================== 分类管理 ====================

@router.get("/category", response_model=BaseResponse)
async def get_category_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文章分类列表"""
    categories = db.query(Category).filter(Category.create_user == current_user.id).all()

    category_list = []
    for cat in categories:
        category_list.append({
            "id": cat.id,
            "categoryName": cat.category_name,
            "categoryAlias": cat.category_alias,
            "createTime": cat.create_time.isoformat() if cat.create_time else None,
            "updateTime": cat.update_time.isoformat() if cat.update_time else None
        })

    return BaseResponse(data=category_list)

@router.post("/category", response_model=BaseResponse)
async def add_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """添加文章分类"""
    new_category = Category(
        category_name=category_data.categoryName,
        category_alias=category_data.categoryAlias,
        create_user=current_user.id
    )
    db.add(new_category)
    db.commit()

    return BaseResponse(msg="添加成功", data=None)

@router.put("/category", response_model=BaseResponse)
async def update_category(
    category_data: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改文章分类"""
    category = db.query(Category).filter(
        Category.id == category_data.id,
        Category.create_user == current_user.id
    ).first()

    if not category:
        return BaseResponse(code=1, msg="分类不存在", data=None)

    category.category_name = category_data.categoryName
    category.category_alias = category_data.categoryAlias
    db.commit()

    return BaseResponse(msg="修改成功", data=None)

@router.delete("/category", response_model=BaseResponse)
async def delete_category(
    id: int = Query(..., description="分类ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除文章分类"""
    category = db.query(Category).filter(
        Category.id == id,
        Category.create_user == current_user.id
    ).first()

    if not category:
        return BaseResponse(code=1, msg="分类不存在", data=None)

    db.delete(category)
    db.commit()

    return BaseResponse(msg="删除成功", data=None)

# ==================== 文章管理 ====================

@router.get("/article", response_model=BaseResponse)
async def get_article_list(
    pageNum: int = Query(1, ge=1),
    pageSize: int = Query(3, ge=1, le=50),
    categoryId: Optional[int] = Query(None),
    state: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文章列表"""
    query = db.query(Article).filter(Article.create_user == current_user.id)

    if categoryId:
        query = query.filter(Article.category_id == categoryId)
    if state:
        query = query.filter(Article.state == state)

    # 计算总数
    total = query.count()

    # 分页
    articles = query.order_by(desc(Article.create_time)).offset(
        (pageNum - 1) * pageSize
    ).limit(pageSize).all()

    article_list = []
    for art in articles:
        article_list.append({
            "id": art.id,
            "title": art.title,
            "content": art.content,
            "coverImg": art.cover_img,
            "state": art.state,
            "categoryId": art.category_id,
            "createTime": art.create_time.isoformat() if art.create_time else None,
            "updateTime": art.update_time.isoformat() if art.update_time else None
        })

    return BaseResponse(data={
        "total": total,
        "items": article_list
    })

@router.post("/article", response_model=BaseResponse)
async def add_article(
    article_data: ArticleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """添加文章"""
    new_article = Article(
        title=article_data.title,
        content=article_data.content,
        cover_img=article_data.coverImg,
        state=article_data.state,
        category_id=article_data.categoryId,
        create_user=current_user.id
    )
    db.add(new_article)
    db.commit()

    return BaseResponse(msg="添加成功", data=None)

@router.put("/article", response_model=BaseResponse)
async def update_article(
    article_data: ArticleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改文章"""
    article = db.query(Article).filter(
        Article.id == article_data.id,
        Article.create_user == current_user.id
    ).first()

    if not article:
        return BaseResponse(code=1, msg="文章不存在", data=None)

    article.title = article_data.title
    article.content = article_data.content
    article.cover_img = article_data.coverImg
    article.state = article_data.state
    article.category_id = article_data.categoryId
    db.commit()

    return BaseResponse(msg="修改成功", data=None)

@router.delete("/article", response_model=BaseResponse)
async def delete_article(
    id: int = Query(..., description="文章ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除文章"""
    article = db.query(Article).filter(
        Article.id == id,
        Article.create_user == current_user.id
    ).first()

    if not article:
        return BaseResponse(code=1, msg="文章不存在", data=None)

    db.delete(article)
    db.commit()

    return BaseResponse(msg="删除成功", data=None)