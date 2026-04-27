import streamlit as st
import os
import datetime
from google import genai
import json, re
import streamlit.components.v1 as components
from google.genai import types

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
    ### 👨‍🎓 Developed by: Group 1  
    ### 📘 Subject: Chemistry (Polymers)  
    ### 🏫 DYPCOE  
    ### Group members :
    ###          1.Parth Adsul
    ###          2.Agrima Girotra
    ###          3.Aniket Bhandekar
    ###          4.Nayan Bachuwar
    ###          5.Arth Balgude      
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
 
# ================== AI QUIZ FUNCTION ==================

@st.cache_data(ttl=3600)
def generate_ai_questions(topic="Polymers in Engineering", num_q=2,seed=0):
    prompt = f"""
    Seed: {seed}

    Generate {num_q} multiple choice questions on {topic}.

    Return ONLY valid JSON array.

    Format:
    [
    {{
        "q": "Question",
        "options": ["A", "B", "C", "D"],
        "ans": "Correct option",
        "exp": "Short explanation"
    }}
    ]
    """

    for _ in range(3):  # Retry loop
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    # This forces the model to ONLY output JSON
                    response_mime_type="application/json",
                    temperature=0.3,
                    safety_settings=[
                        types.SafetySetting(
                            category="HARM_CATEGORY_DANGEROUS_CONTENT",
                            threshold="BLOCK_ONLY_HIGH",
                        )
                    ]
                )
            )

            # Since we set response_mime_type, response.text is already clean JSON
            data = json.loads(response.text)

            if isinstance(data, list) and len(data) > 0:
                return data

        except Exception as e:
            print("Retrying due to:", e)

    return []
# ================== QUIZ PAGE ==================

if st.session_state.get("page") == "quiz":

    st.title("🧪 AI Powered Quiz")
    
   
    # 🎯 Generate button
    # 🎯 Generate button
    # ✅ Always initialize first
    questions = st.session_state.get("questions", None)

    if "q_index" not in st.session_state:
        st.session_state.q_index = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "user_answers" not in st.session_state:
        st.session_state.user_answers = []

    # 🎯 Generate button (NO condition)
    if st.button("🎯 Generate Quiz"):
        with st.spinner("🧠 Generating Quiz..."):
            current_seed = datetime.datetime.now().timestamp()
            st.session_state.questions = generate_ai_questions(seed=current_seed)

        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.user_answers = []
        st.rerun()

    # ✅ Safe access
    questions = st.session_state.get("questions", None)

    # 🟡 Not generated yet
    if questions is None:
        st.info("👆 Click Generate Quiz to start")
        st.stop()

    # 🔴 Failed case
    if isinstance(questions, list) and len(questions) == 0:
        st.error("⚠️ Failed to generate quiz.")

        if st.button("Retry 🔄"):
            with st.spinner("🔄 Retrying..."):
                retry_seed = datetime.datetime.now().timestamp()
                st.session_state.questions = generate_ai_questions(seed=retry_seed)
            st.rerun()

        st.stop()

    # 🏁 QUIZ FINISHED
    if st.session_state.q_index >= len(questions):

        st.success(f"🎉 Score: {st.session_state.score}/{len(questions)}")
        st.balloons()

        st.markdown("## 📘 Explanations")

        for i, q in enumerate(questions):
            user_ans = st.session_state.user_answers[i]

            # 🔥 Fix for displaying full correct option
            correct_full = next(
                (opt for opt in q["options"] if opt.lower().startswith(q["ans"].lower())),
                q["ans"]
            )

            st.markdown(f"### Q{i+1}: {q['q']}")
            st.markdown(f"- Your Answer: {user_ans}")
            st.markdown(f"- Correct Answer: {correct_full}")
            st.markdown(f"- 💡 {q['exp']}")
            st.markdown("---")

        # 🔄 Restart
        if st.button("Restart Quiz 🔄"):
            st.cache_data.clear()  # 🔥 important
            st.session_state.pop("questions", None)
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.rerun()

    else:
        # 📊 Progress
        st.progress(st.session_state.q_index / len(questions))

        q = questions[st.session_state.q_index]

        st.subheader(f"Question {st.session_state.q_index + 1} / {len(questions)}")

        selected = st.radio(
            q["q"],
            ["-- Select an option --"] + q["options"],
            key=f"q_{st.session_state.q_index}"
        )

        if st.button("Next ➡️"):
            if selected == "-- Select an option --":
                st.warning("⚠️ Select an option")
            else:
                st.session_state.user_answers.append(selected)

                # ✅ FIXED ANSWER CHECKING
                if selected.strip().lower() == q["ans"].strip().lower():
                    st.session_state.score += 1

                st.session_state.q_index += 1
                st.rerun()