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

if st.sidebar.button("Notes"):
    st.session_state.page = "notes"


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

#⌬ ⚛︎⚕
if st.session_state.page == "Chem Assistant":
    st.subheader("⌬ Chem Assistant")
   

    user_input = st.text_input("Ask your chemistry doubt:")

    if user_input:
        reply = get_response(user_input)
        st.write("🤖", reply)


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
 
    

if st.session_state.page == "notes":
    st.subheader("⌬ Notes")     
     

    st.title("🧪 Polymers Quiz")

    score = 0

    # Q1
    q1 = st.radio("1. Which polymer is biodegradable?",
                ["PVC", "PHBV", "Polystyrene"])
    if q1 == "PHBV":
        score += 1

    # Q2
    q2 = st.radio("2. Engineering thermoplastics are known for:",
                ["Low strength", "High strength & durability", "Only flexibility"])
    if q2 == "High strength & durability":
        score += 1

    # Q3
    q3 = st.radio("3. Conducting polymers conduct electricity due to:",
                ["Heat", "Electron movement", "Water content"])
    if q3 == "Electron movement":
        score += 1

    # Q4
    q4 = st.radio("4. OLED works on which principle?",
                ["Heat emission", "Electroluminescence", "Magnetism"])
    if q4 == "Electroluminescence":
        score += 1

    # Q5
    q5 = st.radio("5. FRP stands for:",
                ["Flexible Resin Polymer", "Fiber Reinforced Plastic", "Fast Reactive Polymer"])
    if q5 == "Fiber Reinforced Plastic":
        score += 1

    # Q6
    q6 = st.radio("6. Which is used to increase flexibility of plastics?",
                ["Stabilizer", "Plasticizer", "Filler"])
    if q6 == "Plasticizer":
        score += 1

    # Q7
    q7 = st.radio("7. Which polymer is used in biodegradable applications?",
                ["PHBV", "Polyethylene", "PVC"])
    if q7 == "PHBV":
        score += 1

    # Q8
    q8 = st.radio("8. Carbon fiber composites are mainly used in:",
                ["Cooking utensils", "Aerospace", "Paper industry"])
    if q8 == "Aerospace":
        score += 1

    # RESULT
    if st.button("Submit Quiz 🚀"):
        st.success(f"Your Score: {score}/8")

        if score == 8:
            st.balloons()
            st.write("🔥 Perfect! You nailed it!")
        elif score >= 5:
            st.write("💪 Good job! Keep improving!")
        else:
            st.write("😅 Revise once more!")