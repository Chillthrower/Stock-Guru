import streamlit as st
from langchain_ollama import ChatOllama
from langchain_community.utilities import SearxSearchWrapper

llm = ChatOllama(model="llama3", temperature=0, base_url="https://73c7-34-90-49-132.ngrok-free.app")

st.title("Stock Analysis Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores chat history

# Display chat history
if st.session_state.messages:
    for message in st.session_state.messages:
        if message["type"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])

if user_input := st.chat_input("Ask about stocks, e.g., AAPL vs MSFT vs GOOGL"):
    st.session_state.messages.append({"type": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    try:
        s = SearxSearchWrapper(searx_host="http://localhost:32768")
        with st.spinner("Thinking..."):
            search_results = s.run(user_input, engines=["google"], categories='general')
        
        if search_results:
            query_summary = " ".join(search_results)
        else:
            query_summary = "I'm unable to fetch results for your query right now."
        
        response = llm.invoke(f"User asked: {user_input}\nSearch results: {query_summary}\nProvide a detailed and insightful response:")
    
    except Exception as e:
        response = f"Error: {e}"

    st.session_state.messages.append({"type": "assistant", "content": response.content})
    st.chat_message("assistant").write(response.content)

