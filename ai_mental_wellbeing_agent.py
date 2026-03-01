import streamlit as st
from groq import Groq
import random
import os

# 🔐 Get API key from environment variable
# 🔐 Sidebar API Key Input
st.sidebar.header("🔐 Groq API Key")
user_api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")

# Use sidebar key if entered, otherwise use environment variable
groq_api_key = user_api_key if user_api_key else os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Mental Wellbeing Agent", layout="centered")

# 🌌 3D Animated Background + Glass Effect
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 20% 30%, #00ffc8 0%, transparent 25%),
                radial-gradient(circle at 80% 70%, #6a11cb 0%, transparent 25%),
                linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    background-attachment: fixed;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

.main-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(25px);
    padding: 35px;
    border-radius: 25px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.4);
    transform: perspective(1000px) rotateX(2deg);
    transition: 0.4s ease;
}

.main-card:hover {
    transform: perspective(1000px) rotateX(0deg) scale(1.02);
}

h1 {
    text-align: center;
    font-size: 42px;
    background: linear-gradient(90deg, #00ffc8, #00b3ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.quote {
    text-align: center;
    font-size: 22px;
    font-weight: 500;
    color: #ffde59;
    margin-bottom: 25px;
}

.response-box {
    background: rgba(0, 255, 200, 0.07);
    padding: 20px;
    border-radius: 15px;
    border-left: 4px solid #00ffc8;
    margin-top: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.stButton>button {
    background: linear-gradient(90deg, #00ffc8, #00b3ff);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #00ffc8;
}

textarea {
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 AI Mental Wellbeing Agent")

quotes = [
    "🌿 Healing is not linear. Be patient with yourself.",
    "✨ You are stronger than you feel right now.",
    "🌸 Growth takes time, trust the process.",
    "💙 Every emotion you feel is valid.",
    "🌅 One small step today is enough."
]

st.markdown(f'<div class="quote">{random.choice(quotes)}</div>', unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)

mood = st.slider("😊 Mood Level", 1, 10, 5)
sleep = st.slider("😴 Sleep Hours", 0, 12, 6)
stress = st.slider("😰 Stress Level", 1, 10, 5)
message = st.text_area("💭 Tell me what’s on your mind...")

def generate_response(prompt):
    if not groq_api_key:
        return "⚠ GROQ_API_KEY is not set in environment variables."

    try:
        client = Groq(api_key=groq_api_key)

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Respond warmly and include supportive emojis."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant"
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"

if st.button("🚀 Generate Support Insight"):

    prompt = f"""
    Mood: {mood}/10
    Sleep: {sleep} hours
    Stress: {stress}/10
    Description: {message}

    Provide supportive mental wellbeing advice in 3 sections:
    1. Emotional Assessment (add emojis)
    2. Practical Action Plan (add emojis)
    3. Positive Reinforcement (add emojis)
    """

    with st.spinner("🧠 Understanding your emotions..."):
        output = generate_response(prompt)

    st.markdown("### 🌿 Your Personalized Insight")
    st.markdown(f'<div class="response-box">{output}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)