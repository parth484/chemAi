import streamlit as st
import os
import datetime
from google import genai
import streamlit.components.v1 as components

if "page" not in st.session_state:
    st.session_state.page = "home"

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config("Chem-Ai",layout="wide")
st.title("ChemAssist-Ai")


#---------for creating pallet or cards----------------
st.markdown("""
<style>
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


st.markdown(
"""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
""",
unsafe_allow_html=True
)


st.sidebar.title("Navigation")

if st.sidebar.button("Home"):
    st.session_state.page = "home"

if st.sidebar.button("Chem Assistant"):
    st.session_state.page = "Chem Assistant"

if st.sidebar.button("Quiz"):
    st.session_state.page = "quiz"


st.sidebar.markdown("---")

st.sidebar.markdown(
 """
<div style="display:flex; justify-content:center; gap:20px; margin-top:20px;">
<a href="https://www.linkedin.com/in/parth-adsul-889106384/" target="_blank">
<i class="fab fa-linkedin" style="font-size:34px; color:#0A66C2;"></i>
</a>

<a href="https://github.com/parth484" target="_blank">
<i class="fab fa-github" style="font-size:34px; color:black;"></i>
</a>
</div>

<p style="text-align:center; font-size:12px; margin-top:8px;">
Made by Parth Adsul
</p>
""",
unsafe_allow_html=True
)    

def get_response(user_input):
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # stable model
        contents=f"""
        You are a chemistry tutor. Only answer chemistry-related questions.
        If the question is not related to chemistry, say:
        'I only answer chemistry questions 😊'(but if (hi or bro or something other calling name(greeting)) is user input; then answer it as chem tutor)

        Question: {user_input}
        """
    )
    return response.text

#⌬ ⚛︎⚕---------------------Assistant-----------------------------
# 🎨 CSS for chat UI
st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
}

.user-bubble {
    align-self: flex-end;
    background: #00ffd5;
    color: black;
    padding: 10px 15px;
    border-radius: 15px 15px 0px 15px;
    margin: 5px;
    max-width: 70%;
}

.bot-bubble {
    align-self: flex-start;
    background: #2c2c2c;
    color: #f1f1f1;
    padding: 10px 15px;
    border-radius: 15px 15px 15px 0px;
    margin: 5px;
    max-width: 70%;
}
</style>
""", unsafe_allow_html=True)


if st.session_state.page == "Chem Assistant":

    st.subheader("🤖 Chem Assistant")

    # Chat history
    if "chat" not in st.session_state:
        st.session_state.chat = []


    # Input box
    # 💬 FORM (this auto clears input)
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 Ask your chemistry doubt...")
        submitted = st.form_submit_button("Send 🚀")

    if submitted and user_input:
        reply = get_response(user_input)

        st.session_state.chat.append(("user", user_input))
        st.session_state.chat.append(("bot", reply))

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for role, msg in st.session_state.chat:
        if role == "user":
            st.markdown(f'<div class="user-bubble">👤 {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">🤖 {msg}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Clear chat button
    if st.button("🗑 Clear Chat"):
        st.session_state.chat = []
        st.rerun()

#-------------------------------Home------------------------------
if st.session_state.page == "home":
    st.title("🧬 PolyLearn AI")
    st.caption("🚀 Interactive Polymer Learning App with AI Chatbot")

    st.markdown("""
    ### 👨‍🎓 Developed by: Parth  
    ### 📘 Subject: Chemistry (Polymers)  
    ### 🏫 DYPCOE  
    """)

    st.markdown("""
    <div class="card">
        <h3>✨ Features of the App</h3>
        <ul>
            <li>📚 Learn polymer concepts easily</li>
            <li>🧪 Test knowledge with quizzes</li>
            <li>🤖 Ask doubts using AI chatbot</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
 
 #------------------Quiz------------------------   

if st.session_state.page == "quiz":
    st.subheader("⌬ Quiz")     
    st.title("Polymers in Engineering")  
    st.title("🧪 Polymers Quiz")

    # Questions
    questions = [
        {
            "q": "Which polymer is biodegradable?",
            "options": ["PVC", "PHBV", "Polystyrene"],
            "ans": "PHBV"
        },
        {
            "q": "Engineering thermoplastics are known for:",
            "options": ["Low strength", "High strength & durability", "Only flexibility"],
            "ans": "High strength & durability"
        },
        {
            "q": "Conducting polymers conduct electricity due to:",
            "options": ["Heat", "Electron movement", "Water content"],
            "ans": "Electron movement"
        },
        {
            "q": "OLED works on which principle?",
            "options": ["Heat emission", "Electroluminescence", "Magnetism"],
            "ans": "Electroluminescence"
        },
        {
            "q": "FRP stands for:",
            "options": ["Flexible Resin Polymer", "Fiber Reinforced Plastic", "Fast Reactive Polymer"],
            "ans": "Fiber Reinforced Plastic"
        }
    ]

    # Session state
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
        st.session_state.score = 0

    # Current question
    q = questions[st.session_state.q_index]

    st.subheader(f"Question {st.session_state.q_index + 1}")

    selected = st.radio(
        q["q"],
        ["-- Select an option --"] + q["options"],
        key=st.session_state.q_index
    )

    # Next button
    if st.button("Next ➡️"):
        if selected == "-- Select an option --":
            st.warning("⚠️ Please select an option!")
        else:
            if selected == q["ans"]:
                st.session_state.score += 1

            st.session_state.q_index += 1

            # If quiz finished
            if st.session_state.q_index >= len(questions):
                st.success(f"🎉 Quiz Completed! Score: {st.session_state.score}/{len(questions)}")
                st.balloons()

                # Reset button
                if st.button("Restart Quiz 🔄"):
                    st.session_state.q_index = 0
                    st.session_state.score = 0
            else:
                st.rerun()