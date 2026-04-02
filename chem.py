import streamlit as st
import os
import datetime
from google import genai


if "page" not in st.session_state:
    st.session_state.page = "home"

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config("Chem-Ai",layout="wide")
st.title("Chem-Ai")



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
        'I only answer chemistry questions 😊'(but if (hi or bro or something other calling name(greeting)) is user input then answer it as chem tutor)

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

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("✨ Features of the App")
    st.write("""
    - 📚 Learn polymer concepts easily  
    - 🧪 Test knowledge with quizzes  
    - 🤖 Ask doubts using AI chatbot  
    """)
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.page == "notes":
    st.subheader("⌬ Notes")     
    st.warning("Under construction!!!")           