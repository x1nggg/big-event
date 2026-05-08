from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
import redis.asyncio as aioredis
from database import get_db, get_redis
from models import User

async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis)
) -> User:
    """获取当前登录用户"""
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