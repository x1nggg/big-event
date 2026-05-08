from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from utils.dependencies import get_current_user
from models import User
from schemas import BaseResponse
import os
import uuid
import aiofiles

router = APIRouter(tags=["文件上传"])

UPLOAD_DIR = "uploads"

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=BaseResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传文件"""
    # 检查文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        return JSONResponse(
            status_code=400,
            content={"code": 1, "msg": "不支持的文件类型", "data": None}
        )

    # 生成唯一文件名
    file_extension = os.path.splitext(file.filename)[1]
    new_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, new_filename)

    # 保存文件
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)

    # 返回文件访问路径
    file_url = f"/static/{new_filename}"

    return BaseResponse(data=file_url)