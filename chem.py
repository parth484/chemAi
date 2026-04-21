import streamlit as st
import os
import datetime
from google import genai
import json, re
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
    #displaying chats________
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
 
# 🎯 Function: Generate AI Questions--------------------------------------------------------------------------

def generate_ai_questions(topic="Polymers in Engineering", num_q=10):
    prompt = f"""
    Generate {num_q} multiple choice questions on {topic}.

    Format strictly in JSON:
    [
      {{
        "q": "question",
        "options": ["opt1", "opt2", "opt3", "opt4"],
        "ans": "correct option",
        "exp": "short explanation"
      }}
    ]

    Rules:
    - 4 options compulsory
    - Explanation must be 1-2 lines
    - Only return JSON
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    def extract_json(text):
        match = re.search(r"\[.*\]", text, re.DOTALL)
        return match.group(0) if match else "[]"

    clean_text = extract_json(response.text)

    try:
        return json.loads(clean_text)
    except:
        return []

# ================== QUIZ PAGE ==================
if st.session_state.get("page") == "quiz":

    st.title("🧪 AI Powered Quiz")

    # 🧠 Generate Questions with Loading
    if "questions" not in st.session_state:
        with st.spinner("🧠 Generating Quiz... Please wait ⏳"):
            st.session_state.questions = generate_ai_questions()

    # 🧾 Initialize states
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.user_answers = []

    questions = st.session_state.questions

    # ⚠️ Handle empty/failed AI response
    if not questions:
        st.error("⚠️ Failed to generate quiz. Please try again.")

        if st.button("Retry 🔄"):
            st.session_state.questions = generate_ai_questions()
            st.rerun()

        st.stop()

    # 🏁 If quiz finished
    if st.session_state.q_index >= len(questions):

        st.success(f"🎉 Quiz Completed! Score: {st.session_state.score}/{len(questions)}")
        st.balloons()

        st.markdown("## 📘 Explanations")

        for i, q in enumerate(questions):
            user_ans = st.session_state.user_answers[i]

            if user_ans == q["ans"]:
                st.markdown(f"✅ **Q{i+1}: {q['q']}**")
            else:
                st.markdown(f"❌ **Q{i+1}: {q['q']}**")

            st.markdown(f"- Your Answer: {user_ans}")
            st.markdown(f"- Correct Answer: {q['ans']}")
            st.markdown(f"- 💡 Explanation: {q['exp']}")
            st.markdown("---")

        # 🔄 Restart
        if st.button("Restart Quiz 🔄"):
            with st.spinner("🧠 Generating New Quiz..."):
                st.session_state.questions = generate_ai_questions()
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.rerun()

    else:
        # 📊 Progress bar
        st.progress(st.session_state.q_index / len(questions))

        # 📍 Current Question
        q = questions[st.session_state.q_index]

        st.subheader(f"Question {st.session_state.q_index + 1} / {len(questions)}")
        selected = st.radio(
            q["q"],
            ["-- Select an option --"] + q["options"],
            key=f"q_{st.session_state.q_index}"
        )

        # ➡️ Next Button
        if st.button("Next ➡️"):
            if selected == "-- Select an option --":
                st.warning("⚠️ Please select an option!")
            else:
                st.session_state.user_answers.append(selected)

                if selected == q["ans"]:
                    st.session_state.score += 1

                st.session_state.q_index += 1
                st.rerun()