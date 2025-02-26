from dotenv import load_dotenv ## loads API keys
from langchain_core.messages import HumanMessage, AIMessage ## schema for messages
from langchain_core.prompts import ChatPromptTemplate ## Chat Prompt Template
from langchain_openai import ChatOpenAI ## for chatting with OpenAI LLM
from langchain_core.output_parsers.string import StrOutputParser

import streamlit as st ## provides pre-built chatbot UI

load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
st.set_page_config(page_title="AI Chat Bot", page_icon=":sparkler:")

st.title("SimSamTra Bot")
## response from the LLM
def get_response(query, chat_history):
    template = """
    You are a very helpful assistant. Answer the following questions considering the history of this conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI()

    chain = prompt | llm | StrOutputParser()

    # return chain.invoke({
    return chain.astream({
        "chat_history": chat_history,
        "user_question": query
    })
    
## conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

## user input
user_query = st.chat_input("Your Query")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))
    
    st.session_state.chat_history.append(AIMessage(ai_response))