import streamlit as st
from chatbot_backend import workflow,retrive_threads
from langchain_core.messages import HumanMessage
import uuid


st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    text-align: left;
    padding: 12px 14px;
    border-radius: 12px;
    background: #1f2937;
    color: white;
    border: 1px solid #374151;
    margin-bottom: 8px;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background: #374151;
    border-color: #60a5fa;
}

div.stButton > button:focus {
    background: #2563eb;
    border-color: #2563eb;
}
</style>
""", unsafe_allow_html=True)




def gen_thread():
    thread_id=uuid.uuid4()
    return str(thread_id)

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def reset_convo():
    thread_id=gen_thread()
    st.session_state["thread_id"]=thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["messages"]=[]

def load_convo(thread_id):
    state = workflow.get_state(config={"configurable": {"thread_id": thread_id}})
    if "message" in state.values:
        return state.values["message"]
    else:
        return []



if "messages" not in st.session_state:
    st.session_state["messages"]=[]


if "thread_id" not in st.session_state:
    st.session_state["thread_id"]=gen_thread()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"]=retrive_threads()

add_thread(st.session_state["thread_id"])

st.sidebar.title("LangGraph ChatBot")


if st.sidebar.button("Start a new Conversation"):
    reset_convo()

for thread_id in st.session_state["chat_threads"][::-1]:
    state = workflow.get_state(config={"configurable": {"thread_id": thread_id}})

    if "message" in state.values and len(state.values["message"]) > 0:
        title = state.values["message"][0].content[:40]
    else:
        title = "New Chat"

    if st.sidebar.button(title, key=thread_id):
        st.session_state["thread_id"] = thread_id
        messages = load_convo(thread_id)
        temp = []
        for i in messages:
            role = "user" if isinstance(i, HumanMessage) else "ai"
            temp.append({"role": role, "content": i.content})
        st.session_state["messages"] = temp





# st.sidebar.text(st.session_state["thread_id"])



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


