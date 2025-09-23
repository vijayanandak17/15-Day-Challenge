import streamlit as st
import random

st.set_page_config(page_title="Rock-Paper-Scissors", page_icon="✂️")

# --- Initialize Session State for Scores ---
if 'scores' not in st.session_state:
    st.session_state.scores = {'player1': 0, 'player2': 0, 'computer': 0}

# --- Game Logic ---
def get_winner(player1_choice, player2_choice):
    """Determines the winner of a single round."""
    if player1_choice == player2_choice:
        return 'draw'
    
    if (player1_choice == 'rock' and player2_choice == 'scissors') or \
       (player1_choice == 'scissors' and player2_choice == 'paper') or \
       (player1_choice == 'paper' and player2_choice == 'rock'):
        return 'player1'
    else:
        return 'player2'

def play_round_one_player(player_choice):
    """Handles the game logic for one-player mode."""
    computer_choice = random.choice(['rock', 'paper', 'scissors'])
    st.session_state.player_choice = player_choice
    st.session_state.computer_choice = computer_choice
    
    winner = get_winner(player_choice, computer_choice)
    
    if winner == 'player1':
        st.session_state.scores['player1'] += 1
        st.session_state.result_message = f"You chose {player_choice}. The computer chose {computer_choice}. 🎉 You win!"
        st.balloons()
    elif winner == 'player2':
        st.session_state.scores['computer'] += 1
        st.session_state.result_message = f"You chose {player_choice}. The computer chose {computer_choice}. 💻 The computer wins!"
    else:
        st.session_state.result_message = f"You both chose {player_choice}. 🤝 It's a draw!"

def play_round_two_player(player1_choice, player2_choice):
    """Handles the game logic for two-player mode."""
    st.session_state.p1_choice = player1_choice
    st.session_state.p2_choice = player2_choice

    winner = get_winner(player1_choice, player2_choice)

    if winner == 'player1':
        st.session_state.scores['player1'] += 1
        st.session_state.result_message = f"Player 1 chose {player1_choice}. Player 2 chose {player2_choice}. 🎉 Player 1 wins!"
        st.balloons()
    elif winner == 'player2':
        st.session_state.scores['player2'] += 1
        st.session_state.result_message = f"Player 1 chose {player1_choice}. Player 2 chose {player2_choice}. 🥳 Player 2 wins!"
        st.balloons()
    else:
        st.session_state.result_message = f"Player 1 chose {player1_choice}. Player 2 chose {player2_choice}. 🤝 It's a draw!"

# --- UI Layout and Styling ---
st.title("✂️ Rock-Paper-Scissors Fun! 🗿📜")
st.markdown("### Let's Play!")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Player vs Computer")
    st.write("Can you beat the computer?")
    
    with st.expander("How to Play", expanded=False):
        st.markdown("""
        - **Rock** crushes **Scissors**
        - **Scissors** cuts **Paper**
        - **Paper** covers **Rock**
        """)
        
    choice_emojis = {'rock': '🗿', 'paper': '📜', 'scissors': '✂️'}
    
    # One-player buttons
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Rock", key='1p_rock'):
            play_round_one_player('rock')
    with c2:
        if st.button("Paper", key='1p_paper'):
            play_round_one_player('paper')
    with c3:
        if st.button("Scissors", key='1p_scissors'):
            play_round_one_player('scissors')
            
    # Display one-player result
    if 'result_message' in st.session_state and st.session_state.get('p2_choice') is None:
        st.success(st.session_state.result_message)
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="font-size: 24px;">
                You: {choice_emojis.get(st.session_state.player_choice)} vs Computer: {choice_emojis.get(st.session_state.computer_choice)}
            </p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("Player 1 vs Player 2")
    st.write("Challenge a friend!")

    with st.expander("How to Play", expanded=False):
        st.markdown("""
        - **Rock** crushes **Scissors**
        - **Scissors** cuts **Paper**
        - **Paper** covers **Rock**
        """)

    # Two-player choice selection
    player1_choice = st.radio("Player 1's choice:", ['rock', 'paper', 'scissors'], key='p1_radio', format_func=lambda x: x.capitalize())
    player2_choice = st.radio("Player 2's choice:", ['rock', 'paper', 'scissors'], key='p2_radio', format_func=lambda x: x.capitalize())

    if st.button("Let's Play!", key='2p_play'):
        play_round_two_player(player1_choice, player2_choice)
    
    # Display two-player result
    if 'result_message' in st.session_state and st.session_state.get('p2_choice') is not None:
        st.success(st.session_state.result_message)
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="font-size: 24px;">
                Player 1: {choice_emojis.get(st.session_state.p1_choice)} vs Player 2: {choice_emojis.get(st.session_state.p2_choice)}
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# --- Scoreboard ---
st.subheader("🏆 Scoreboard")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("You", st.session_state.scores['player1'])
with c2:
    st.metric("Computer", st.session_state.scores['computer'])
with c3:
    st.metric("Player 2", st.session_state.scores['player2'])

if st.button("Reset Score"):
    st.session_state.scores = {'player1': 0, 'player2': 0, 'computer': 0}
    st.session_state.result_message = ""
    st.rerun()

st.markdown("""
<style>
    .stButton>button {
        font-size: 20px;
        padding: 10px 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        background-color: #E8F5E9;
        color: #1B5E20;
        cursor: pointer;
    }
    .stRadio > label {
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)