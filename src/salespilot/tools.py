"""工具的集合。Tool = 普通函数 + 给模型看的说明书(后面加 Schema)。"""

import json

from salespilot.products_data import PRODUCTS

def search_product(keyword: str) -> list[dict]:
    """按关键词在商品数据里模糊搜索，返回匹配的商品列表。"""
    results = []
    for product in PRODUCTS:
        haystack = f"{product['name']} {product['category']} {product['description']}"
        if keyword in haystack:
            results.append(product)
    return results

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