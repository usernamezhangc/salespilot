from salespilot.repository import search_products, search_knowledge, get_order, list_orders, update_order_status
from salespilot.embedding import embed_text

class ProductService:
    def search_product(self, keyword:str) -> list:
        return search_products(keyword)

class KnowledgeService:
    def search(self, query: str, top_k: int = 3) -> list:
        vec = embed_text(query)
        return search_knowledge(vec, top_k)

class OrderService:
    def get_order(self, order_no: str):
        return get_order(order_no)

    def list_orders(self, user_id: int):
        return list_orders(user_id)

    def cancel_order(self, order_no: str):
        order = self.get_order(order_no)
        if not order:
            return "订单不存在"
        elif order.status == "shipped" or order.status == "completed":
            return "订单已发货/已完成，无法取消"
        elif order.status == "cancelled":
            return "订单已经是取消状态"
        else:
            update_order_status(order_no, "cancelled")
            return "订单已取消"
