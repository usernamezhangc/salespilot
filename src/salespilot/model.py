from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Text, DateTime
from pgvector.sqlalchemy import Vector
import datetime

class Base(DeclarativeBase):
    pass

class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list] = mapped_column(Vector(768))

class Orders(Base):
    __tablename__ = "orders"
    # 主键：数据库自动生成的自增 id
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # 订单号：给人看的编号，如 "ORD20260916001"，业务上用来查单
    order_no: Mapped[str] = mapped_column(String(50))
    # 下单用户 id（先不建外键关联，保持简单）
    user_id: Mapped[int] = mapped_column(Integer)
    # 买的商品 id，对应 products 表的 id
    product_id: Mapped[int] = mapped_column(Integer)
    # 购买数量
    quantity: Mapped[int] = mapped_column(Integer)
    # 总价 = 单价 × 数量（这里直接存算好的结果）
    total_price: Mapped[float] = mapped_column(Float)
    # 订单状态：pending / paid / shipped / completed / cancelled
    status: Mapped[str] = mapped_column(String(20))
    # 下单时间：默认取当前时间，不手动传也行
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )