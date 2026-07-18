import streamlit as st
import requests
from chatbot_ui.core.config import config

def api_call(method, url, **kwargs):
    def _show_error_popup(message):
        """shwow error message as a popup in the top right corner."""
        st.session_state["error_popup"] = {
            "visible": True,
            "message": message,
        }
    
    try:
        response = getattr(requests, method)(url, **kwargs)

        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            response_data = {"message": "Invalid JSON response from the API."}

        if response.status_code != 200:
            return False, response_data
        
        return True, response_data
    
    except requests.exceptions.RequestException as e:
        _show_error_popup("Error occurred while making the API request.")
        return False, {"message": str(e)}
    
with st.sidebar:   
    st.title("LLM API Playground")
    provider = st.selectbox("Select LLM Provider", ["OpenAI", "Google"])
    model_name = st.text_input("Enter Model Name", value="gpt-5-nano" if provider == "OpenAI" else "gemini-2.5-flash")


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

        output = api_call("post", f"{config.API_URL}/chat", json={
            "provider": st.session_state.provider,
            "model_name": st.session_state.model_name,
            "messages": st.session_state.messages
        })
        response_data = output[1]
        answer = response_data["answer"]
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})