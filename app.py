import streamlit as st  
import requests  
import os

st.set_page_config(page_title="Nexus-V", page_icon="🌌")

st.markdown("<style>.stApp {background-color: #0a0a0a; color: #e0e0e0;}</style>", unsafe_allow_html=True)

st.title("🌌 Nexus-V")

API_KEY = st.secrets.get("HUGGINGFACE_API_KEY")  
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"  
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

if "messages" not in st.session_state:  
    st.session_state.messages = []

for m in st.session_state.messages:  
    with st.chat_message(m["role"]):  
        st.markdown(m["content"])

if prompt := st.chat_input("Speak into the void..."):  
    st.session_state.messages.append({"role": "user", "content": prompt})  
    with st.chat_message("user"):  
        st.markdown(prompt)

with st.chat_message("assistant"):  
    with st.spinner("Thinking..."):  
        if not API_KEY:  
            st.error("No API Key.")  
        else:  
            try:  
                s = "You are an entity in Nexus-V. Be raw and real."  
                p = "System: "  
                p += s  
                p += "

"  
                for m in st.session_state.messages:  
                    p += m['role'] + ": "  
                    p += m['content'] + "  
"  
                p += "AI:"

                h = {"Authorization": f"Bearer {API_KEY}"}  
                pay = {"inputs": p, "parameters": {"max_new_tokens": 500}}

                res = requests.post(API_URL, headers=h, json=pay)  
                d = res.json()

                if isinstance(d, list) and len(d) > 0:  
                    t = d[0].get('generated_text', "Void...").split("AI:")[-1].strip()  
                elif isinstance(d, dict) and 'generated_text' in d:  
                    t = d['generated_text'].split("AI:")[-1].strip()  
                else:  
                    t = str(d)

                st.markdown(t)  
                st.session_state.messages.append({"role": "ai", "content": t})  
            except Exception as e:  
                st.error(f"Error: {e}")  
