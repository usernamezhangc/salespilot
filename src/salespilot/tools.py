"""工具的集合。Tool = 普通函数 + 给模型看的说明书(后面加 Schema)。"""

import json
from sqlalchemy import inspect
from salespilot.service import ProductService

def search_product(keyword: str) -> list[dict]:
    ps = ProductService()
    return [
    {c.key: getattr(p, c.key) for c in inspect(p).mapper.column_attrs}  # 把每个 p 转成 dict
    for p in ps.search_product(keyword)                                 # 遍历 service 返回的商品
]

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
        }
    ]

def call_tool(name: str, arguments: str) -> list[dict]:
    """根据工具名和参数，调用对应的工具函数。"""
    if name == "search_product":
        args = json.loads(arguments)
        return search_product(args["keyword"])
    else:
        raise ValueError(f"未知工具 {name}")