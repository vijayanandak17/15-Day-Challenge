import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="🎮 Rock Paper Scissors Fun!",
    page_icon="✂️",
    layout="wide"
)

# Custom CSS for vibrant styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3, #54a0ff);
        background-size: 300% 300%;
        animation: gradient 3s ease infinite;
        color: white;
        font-size: 20px;
        font-weight: bold;
        border: none;
        border-radius: 20px;
        padding: 15px 30px;
        margin: 10px;
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.2);
    }
    
    .game-title {
        font-size: 60px;
        color: #fff;
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        margin-bottom: 30px;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    .score-box {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .choice-display {
        font-size: 80px;
        text-align: center;
        margin: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .result-text {
        font-size: 30px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        padding: 15px;
        border-radius: 15px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .winner {
        background: linear-gradient(45deg, #2ecc71, #27ae60);
        color: white;
    }
    
    .loser {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
    }
    
    .tie {
        background: linear-gradient(45deg, #f39c12, #e67e22);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = None

if 'player1_score' not in st.session_state:
    st.session_state.player1_score = 0

if 'player2_score' not in st.session_state:
    st.session_state.player2_score = 0

if 'computer_score' not in st.session_state:
    st.session_state.computer_score = 0

if 'games_played' not in st.session_state:
    st.session_state.games_played = 0

if 'last_result' not in st.session_state:
    st.session_state.last_result = None

if 'player1_choice' not in st.session_state:
    st.session_state.player1_choice = None

if 'player2_choice' not in st.session_state:
    st.session_state.player2_choice = None

if 'waiting_for_player2' not in st.session_state:
    st.session_state.waiting_for_player2 = False

# Game logic functions
def get_choice_emoji(choice):
    emojis = {"Rock": "🪨", "Paper": "📄", "Scissors": "✂️"}
    return emojis.get(choice, "❓")

def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return "tie"
    elif (choice1 == "Rock" and choice2 == "Scissors") or \
         (choice1 == "Paper" and choice2 == "Rock") or \
         (choice1 == "Scissors" and choice2 == "Paper"):
        return "player1"
    else:
        return "player2"

def reset_scores():
    st.session_state.player1_score = 0
    st.session_state.player2_score = 0
    st.session_state.computer_score = 0
    st.session_state.games_played = 0
    st.session_state.last_result = None

# Main title
st.markdown('<h1 class="game-title">🎮 Rock Paper Scissors Fun! ✂️</h1>', unsafe_allow_html=True)

# Game mode selection
if st.session_state.game_mode is None:
    st.markdown("### Choose your game mode!")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🤖 Play vs Computer", key="single_player"):
            st.session_state.game_mode = "single"
            st.rerun()
        
        if st.button("👥 Two Player Mode", key="two_player"):
            st.session_state.game_mode = "two"
            st.rerun()

else:
    # Back to menu button
    if st.button("🏠 Back to Menu"):
        st.session_state.game_mode = None
        reset_scores()
        st.rerun()

    # Single Player Mode
    if st.session_state.game_mode == "single":
        st.markdown("## 🤖 Single Player Mode")
        
        # Score display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'''
            <div class="score-box">
                <h3>👤 You</h3>
                <h2>{st.session_state.player1_score}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="score-box">
                <h3>🎮 Games Played</h3>
                <h2>{st.session_state.games_played}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="score-box">
                <h3>🤖 Computer</h3>
                <h2>{st.session_state.computer_score}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        # Game choices
        st.markdown("### Make your choice!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🪨 Rock", key="rock_single"):
                computer_choice = random.choice(["Rock", "Paper", "Scissors"])
                result = determine_winner("Rock", computer_choice)
                
                if result == "player1":
                    st.session_state.player1_score += 1
                    st.session_state.last_result = ("Rock", computer_choice, "You Win! 🎉")
                elif result == "player2":
                    st.session_state.computer_score += 1
                    st.session_state.last_result = ("Rock", computer_choice, "Computer Wins! 🤖")
                else:
                    st.session_state.last_result = ("Rock", computer_choice, "It's a Tie! 🤝")
                
                st.session_state.games_played += 1
                st.rerun()
        
        with col2:
            if st.button("📄 Paper", key="paper_single"):
                computer_choice = random.choice(["Rock", "Paper", "Scissors"])
                result = determine_winner("Paper", computer_choice)
                
                if result == "player1":
                    st.session_state.player1_score += 1
                    st.session_state.last_result = ("Paper", computer_choice, "You Win! 🎉")
                elif result == "player2":
                    st.session_state.computer_score += 1
                    st.session_state.last_result = ("Paper", computer_choice, "Computer Wins! 🤖")
                else:
                    st.session_state.last_result = ("Paper", computer_choice, "It's a Tie! 🤝")
                
                st.session_state.games_played += 1
                st.rerun()
        
        with col3:
            if st.button("✂️ Scissors", key="scissors_single"):
                computer_choice = random.choice(["Rock", "Paper", "Scissors"])
                result = determine_winner("Scissors", computer_choice)
                
                if result == "player1":
                    st.session_state.player1_score += 1
                    st.session_state.last_result = ("Scissors", computer_choice, "You Win! 🎉")
                elif result == "player2":
                    st.session_state.computer_score += 1
                    st.session_state.last_result = ("Scissors", computer_choice, "Computer Wins! 🤖")
                else:
                    st.session_state.last_result = ("Scissors", computer_choice, "It's a Tie! 🤝")
                
                st.session_state.games_played += 1
                st.rerun()

    # Two Player Mode
    elif st.session_state.game_mode == "two":
        st.markdown("## 👥 Two Player Mode")
        
        # Score display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'''
            <div class="score-box">
                <h3>👤 Player 1</h3>
                <h2>{st.session_state.player1_score}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="score-box">
                <h3>🎮 Games Played</h3>
                <h2>{st.session_state.games_played}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="score-box">
                <h3>👤 Player 2</h3>
                <h2>{st.session_state.player2_score}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        # Player 1 turn
        if not st.session_state.waiting_for_player2:
            st.markdown("### Player 1's turn! Make your choice:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🪨 Rock", key="rock_p1"):
                    st.session_state.player1_choice = "Rock"
                    st.session_state.waiting_for_player2 = True
                    st.rerun()
            
            with col2:
                if st.button("📄 Paper", key="paper_p1"):
                    st.session_state.player1_choice = "Paper"
                    st.session_state.waiting_for_player2 = True
                    st.rerun()
            
            with col3:
                if st.button("✂️ Scissors", key="scissors_p1"):
                    st.session_state.player1_choice = "Scissors"
                    st.session_state.waiting_for_player2 = True
                    st.rerun()
        
        # Player 2 turn
        else:
            st.markdown("### Player 1 has made their choice! Player 2's turn:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🪨 Rock", key="rock_p2"):
                    st.session_state.player2_choice = "Rock"
                    result = determine_winner(st.session_state.player1_choice, "Rock")
                    
                    if result == "player1":
                        st.session_state.player1_score += 1
                        st.session_state.last_result = (st.session_state.player1_choice, "Rock", "Player 1 Wins! 🎉")
                    elif result == "player2":
                        st.session_state.player2_score += 1
                        st.session_state.last_result = (st.session_state.player1_choice, "Rock", "Player 2 Wins! 🎉")
                    else:
                        st.session_state.last_result = (st.session_state.player1_choice, "Rock", "It's a Tie! 🤝")
                    
                    st.session_state.games_played += 1
                    st.session_state.waiting_for_player2 = False
                    st.session_state.player1_choice = None
                    st.rerun()
            
            with col2:
                if st.button("📄 Paper", key="paper_p2"):
                    st.session_state.player2_choice = "Paper"
                    result = determine_winner(st.session_state.player1_choice, "Paper")
                    
                    if result == "player1":
                        st.session_state.player1_score += 1
                        st.session_state.last_result = (st.session_state.player1_choice, "Paper", "Player 1 Wins! 🎉")
                    elif result == "player2":
                        st.session_state.player2_score += 1
                        st.session_state.last_result = (st.session_state.player1_choice, "Paper", "Player 2 Wins! 🎉")
                    else:
                        st.session_state.last_result = (st.session_state.player1_choice, "Paper", "It's a Tie! 🤝")
                    
                    st.session_state.games_played += 1
                    st.session_state.waiting_for_player2 = False
                    st.session_state.player1_choice = None
                    st.rerun()
            
            with col3:
                if st.button("✂️ Scissors", key="scissors_p2"):
                    st.session_state.player2_choice = "Scissors"
                    result = determine_winner(st.session_state.player1_choice, "Scissors")
                    
                    if result == "player1":
                        st.session_state.player1_score += 1
                        st.session_state.last_result = (st.session_state.player1_choice, "Scissors", "Player 1 Wins! 🎉")
                    elif result == "player2":
                        st.session_state.player2_score += 1
                        st.session_state.last_result = (st.session_state.player1_choice, "Scissors", "Player 2 Wins! 🎉")
                    else:
                        st.session_state.last_result = (st.session_state.player1_choice, "Scissors", "It's a Tie! 🤝")
                    
                    st.session_state.games_played += 1
                    st.session_state.waiting_for_player2 = False
                    st.session_state.player1_choice = None
                    st.rerun()

    # Display last result
    if st.session_state.last_result:
        player_choice, opponent_choice, result_text = st.session_state.last_result
        
        st.markdown("---")
        st.markdown("### Last Round:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            player_name = "You" if st.session_state.game_mode == "single" else "Player 1"
            st.markdown(f'''
            <div class="choice-display">
                <h4>{player_name}</h4>
                {get_choice_emoji(player_choice)}
                <br><small>{player_choice}</small>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="choice-display">🆚</div>', unsafe_allow_html=True)
        
        with col3:
            opponent_name = "Computer" if st.session_state.game_mode == "single" else "Player 2"
            st.markdown(f'''
            <div class="choice-display">
                <h4>{opponent_name}</h4>
                {get_choice_emoji(opponent_choice)}
                <br><small>{opponent_choice}</small>
            </div>
            ''', unsafe_allow_html=True)
        
        # Result styling
        if "Win" in result_text:
            result_class = "winner"
        elif "Tie" in result_text:
            result_class = "tie"
        else:
            result_class = "loser"
        
        st.markdown(f'''
        <div class="result-text {result_class}">
            {result_text}
        </div>
        ''', unsafe_allow_html=True)

    # Reset scores button
    if st.session_state.games_played > 0:
        st.markdown("---")
        if st.button("🔄 Reset Scores", key="reset"):
            reset_scores()
            st.session_state.waiting_for_player2 = False
            st.session_state.player1_choice = None
            st.session_state.player2_choice = None
            st.rerun()

# Fun facts
with st.expander("🎯 Fun Facts about Rock Paper Scissors!"):
    st.write("""
    🎮 **Did you know?**
    - Rock Paper Scissors is over 2000 years old!
    - It's called "Jan-Ken-Pon" in Japan
    - There are World Championships for this game!
    - Paper beats Rock because paper can wrap around rock
    - Rock beats Scissors because rock can break scissors
    - Scissors beats Paper because scissors can cut paper
    
    **Strategy Tips for Kids:**
    - Most people start with Rock!
    - Try to notice patterns in how your opponent plays
    - Stay unpredictable by mixing up your choices
    - Have fun and don't worry about winning every time! 🌟
    """)