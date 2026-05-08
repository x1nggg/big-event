from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ==================== 用户相关Schema ====================

class UserRegister(BaseModel):
    username: str = Field(..., min_length=5, max_length=16)
    password: str = Field(..., min_length=5, max_length=16)
    rePassword: Optional[str] = None


class UserLogin(BaseModel):
    username: str = Field(..., min_length=5, max_length=16)
    password: str = Field(..., min_length=5, max_length=16)


class UserInfoUpdate(BaseModel):
    id: Optional[int] = None
    nickname: Optional[str] = Field(None, max_length=10)
    email: Optional[str] = None


class UserAvatarUpdate(BaseModel):
    avatarUrl: str


class UserPasswordUpdate(BaseModel):
    old_pwd: str = Field(..., min_length=6, max_length=16)
    new_pwd: str = Field(..., min_length=6, max_length=16)
    re_pwd: str = Field(..., min_length=6, max_length=16)


class UserInfo(BaseModel):
    id: int
    username: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    user_pic: Optional[str] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== 分类相关Schema ====================

class CategoryCreate(BaseModel):
    categoryName: str = Field(..., min_length=1, max_length=10)
    categoryAlias: str = Field(..., min_length=1, max_length=15)


class CategoryUpdate(BaseModel):
    id: int
    categoryName: str = Field(..., min_length=1, max_length=10)
    categoryAlias: str = Field(..., min_length=1, max_length=15)


class CategoryResponse(BaseModel):
    id: int
    categoryName: str
    categoryAlias: str
    createTime: Optional[datetime] = None
    updateTime: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== 文章相关Schema ====================

class ArticleCreate(BaseModel):
    title: Optional[str] = ''
    content: Optional[str] = ''
    coverImg: Optional[str] = ''
    state: Optional[str] = '草稿'
    categoryId: Optional[int] = None


class ArticleUpdate(BaseModel):
    id: int
    title: Optional[str] = ''
    content: Optional[str] = ''
    coverImg: Optional[str] = ''
    state: Optional[str] = '草稿'
    categoryId: Optional[int] = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    coverImg: Optional[str] = ''
    state: str
    categoryId: Optional[int] = None
    createTime: Optional[datetime] = None
    updateTime: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== 通用响应Schema ====================

class BaseResponse(BaseModel):
    code: int = 0
    msg: str = 'success'
    data: dict | list | str | None = None


class TokenResponse(BaseModel):
    code: int = 0
    msg: str = 'success'
    data: Optional[str] = None