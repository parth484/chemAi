# components.html("""
#     <div style="
#         background: rgba(255,255,255,0.05);
#         padding: 20px;
#         border-radius: 15px;
#         color: white;
#         box-shadow: 0 8px 20px rgba(0,0,0,0.3);
#     ">
#         <h3>✨ Contents</h3>

#         <p><b>📚 Learning Made Easy:</b><br>
#         This app explains polymer concepts in a simple and structured way.</p>

#         <p><b>🧪 Interactive Quizzes:</b><br>
#         Practice with quizzes that reinforce your knowledge.</p>

#         <p><b>🤖 AI Chatbot Support:</b><br>
#         Ask any doubt anytime and get instant explanations.</p>

#     </div>
#     """, height=300)





import streamlit as st
import json, re
from google import genai

# 🔑 Gemini Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 🎯 Function: Generate AI Questions
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
        model="gemini-2.0-flash",
        contents=prompt
    )

    def extract_json(text):
        match = re.search(r"\[.*\]", text, re.DOTALL)
        return match.group(0) if match else "[]"

    clean_text = extract_json(response.text)
    return json.loads(clean_text)


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

        st.subheader(f"Question {st.session_state.q_index + 1}")
        selected = st.radio(
            q["q"],
            ["-- Select an option --"] + q["options"],
            key=st.session_state.q_index
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