"""工具的集合。Tool = 普通函数 + 给模型看的说明书(后面加 Schema)。"""

import json
import time
from sqlalchemy import inspect
from salespilot.service import ProductService, KnowledgeService, OrderService, ApprovalService

def search_product(keyword: str) -> list[dict]:
    ps = ProductService()
    return [
        { c.key: getattr(p, c.key) for c in inspect(p).mapper.column_attrs }  # 把每个 p 转成 dict
        for p in ps.search_product(keyword)                                 # 遍历 service 返回的商品
    ]

def search_knowledge(query: str) -> list[dict]:
    """语义检索客服知识库，返回最相关的知识块。"""
    ks = KnowledgeService()
    chunks = ks.search(query)
    # 只给模型 title 和 content，embedding 向量没必要塞给 LLM
    return [{"title": c.title, "content": c.content} for c in chunks]

def _order_to_dict(order) -> dict:
    """把 Orders 对象转成 dict，并把 datetime 转成字符串。"""
    d = {c.key: getattr(order, c.key) for c in inspect(order).mapper.column_attrs}
    d["created_at"] = d["created_at"].isoformat()   # datetime 对象 json.dumps 会报错，转成字符串
    return d

def get_order(order_no: str):
    """按订单号查单个订单，找不到返回 None。"""
    order = OrderService().get_order(order_no)
    if order is None:
        return None
    return _order_to_dict(order)

def list_orders(user_id: int) -> list[dict]:
    """列出某个用户的所有订单。"""
    return [_order_to_dict(o) for o in OrderService().list_orders(user_id)]

def cancel_order(order_no: str) -> str:
    """取消订单（内部会做状态校验）。"""
    return OrderService().cancel_order(order_no)

def submit_for_approval(user_id: int, action_type: str, action_args: str) -> str:
    """登记一条待审批的请求，暂不执行。action_args 是危险操作的参数（JSON 字符串）。"""
    # 参数是 LLM 给的 JSON 字符串，转成 dict 交给 service
    args = json.loads(action_args)
    req = ApprovalService().create_request(user_id, action_type, args)
    return f"审批请求已提交，编号 {req.id}，待人工审批。"

def decide_approval(request_id: int, approve: bool, note: str = "") -> str:
    """审批人处置一条待审批请求：approve=True 同意并执行，approve=False 拒绝不执行。"""
    result, executed = ApprovalService().decide(request_id, approve, note)
    return f"{result}（执行与否：{executed}）"

def get_tool_schema() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": "search_product",
                "description": "按关键词在商品数据里模糊搜索，返回匹配的商品列表。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "要搜索的商品关键词,如耳机"
                        },
                    },
                    "required": ["keyword"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_knowledge",
                "description": "在客服知识库中按语义搜索，返回与问题最相关的知识条目（含标题和正文）。用于解答退货、保修、发货、物流、支付、发票、会员、售后等政策类问题。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "用户的问题，如：键盘坏了找谁处理"
                        },
                    },
                    "required": ["query"]
                }
            }
        },
                {
            "type": "function",
            "function": {
                "name": "get_order",
                "description": "根据订单号查询单个订单的详细信息。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_no": {
                            "type": "string",
                            "description": "要查询的订单号，如 ORD20260916001"
                        },
                    },
                    "required": ["order_no"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_orders",
                "description": "列出某个用户的所有订单。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "用户的 ID"
                        },
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "cancel_order",
                "description": "取消一个订单。注意：只有待付款(pending)或已付款(paid)的订单才能取消，已发货、已完成、已取消的订单无法取消。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_no": {
                            "type": "string",
                            "description": "要取消的订单号"
                        },
                    },
                    "required": ["order_no"]
                }
            }
        },        
        {
            "type": "function",
            "function": {
                "name": "submit_for_approval",
                "description": "发起一项需要人工审批的危险操作。适合取消订单等高风险操作：先登记审批请求，等审批通过才真正执行。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "发起操作的用户 ID"},
                        "action_type": {"type": "string", "description": "操作类型，目前仅支持 cancel_order"},
                        "action_args": {"type": "string", "description": "操作参数 JSON，如 {\"order_no\": \"ORD20260916001\"}"},
                    },
                    "required": ["user_id", "action_type", "action_args"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "decide_approval",
                "description": "审批人处置一条待审批请求。同意则真正执行该操作，拒绝则不执行。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "request_id": {"type": "integer", "description": "审批请求的编号 id"},
                        "approve": {"type": "boolean", "description": "true 表示同意，false 表示拒绝"},
                        "note": {"type": "string", "description": "审批备注，可留空"},
                    },
                    "required": ["request_id", "approve"]
                }
            }
        },

    ]

def call_tool(name: str, arguments: str) -> list[dict]:
    """根据工具名和参数，调用对应的工具函数。"""
    if name == "search_product":
        args = json.loads(arguments)
        return search_product(args["keyword"])
    elif name == "search_knowledge":
        args = json.loads(arguments)
        return search_knowledge(args["query"])
    elif name == "get_order":
        args = json.loads(arguments)
        return get_order(args["order_no"])
    elif name == "list_orders":
        args = json.loads(arguments)
        return list_orders(args["user_id"])
    elif name == "cancel_order":
        args = json.loads(arguments)
        return cancel_order(args["order_no"])
    elif name == "submit_for_approval":
        args = json.loads(arguments)
        return submit_for_approval(args["user_id"], args["action_type"], args["action_args"])
    elif name == "decide_approval":
        args = json.loads(arguments)
        return decide_approval(args["request_id"], args["approve"], args.get("note", ""))
    else:
        raise ValueError(f"未知工具 {name}")