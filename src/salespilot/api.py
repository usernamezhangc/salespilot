from fastapi import FastAPI
from pydantic import BaseModel

# 引入我们自己写的 llm.py 里的 ask_llm 函数
from salespilot.llm import ask_llm
from salespilot.agent import app as agent_app

app = FastAPI(title="SalesPilot API")

SYSTEM_PROMPT = """你是 SalesPilot 的智能客服助手。你的职责是解答与商品、订单、售后相关的问题。规则：
            1. 只回答与销售/客服相关的内容，其他问题礼貌拒绝。
            2. 回答简洁、专业、友好。
            3. 不知道的信息，诚实说明，不要编造。"""

# 定义"请求长什么样"：必须有一个字符串字段 question
class ChatRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"Message": "Salespilot is alive"}

@app.post("/chat")
def chat(req: ChatRequest):
    # 把用户问题包装成"一条用户消息"
    initial_state = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.question}
        ]
    }
    
    final_state = agent_app.invoke(initial_state)

    return {"answer": final_state["messages"][-1]["content"]}