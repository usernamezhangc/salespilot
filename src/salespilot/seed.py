from salespilot.database import engine, SessionLocal
from salespilot import model
from salespilot.products_data import PRODUCTS 
from salespilot.order_data import ORDERS
from salespilot.model import Products, Orders
from salespilot.repository import add_product, add_order

def seed():
    model.Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        db.query(Products).delete()
        db.query(Orders).delete()
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

    for item in ORDERS:
        order = Orders(
            order_no=item["order_no"],
            user_id=item["user_id"],
            product_id=item["product_id"],
            quantity=item["quantity"],
            total_price=item["total_price"],
            status=item["status"],
        )
        print(f"已添加： {item['order_no']}")
        add_order(order)
    db.commit()

if __name__ == "__main__":
    seed()
