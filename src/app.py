from dotenv import load_dotenv ## loads API keys
from langchain_core.messages import HumanMessage, AIMessage ## schema for messages
import streamlit as st ## provides pre-built chatbot UI

load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
st.set_page_config(page_title="AI Chat Bot", page_icon=":sparkler:")

st.title("SimSamTra Bot")

## conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

user_query = st.chat_input("Your Query")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        ai_response = "AI responds ... just wait"
        st.markdown(ai_response)
    
    st.session_state.chat_history.append(AIMessage(ai_response))