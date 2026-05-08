from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import redis.asyncio as aioredis

# MySQL数据库配置
DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/big_event?charset=utf8mb4"

# SQLAlchemy配置
engine = create_engine(DATABASE_URL.replace('+aiomysql', '+pymysql'), echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis配置
REDIS_URL = "redis://localhost:6379/0"

async def get_redis():
    redis = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()