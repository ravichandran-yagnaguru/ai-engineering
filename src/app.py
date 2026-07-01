import streamlit as st
from openai import OpenAI
from groq import Groq
from google import genai
from core.config import config

def run_llm(provider, model_name, messages, max_tokens=100):
    if provider == "OpenAI":
        client = OpenAI(api_key=config.OPENAI_API_KEY) 
    elif provider == "Groq":
        client = Groq(api_key=config.GROQ_API_KEY)
    elif provider == "Google":
        client = genai.Client(api_key=config.GOOGLE_API_KEY)

    if provider == "Google":
        return client.models.generate_content(
            model=model_name,
            contents=[message["content"] for message in messages],
        ).text
    elif provider =="Groq":
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens
        ).choices[0].message.content
    else:
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_tokens,
            reasoning_effort="minimal"
        ).choices[0].message.content
    
with st.sidebar:   
    st.title("LLM API Playground")
    provider = st.selectbox("Select LLM Provider", ["OpenAI", "Google"])
    model_name = st.text_input("Enter Model Name", value="gpt-5-nano" if provider == "OpenAI" else "gemini-2.5-flash")
    user_input = st.text_area("Enter your prompt here:")

    st.session_state.provider = provider
    st.session_state.model_name = model_name

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:= st.chat_input("Hello! How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output = run_llm(st.session_state.provider, st.session_state.model_name, st.session_state.messages)
        response_data = output
        answer = response_data
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})