from sqlalchemy import or_, select
from salespilot.database import SessionLocal
from salespilot.model import Products, KnowledgeChunk

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

def add_product(product: Products):
    with SessionLocal() as db:
        db.add(product)
        db.commit()

def add_knowledge_chunk(chunk: KnowledgeChunk):
    with SessionLocal() as db:
        db.add(chunk)
        db.commit()

def search_knowledge(query_vector: list[float], top_k: int = 3) -> list[KnowledgeChunk]:
    """根据查询向量搜索知识库，返回 top_k 个最相关的知识块。"""
    with SessionLocal() as db:
        stmt = (
            select(KnowledgeChunk)
            .order_by(KnowledgeChunk.embedding.cosine_distance(query_vector))
            .limit(top_k)
        )
        return db.execute(stmt).scalars().all()
