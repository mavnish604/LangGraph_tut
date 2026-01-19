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
    
    with st.chat_message("ai"):
        #st.session_state["messages"].append({"role":"ai","content":ai_mess})
        #st.text(ai_mess)
        ai_mess=st.write_stream(
            message_.content for message_,metadata in workflow.stream(
                {"message":[HumanMessage(content=usr_in)]},
                config={"configurable":{"thread_id":"thread_1"}},
                stream_mode="messages"
            )
        )
        st.session_state["messages"].append({"role":"ai","content":ai_mess})


