from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import HumanMessage,BaseMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

model=ChatOpenAI(model="openai/gpt-4.1-nano",base_url="https://openrouter.ai/api/v1")

class ChatBot(TypedDict):
    message:Annotated[list[BaseMessage],add_messages] #add_message is reducer fn like operator.add but is buit in langgraph for spec. purpose


def chat_node(state:ChatBot)->ChatBot:
    messages=state["message"]
    state["message"]=[model.invoke(messages)]
    return state

checkpoint=MemorySaver()

graph = StateGraph(ChatBot)

graph.add_node("chat_node",chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

workflow=graph.compile(checkpointer=checkpoint)

