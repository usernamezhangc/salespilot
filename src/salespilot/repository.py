from sqlalchemy import or_, select
from salespilot.database import SessionLocal
from salespilot.model import Products, KnowledgeChunk, Orders

def add_product(product: Products):
    with SessionLocal() as db:
        db.add(product)
        db.commit()

def add_knowledge_chunk(chunk: KnowledgeChunk):
    with SessionLocal() as db:
        db.add(chunk)
        db.commit()


def search_products(keyword: str) -> list[Products]:
    """按关键词在 products 表里搜索，返回商品列表（Products 对象）。"""
    with SessionLocal() as db:                     # 开一个数据库会话
        stmt = select(Products).where(
            or_(                                     # 或：任一字段匹配即可
                Products.name.contains(keyword),
                Products.category.contains(keyword),
                Products.description.contains(keyword),
            )
        )
        return db.execute(stmt).scalars().all()    # 执行并取全部结果

def search_knowledge(query_vector: list[float], top_k: int = 3) -> list[KnowledgeChunk]:
    """根据查询向量搜索知识库，返回 top_k 个最相关的知识块。"""
    with SessionLocal() as db:
        stmt = (
            select(KnowledgeChunk)
            .order_by(KnowledgeChunk.embedding.cosine_distance(query_vector))
            .limit(top_k)
        )
        return db.execute(stmt).scalars().all()

def add_order(order: Orders):
    """新增一个订单。"""
    with SessionLocal() as db:
        db.add(order)
        db.commit()

def get_order(order_no: str) -> Orders | None:
    """根据订单号查单个订单，找不到返回 None。"""
    with SessionLocal() as db:
        stmt = select(Orders).where(Orders.order_no == order_no)
        return db.execute(stmt).scalars().first()

def list_orders(user_id: int) -> list[Orders]:
    """列出某个用户的所有订单。"""
    with SessionLocal() as db:
        stmt = select(Orders).where(Orders.user_id == user_id)
        return db.execute(stmt).scalars().all()

def update_order_status(order_no: str, new_status: str) -> bool:
    """把订单状态改成 new_status。更新成功返回 True，订单不存在返回 False。"""
    with SessionLocal() as db:
        order = db.execute(
            select(Orders).where(Orders.order_no == order_no)
        ).scalars().first()
        if not order:
            return False
        order.status = new_status   # 改对象属性
        db.commit()                 # 提交，真正写进数据库
        return True