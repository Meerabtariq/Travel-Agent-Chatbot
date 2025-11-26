
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- Load Gemini API key ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

# --- Page Config ---
st.set_page_config(page_title="Travel Agent Chatbot 🌍", page_icon="🤖", layout="wide")

# --- Session State ---
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

# --- CSS Styles ---
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.left-col {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 60px;
}
.heading {
    font-size: 60px;
    font-weight: 800;
    color: #2C3E50;
}
.subtext {
    font-size: 20px;
    color: #555;
    margin-top: 10px;
    margin-bottom: 30px;
}
.chat-btn {
    background-color: #281f6e;
    color: white;
    padding: 14px 30px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 50px;
    cursor: pointer;
    text-align: center;
}
.chat-btn:hover {
    background-color: #281f6e;
}
/* Ensure image container won't force full width */
.robot-img {
    display: block;
    margin: auto;
    max-width: 350px; /* smaller robot */
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# --- MAIN UI: Before Chat Starts ---
if not st.session_state.chat_open:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="left-col">', unsafe_allow_html=True)
        st.markdown('<div class="heading">Travel Agent Template Library</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtext">Your friendly travel assistant — plan trips, find hotels & explore destinations 🌍</div>', unsafe_allow_html=True)
        if st.button("💬 Let's Chat", key="open_chat"):
            st.session_state.chat_open = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        # Use use_container_width parameter or specify width to avoid deprecation warning.
        # Here we set use_container_width=False and a fixed width to keep robot small.
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712100.png",
                 use_container_width=False, width=350)

# --- CHAT INTERFACE ---
else:
    # Darker blue tone background (clearly visible)
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #7fa6ff, #5f8dff);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🤖 Travel Chatbot")
    st.markdown("Ask me about any city, country, or tourist place in the world! 🌏")

    # user input
    user_input = st.text_input("✈️ Type your travel question:", key="user_q")

    if user_input:
        try:
            response = model.generate_content(user_input)
            # show result in black text (readable on the blue background)
            st.markdown(f"<div style='color:#000; font-size:18px; padding:12px 0;'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Sorry, I faced an error: {e}")

    if st.button("⬅️ Back"):
        st.session_state.chat_open = False
        st.rerun()
