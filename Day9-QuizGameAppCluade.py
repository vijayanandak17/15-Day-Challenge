import streamlit as st
import base64
from io import BytesIO
import requests
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Tamil Film Quiz",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .question-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        color: white;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .option-button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border: none;
        padding: 15px 25px;
        margin: 10px 0;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .option-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .correct-answer {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%) !important;
    }
    
    .wrong-answer {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%) !important;
    }
    
    .score-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .progress-bar {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        height: 20px;
        border-radius: 10px;
        margin: 20px 0;
        overflow: hidden;
    }
    
    .movie-image {
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Quiz questions with Tamil movies/actors
QUIZ_QUESTIONS = [
    {
        "question": "Which legendary Tamil actor is known as 'Thalaivar' (Leader)?",
        "image_url": "rajni.jpg",
        "options": ["Kamal Haasan", "Rajinikanth", "Vijay", "Ajith Kumar"],
        "correct": 1,
        "explanation": "Rajinikanth is widely known as 'Thalaivar' and is one of the most iconic actors in Tamil cinema."
    },
    {
        "question": "Which Tamil movie won the National Film Award for Best Feature Film in 2019?",
        "image_url": "https://images.unsplash.com/photo-1489599537954-1e9c28bd04dd?w=300&h=200&fit=crop",
        "options": ["96", "Pariyerum Perumal", "Vada Chennai", "Asuran"],
        "correct": 3,
        "explanation": "Asuran, starring Dhanush, won the National Film Award for Best Feature Film in Tamil in 2019."
    },
    {
        "question": "Who directed the critically acclaimed Tamil film 'Kaaka Muttai'?",
        "image_url": "https://images.unsplash.com/photo-1574267432553-4b4628081c31?w=300&h=200&fit=crop",
        "options": ["Pa. Ranjith", "M. Manikandan", "Vetrimaaran", "Karthik Subbaraj"],
        "correct": 1,
        "explanation": "M. Manikandan directed 'Kaaka Muttai', which received widespread critical acclaim and international recognition."
    },
    {
        "question": "Which composer is known as the 'Mozart of Madras'?",
        "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300&h=200&fit=crop",
        "options": ["Ilaiyaraaja", "A.R. Rahman", "Harris Jayaraj", "Yuvan Shankar Raja"],
        "correct": 1,
        "explanation": "A.R. Rahman is famously known as the 'Mozart of Madras' for his innovative music compositions."
    }
]

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'answers' not in st.session_state:
        st.session_state.answers = []

def reset_quiz():
    """Reset the quiz to initial state"""
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_completed = False
    st.session_state.answers = []

def get_score_message(score, total):
    """Get appropriate message based on score"""
    percentage = (score / total) * 100
    if percentage >= 75:
        return "🏆 Tamil Cinema Expert! Outstanding knowledge!"
    elif percentage >= 50:
        return "👏 Good job! You know Tamil films well!"
    else:
        return "📚 Keep watching more Tamil movies and try again!"

def display_question(question_data, question_num):
    """Display a single question with options"""
    st.markdown(f"""
    <div class="question-container">
        <h2>Question {question_num + 1} of {len(QUIZ_QUESTIONS)}</h2>
        <h3>{question_data['question']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display movie-related image
    try:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(question_data['image_url'], caption="Tamil Cinema", use_container_width=True, output_format="JPEG")
    except:
        st.info("🎬 Imagine a scene from Tamil cinema here!")
    
    # Progress bar
    progress = (question_num + 1) / len(QUIZ_QUESTIONS)
    st.markdown(f"""
    <div class="progress-bar">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    width: {progress * 100}%; 
                    height: 100%; 
                    border-radius: 10px;
                    transition: width 0.3s ease;">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display options as buttons
    st.write("### Choose your answer:")
    
    cols = st.columns(2)
    for i, option in enumerate(question_data['options']):
        col = cols[i % 2]
        with col:
            if st.button(f"{chr(65 + i)}. {option}", key=f"option_{i}", use_container_width=True):
                # Store the answer
                st.session_state.answers.append(i)
                
                # Check if correct
                if i == question_data['correct']:
                    st.session_state.score += 1
                    st.success(f"✅ Correct! {question_data['explanation']}")
                else:
                    correct_answer = question_data['options'][question_data['correct']]
                    st.error(f"❌ Wrong! The correct answer is: {correct_answer}")
                    st.info(question_data['explanation'])
                
                # Move to next question or complete quiz
                if st.session_state.current_question < len(QUIZ_QUESTIONS) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.session_state.quiz_completed = True
                    st.rerun()

def display_results():
    """Display final quiz results"""
    score = st.session_state.score
    total = len(QUIZ_QUESTIONS)
    percentage = (score / total) * 100
    
    st.markdown(f"""
    <div class="score-container">
        <h1>🎬 Quiz Completed!</h1>
        <h2>Your Score: {score}/{total} ({percentage:.0f}%)</h2>
        <h3>{get_score_message(score, total)}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Show detailed results
    st.markdown("### 📊 Detailed Results")
    for i, question in enumerate(QUIZ_QUESTIONS):
        user_answer = st.session_state.answers[i]
        correct_answer = question['correct']
        
        with st.expander(f"Question {i+1}: {question['question']}"):
            col1, col2 = st.columns(2)
            with col1:
                if user_answer == correct_answer:
                    st.success(f"✅ Your answer: {question['options'][user_answer]}")
                else:
                    st.error(f"❌ Your answer: {question['options'][user_answer]}")
            with col2:
                st.info(f"✅ Correct answer: {question['options'][correct_answer]}")
            st.write(f"💡 **Explanation:** {question['explanation']}")
    
    # Restart button
    if st.button("🔄 Restart Quiz", use_container_width=True):
        reset_quiz()
        st.rerun()

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 Tamil Film Quiz Challenge</h1>
        <p>Test your knowledge of Tamil cinema! 🌟</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.quiz_completed:
        # Display current question
        current_q = st.session_state.current_question
        display_question(QUIZ_QUESTIONS[current_q], current_q)
        
        # Show current score
        st.markdown(f"""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; 
                    background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); 
                    border-radius: 10px;">
            <h4>Current Score: {st.session_state.score}/{st.session_state.current_question + 1} attempted</h4>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Display results
        display_results()

if __name__ == "__main__":
    main()