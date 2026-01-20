import streamlit as st
from chat_bot_backend import workflow
from langchain_core.messages import HumanMessage
import uuid

def gen_thread():
    thread_id=uuid.uuid4()
    return thread_id

def reset_convo():
    thread_ig=gen_thread()
    st.session_state["thread_id"]
    st.session_state["messages"]=[]

if "messages" not in st.session_state:
    st.session_state["messages"]=[]

if "thread_id" not in st.session_state:
    st.session_state["thread_id"]=gen_thread()


st.sidebar.title("LangGraph ChatBot")
if st.sidebar.button("Start a new Conversation"):
    reset_convo()
st.sidebar.header("Previous conversations")
st.sidebar.text(st.session_state["thread_id"])



CONFIG={"configurable":{"thread_id":st.session_state["thread_id"]}}


usr_in=st.chat_input("type here: ")

for i in st.session_state["messages"]:
    with st.chat_message(i["role"]):
        st.text(i["content"])



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
                config=CONFIG,
                stream_mode="messages"
            )
        )
        st.session_state["messages"].append({"role":"ai","content":ai_mess})


