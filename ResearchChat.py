import streamlit as st
from tavily import TavilyClient
from langchain_community.llms import Ollama

tavily_client = TavilyClient(api_key="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")
llm = Ollama(model="qwen2:0.5b-instruct-q8_0", base_url="https://b924-35-230-57-99.ngrok-free.app/")

st.set_page_config(page_title="Stock Recommendation Assistant", layout="wide")

st.title("Talk to Stock Guru")

if "messages" not in st.session_state:
    st.session_state.messages = []

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
        response = tavily_client.search(user_input)
        formatted_results = ""
        for result in response['results']:
            # Limit content to the first 300 characters, ending at the nearest sentence
            content = result.get('content', 'N/A')
            prompt = f"Context: {content}\nQuestion: {user_input}\nPrompt: Give brief explanation of the context"
            response = llm.invoke(prompt)
            formatted_result = (
                f"**Title**: {result.get('title', 'N/A')}\n\n"
                f"**URL**: {result.get('url', 'N/A')}\n\n"
                f"**Content**: {response}\n\n"
                "------------------\n\n"
            )
            formatted_results += formatted_result
    
    except Exception as e:
        response = f"Error: {e}"

    st.session_state.messages.append({"type": "assistant", "content": formatted_results})
    st.chat_message("assistant").write(formatted_results)
