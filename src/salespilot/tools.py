"""工具的集合。Tool = 普通函数 + 给模型看的说明书(后面加 Schema)。"""

import json
from sqlalchemy import inspect
from salespilot.service import ProductService, KnowledgeService

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
        }
    ]

def call_tool(name: str, arguments: str) -> list[dict]:
    """根据工具名和参数，调用对应的工具函数。"""
    if name == "search_product":
        args = json.loads(arguments)
        return search_product(args["keyword"])
    elif name == "search_knowledge":
        args = json.loads(arguments)
        return search_knowledge(args["query"])
    else:
        raise ValueError(f"未知工具 {name}")