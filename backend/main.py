from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import user, article, upload
import os

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(title="大事件API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vue前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
os.makedirs("uploads", exist_ok=True)

# 挂载静态文件目录（仅用于访问上传的文件）
app.mount("/static", StaticFiles(directory="uploads"), name="static")

# 注册路由
app.include_router(user.router, prefix="/api")
app.include_router(article.router, prefix="/api")
app.include_router(upload.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "大事件API服务运行中"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)