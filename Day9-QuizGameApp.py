import streamlit as st

# --- App Config ---
st.set_page_config(page_title="🎬 Tamil Cinema Quiz", layout="centered")

# --- CSS Styling for Colorful Look ---
st.markdown("""
    <style>
        .question-card {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .question-text {
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #222;
        }
    </style>
""", unsafe_allow_html=True)

# --- Tamil Film Quiz Questions (Only 4) ----
questions = [
    {
        "question": "Who is known as 'Ulaganayagan' in Tamil cinema?",
        "options": ["Rajinikanth", "Kamal Haasan", "Vijay", "Ajith"],
        "answer": "Kamal Haasan",
        "image": "kamal.jpg"
    },
    {
        "question": "Which Tamil movie was India's first submission to the Oscars?",
        "options": ["Nayakan", "Devar Magan", "Jeans", "Lagaan"],
        "answer": "Nayakan",
        "image": "https://m.media-amazon.com/images/M/MV5BMjA1NzYxOTk1N15BMl5BanBnXkFtZTcwNjYxNTQyMQ@@._V1_.jpg"
    },
    {
        "question": "Who composed the music for the movie 'Roja'?",
        "options": ["Ilaiyaraaja", "A.R. Rahman", "Deva", "Yuvan Shankar Raja"],
        "answer": "A.R. Rahman",
        "image": "https://upload.wikimedia.org/wikipedia/en/0/09/Roja_poster.jpg"
    },
    {
        "question": "Which Tamil movie introduced the character 'Chitti the Robot'?",
        "options": ["Sivaji", "Indian", "Enthiran", "2.0"],
        "answer": "Enthiran",
        "image": "https://upload.wikimedia.org/wikipedia/en/1/1e/Enthiran_poster.jpg"
    }
]

# --- Session State Initialization ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "completed" not in st.session_state:
    st.session_state.completed = False

# --- Quiz Logic ---
if not st.session_state.completed:
    q = questions[st.session_state.q_index]

    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.image(q["image"],  use_container_width =True, caption="🎥 Tamil Cinema Trivia")
    st.markdown(f"<div class='question-text'>Q{st.session_state.q_index+1}. {q['question']}</div>", unsafe_allow_html=True)

    answer = st.radio("Choose your answer:", q["options"], index=None, key=f"q_{st.session_state.q_index}")

    if st.button("Submit Answer"):
        if answer:
            if answer == q["answer"]:
                st.session_state.score += 1
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong! Correct Answer: {q['answer']}")

            st.session_state.q_index += 1
            if st.session_state.q_index >= len(questions):
                st.session_state.completed = True
        else:
            st.warning("⚠️ Please select an option before submitting.")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.subheader("🎉 Quiz Completed!")
    st.write(f"Your Final Score: **{st.session_state.score} / {len(questions)}**")
    if st.session_state.score == len(questions):
        st.balloons()
        st.success("👏 Excellent! You are a Tamil cinema expert.")
    elif st.session_state.score >= 2:
        st.info("👍 Good job! You know Tamil cinema quite well.")
    else:
        st.warning("📖 Better luck next time! Keep watching Tamil films 🎬")

    if st.button("Restart Quiz"):
        st.session_state.score = 0
        st.session_state.q_index = 0
        st.session_state.completed = False
