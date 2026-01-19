import streamlit as st
from chat_bot_backend import workflow
from langchain_core.messages import HumanMessage

if "messages" not in st.session_state:
    st.session_state["messages"]=[]

usr_in=st.chat_input("type here: ")

for i in st.session_state["messages"]:
    with st.chat_message(i["role"]):
        st.text(i["content"])

thread_id="1"

if usr_in:
    with st.chat_message("user"):
        st.session_state["messages"].append({"role":"user","content":usr_in})
        st.text(usr_in)
    
    res=workflow.invoke({"message":[HumanMessage(content=usr_in)]},config={"configurable":{"thread_id":thread_id}})
    ai_mess=res["message"][-1].content
    with st.chat_message("ai"):
        st.session_state["messages"].append({"role":"ai","content":ai_mess})
        st.text(ai_mess)