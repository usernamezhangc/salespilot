from sqlalchemy import or_, select
from salespilot.database import SessionLocal
from salespilot.model import Products

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