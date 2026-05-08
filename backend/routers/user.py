from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import redis.asyncio as aioredis
from typing import Optional
from schemas import *
from models import User
from utils.auth import verify_password, get_password_hash, create_token
from database import get_db, get_redis
from datetime import timedelta

router = APIRouter(prefix="/user", tags=["用户管理"])


# ========== 获取当前用户的依赖函数（只定义一次）==========
async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis)
) -> User:
    """从请求头中获取token并返回当前用户"""
    if not authorization:
        raise HTTPException(status_code=401, detail="请先登录")

    token = authorization
    username = await redis.get(f"token:{token}")

    if not username:
        raise HTTPException(status_code=401, detail="请先登录")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")

    return user


# ========== 路由定义 ==========

@router.post("/register", response_model=BaseResponse)
async def register(register_data: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
    existing_user = db.query(User).filter(User.username == register_data.username).first()
    if existing_user:
        return BaseResponse(code=1, msg="用户名已存在", data=None)

    hashed_password = get_password_hash(register_data.password)
    new_user = User(
        username=register_data.username,
        password=hashed_password,
        nickname=register_data.username
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return BaseResponse(msg="注册成功", data=None)


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin, db: Session = Depends(get_db), redis: aioredis.Redis = Depends(get_redis)):
    """用户登录"""
    user = db.query(User).filter(User.username == login_data.username).first()

    if not user or not verify_password(login_data.password, user.password):
        return BaseResponse(code=1, msg="用户名或密码错误", data=None)

    token = create_token(user.username)
    await redis.setex(f"token:{token}", timedelta(hours=24), user.username)

    return TokenResponse(msg="登录成功", data=token)


@router.get("/userinfo", response_model=BaseResponse)
async def get_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取用户详细信息"""
    user_info = UserInfo(
        id=current_user.id,
        username=current_user.username,
        nickname=current_user.nickname,
        email=current_user.email,
        user_pic=current_user.user_pic,
        create_time=current_user.create_time,
        update_time=current_user.update_time
    )
    return BaseResponse(data=user_info.model_dump())


@router.put("/update", response_model=BaseResponse)
async def update_user_info(
    user_info_data: UserInfoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改个人信息"""
    if user_info_data.nickname:
        current_user.nickname = user_info_data.nickname
    if user_info_data.email:
        current_user.email = user_info_data.email

    db.commit()
    return BaseResponse(msg="修改成功", data=None)


@router.patch("/updateAvatar", response_model=BaseResponse)
async def update_avatar(
    avatar_data: UserAvatarUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改用户头像"""
    current_user.user_pic = avatar_data.avatarUrl
    db.commit()
    return BaseResponse(msg="修改成功", data=None)


@router.patch("/updatePwd", response_model=BaseResponse)
async def update_password(
    pwd_data: UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis)
):
    """修改用户密码"""
    if not verify_password(pwd_data.old_pwd, current_user.password):
        return BaseResponse(code=1, msg="原密码不正确", data=None)

    if pwd_data.new_pwd != pwd_data.re_pwd:
        return BaseResponse(code=1, msg="两次新密码输入不一致", data=None)

    current_user.password = get_password_hash(pwd_data.new_pwd)
    db.commit()

    return BaseResponse(msg="修改成功,请重新登录", data=None)


@router.post("/logout", response_model=BaseResponse)
async def logout(
    authorization: Optional[str] = Header(None),
    redis: aioredis.Redis = Depends(get_redis)
):
    """退出登录"""
    if authorization:
        await redis.delete(f"token:{authorization}")
    return BaseResponse(msg="退出登录成功", data=None)