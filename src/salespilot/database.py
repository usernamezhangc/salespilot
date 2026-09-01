"""数据库连接管理：创建 engine 和 SessionLocal，全局复用一份。"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 读取 .env（和 llm.py 一样）
load_dotenv()

# 从环境变量读取连接串
DATABASE_URL = os.getenv("DATABASE_URL")

# ---- TODO 1：用 create_engine 创建一个 engine（传 DATABASE_URL）----
engine = create_engine(DATABASE_URL)
# ---- TODO 1 end ----

# ---- TODO 2：用 sessionmaker 造一个会话工厂 SessionLocal（bind 到 engine）----
SessionLocal = sessionmaker(bind=engine)
# ---- TODO 2 end ----