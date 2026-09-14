from salespilot.database import engine, SessionLocal
from salespilot import model
from salespilot.products_data import PRODUCTS 
from salespilot.model import Products
from salespilot.repository import add_product

def seed():
    model.Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        db.query(Products).delete()
        db.commit()
    for item in PRODUCTS:
        product = Products(
            name=item["name"],
            price=item["price"],
            stock=item["stock"],
            category=item["category"],
            description=item["description"],
        )
        print(f"已添加： {item['name']}")
        add_product(product)

if __name__ == "__main__":
    seed()
