import sys
sys.stdout.reconfigure(encoding = "utf-8")
import json

from salespilot.llm import client
from salespilot.tools import get_tool_schema, call_tool

MODEL = "deepseek-v4-flash"

def run_agent(user_question: str) -> str:
    messages = [
        {"role": "system", "content": "你是 SalesPilot 的智能客服助手。需要真实商品数据时，使用 search_product 工具查询。"},
        {"role": "user", "content": user_question},
    ]
    tools = get_tool_schema()
    
    for _ in range(10):
        response = client.chat.completions.create(
            model = MODEL,
            messages = messages,
            tools = tools,
        )
        msg = response.choices[0].message
        
        if msg.tool_calls:
            call = msg.tool_calls[0]
            print("[Agent] 要调工具:", call.function.name)
            print("[Agent] 参数:", call.function.arguments)
            result = call_tool(call.function.name, call.function.arguments)
            print("[Agent] 工具结果:", result)
            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result, ensure_ascii=False),
            })
            continue
        return msg.content
    return "超过最大轮次"

if __name__ == "__main__":
    print("最终回答:", run_agent("耳机还有货吗？"))
