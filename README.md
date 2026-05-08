# 大事件 - 全栈内容管理系统

课程结业项目，基于 FastAPI + Vue 3 的文章管理系统。

## 环境要求

- Python 3.10+
- Node.js 16+
- MySQL 8.0
- Redis（Windows 可下载 https://github.com/tporadowski/redis/releases ，解压后运行 redis-server.exe）

## 数据库准备

启动 MySQL 后，创建数据库：

```sql
CREATE DATABASE big_event CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

数据表会在后端启动时自动创建，无需手动建表。

MySQL 连接配置在 `backend/database.py` 中，默认配置：

- 地址：localhost:3306
- 用户名：root
- 密码：123456
- 数据库：big_event

如果你的密码不是 123456，需要修改 `backend/database.py` 第 7 行的连接字符串。

## 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

后端运行在 http://localhost:8080

## 启动前端

```bash
cd frontend/big-event

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在 http://localhost:5173，浏览器打开即可使用。

## 启动 Redis

后端依赖 Redis 进行 Token 管理，需要确保 Redis 服务已启动。

```bash
# Windows: 双击 redis-server.exe 或命令行启动
redis-server

# macOS/Linux
redis-server
```

Redis 默认配置为 localhost:6379，如需修改请编辑 `backend/database.py` 第 15 行。

## 注意事项

- 先启动 MySQL 和 Redis，再启动后端，最后启动前端
- 注册账号后即可登录使用
