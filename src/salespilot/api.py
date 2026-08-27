from fastapi import FastAPI
from pydantic import BaseModel

# 引入我们自己写的 llm.py 里的 ask_llm 函数
from salespilot.llm import ask_llm

app = FastAPI(title="SalesPilot API")

# 定义"请求长什么样"：必须有一个字符串字段 question
class ChatRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"Message": "Salespilot is alive"}

@app.post("/chat")
def chat(req: ChatRequest):
# system：给模型"入职培训"——身份、职责、纪律
    system_prompt = """你是 SalesPilot 的智能客服助手。你的职责是解答与商品、订单、售后相关的问题。规则：
            1. 只回答与销售/客服相关的内容，其他问题礼貌拒绝。
            2. 回答简洁、专业、友好。
            3. 不知道的信息，诚实说明，不要编造。"""    

    # 把用户问题包装成"一条用户消息"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": req.question}
        ]
    # 调 LLM，拿到回答
    answer = ask_llm(messages)
    # 返回给浏览器
    return {"answer": answer}