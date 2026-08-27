import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = "https://api.deepseek.com",
)

def ask_llm(messages: list[dict], tools: list[dict] | None = None) -> str:
    """把一组对话发给 DeepSeek 的 LLM，返回回复的文本"""
    response = client.chat.completions.create(
        model = "deepseek-v4-flash",
        messages = messages,
        tools = tools,
    )
    # 拿到第一段回复的文本内容
    return response.choices[0].message.content
