from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
import uuid

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_token(username: str) -> str:
    return uuid.uuid4().hex

def decode_token(token: str) -> str:
    """简化版：直接返回token，实际应从Redis查询"""
    return token