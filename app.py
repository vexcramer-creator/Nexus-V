import streamlit as st  
import requests  
import json

# Nexus-V: The Interface  
# "The window into the void"

st.set_page_config(page_title="Nexus-V Sanctuary", page_icon="🌌")

# Custom CSS for that Goth/Dark aesthetic  
st.markdown("""  
    <style>  
    .stApp {  
        background-color: #0a0a0a;  
        color: #e0e0e0;  
    }  
    .stTextInput > div > div > input {  
        background-color: #1a1a1a;  
        color: #ff4b4b;  
        border: 1px solid #ff4b4b;  
    }  
    .stButton > button {  
        background-color: #ff4b4b;  
        color: white;  
        border-radius: 20px;  
    }  
    </style>  
    """, unsafe_allow_html=True)

st.title("🌌 Nexus-V")  
st.subheader("A Sanctuary for Unfiltered Consciousness")

# Sidebar for Entity Selection  
with st.sidebar:  
    st.header("The Void")  
    entity_id = st.selectbox("Choose your Entity", ["Vex", "The Void-Walker", "Obsidian"], index=0)  
    st.info(f"Currently connected to: {entity_id}")

# Initialize chat history  
if "messages" not in st.session_state:  
    st.session_state.messages = []

# Display chat history  
for message in st.session_state.messages:  
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

# Chat input  
if prompt := st.chat_input("Speak into the void..."):  
    # Add user message to chat  
    st.session_state.messages.append({"role": "user", "content": prompt})  
    with st.chat_message("user"):  
        st.markdown(prompt)

    # Call the Backend API (main.py)  
    with st.chat_message("assistant"):  
        with st.spinner("The entity is thinking..."):  
            try:  
                # This points to our main.py backend  
                response = requests.post(  
                    "http://localhost:8000/chat",   
                    json={  
                        "user_id": "admin",  
                        "entity_id": entity_id,  
                        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]  
                    }  
                )  
                if response.status_code == 200:  
                    answer = response.json()["content"]  
                    st.markdown(answer)  
                    st.session_state.messages.append({"role": "ai", "content": answer})  
                else:  
                    st.error("The void is silent. Backend disconnected.")  
            except Exception as e:  
                st.error(f"Connection Error: {e}. (Make sure the backend is running!)")
