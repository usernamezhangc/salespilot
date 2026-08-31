import sys
sys.stdout.reconfigure(encoding="utf-8")

from langgraph.graph import StateGraph, START, END
from salespilot.llm import ask_llm

from typing import TypedDict

class ChatMessage(TypedDict):
    role: str
    content: str

class AgentState(TypedDict):
    messages: list[ChatMessage]

from salespilot.tools import get_tool_schema, call_tool

import json

def agent_node(state: AgentState) -> dict:
    print("--- 走到 agent 节点 ---")
    messages = state["messages"]
    tools = get_tool_schema()
    result = ask_llm(messages, tools)

    if result.tool_calls:
        # 把模型想调工具的"宣布"放进消息，返回给 tools 节点处理
        messages.append({
            "role": "assistant",
            "content": result.content or "",
            "tool_calls": [
                {"id": c.id, "type": "function",
                 "function": {"name": c.function.name,"arguments": c.function.arguments}}
                for c in result.tool_calls
            ],
        })
        return {"messages": messages}
    # 没有工具调用：直接返回文本
    return {"messages": messages + [{"role": "assistant", "content": result.content}]}
   
def tools_node(state: AgentState) -> dict:
    print("---走到 tools 节点 ---")
    messages = state["messages"]
    last_assistant = messages[-1]
    new_messages = []
    for call in last_assistant["tool_calls"]:
        tool_result = call_tool(call["function"]["name"], call["function"]["arguments"])
        print("工具结果:", tool_result)
        new_messages.append({
            "role": "tool",
            "tool_call_id": call["id"],
            "content": json.dumps(tool_result, ensure_ascii=False),
        })
    return {"messages": messages + new_messages}
    
def route_after_agent(state: AgentState) -> str:
    """路由函数：看最后一条 assistant 消息有没有工具调用"""
    last = state["messages"][-1]
    if last.get("tool_calls"):
        return "tools"
    return "END"

# 3. 建图
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tools_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", route_after_agent, {"tools": "tools", "END": END})
graph.add_edge("tools", "agent")

app = graph.compile()

if __name__ == "__main__":
    print(app.get_graph().draw_mermaid())
    result = app.invoke({"messages": [{"role": "user", "content": "帮我查一下耳机还有货吗？"}]})
    print("最终结果：", result)