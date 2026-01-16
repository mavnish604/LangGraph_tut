from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="openai/gpt-4.1-nano",base_url="https://openrouter.ai/api/v1")

print(model.invoke("hi"))