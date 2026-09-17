from salespilot.repository import search_products, search_knowledge, get_order, list_orders, update_order_status, create_approval_request, get_approval_request, update_approval_status
from salespilot.embedding import embed_text
from salespilot.model import ApprovalRequest
import json

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

class ApprovalService:
    def create_request(self, user_id: int, action_type: str, action_args: dict):
        """发起一条待审批的请求。action_args 是危险操作的实际参数，这里先记账，不执行。"""
        req = ApprovalRequest(
            user_id=user_id,
            action_type=action_type,
            action_args=json.dumps(action_args, ensure_ascii=False),  # dict 转 JSON 文本再入库
            status="pending",
        )
        create_approval_request(req)
        return req

    def execute(self, action_type: str, action_args: str) -> str:
        """审批通过后，根据操作类型真正执行危险操作。action_args 是存库的 JSON 文本。"""
        args = json.loads(action_args)          # JSON 文本转回 dict
        if action_type == "cancel_order":
            # 真正取消订单：复用的是 OrderService 里的状态校验逻辑
            return OrderService().cancel_order(args["order_no"])   
        return f"未知的操作类型: {action_type}"

    def decide(self, request_id: int, approve: bool, note: str = ""):
        """审批人处置：批准则调用 execute()，拒绝则只改状态。返回 (结果文本, 是否执行了)。"""
        req = get_approval_request(request_id)
        if not req:
            return "审批请求不存在", False
        if req.status != "pending":
            return f"该请求已是 {req.status} 状态，不能重复审批", False

        if approve:
            update_approval_status(request_id, "approved", note)
            result = self.execute(req.action_type, req.action_args)
            return f"已批准并执行：{result}", True
        else:
            update_approval_status(request_id, "rejected", note)
            return "已拒绝，未执行", False