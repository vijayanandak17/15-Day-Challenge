import streamlit as st
import random
import time

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = [['', '', ''], ['', '', ''], ['', '', '']]
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = 'Two Player'
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'winning_line' not in st.session_state:
    st.session_state.winning_line = []

def check_winner(board):
    """Check if there's a winner and return the winner and winning line"""
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0], [(i, 0), (i, 1), (i, 2)]
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != '':
            return board[0][j], [(0, j), (1, j), (2, j)]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2], [(0, 2), (1, 1), (2, 0)]
    
    return None, []

def is_board_full(board):
    """Check if the board is full"""
    for row in board:
        if '' in row:
            return False
    return True

def get_available_moves(board):
    """Get list of available moves"""
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                moves.append((i, j))
    return moves

def computer_move():
    """Make a random computer move"""
    available_moves = get_available_moves(st.session_state.board)
    if available_moves and not st.session_state.game_over:
        row, col = random.choice(available_moves)
        st.session_state.board[row][col] = 'O'
        
        # Check for winner after computer move
        winner, winning_line = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
            st.session_state.winning_line = winning_line
            st.session_state.game_over = True
        elif is_board_full(st.session_state.board):
            st.session_state.game_over = True
        else:
            st.session_state.current_player = 'X'

def make_move(row, col):
    """Handle player move"""
    if st.session_state.board[row][col] == '' and not st.session_state.game_over:
        st.session_state.board[row][col] = st.session_state.current_player
        
        # Check for winner
        winner, winning_line = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
            st.session_state.winning_line = winning_line
            st.session_state.game_over = True
        elif is_board_full(st.session_state.board):
            st.session_state.game_over = True
        else:
            # Switch players or trigger computer move
            if st.session_state.game_mode == 'Two Player':
                st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
            else:  # Single Player mode
                st.session_state.current_player = 'O'
                # Trigger computer move after a short delay
                time.sleep(0.5)
                computer_move()

def reset_game():
    """Reset the game to initial state"""
    st.session_state.board = [['', '', ''], ['', '', ''], ['', '', '']]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_line = []

# Game statistics initialization
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0
if 'x_wins' not in st.session_state:
    st.session_state.x_wins = 0
if 'o_wins' not in st.session_state:
    st.session_state.o_wins = 0
if 'ties' not in st.session_state:
    st.session_state.ties = 0

# Update statistics when game ends
if st.session_state.game_over and 'stats_updated' not in st.session_state:
    st.session_state.games_played += 1
    if st.session_state.winner == 'X':
        st.session_state.x_wins += 1
    elif st.session_state.winner == 'O':
        st.session_state.o_wins += 1
    else:
        st.session_state.ties += 1
    st.session_state.stats_updated = True

# Reset stats flag when game is reset
if not st.session_state.game_over and 'stats_updated' in st.session_state:
    del st.session_state.stats_updated

def get_button_style(row, col):
    """Get the CSS style for a button based on its state"""
    if (row, col) in st.session_state.winning_line:
        return """
        background-color: #90EE90 !important;
        border: 3px solid #228B22 !important;
        color: #000000 !important;
        font-weight: bold !important;
        """
    else:
        return """
        background-color: #f0f0f0 !important;
        border: 2px solid #cccccc !important;
        color: #333333 !important;
        """

# Main app
st.title("🎮 Tic-Tac-Toe Game")

# Custom CSS for layout and buttons
st.markdown("""
<style>
.main-container {
    max-width: 800px;
    height: 400px;
    overflow: hidden;
}

.stButton > button {
    width: 70px !important;
    height: 70px !important;
    font-size: 24px !important;
    font-weight: bold !important;
    margin: 1px !important;
    background-color: #4472C4 !important;
    border: 2px solid #2E5AAC !important;
    color: white !important;
}

.stButton > button:hover {
    background-color: #5A82D4 !important;
    border: 2px solid #4472C4 !important;
}

.stButton > button:disabled {
    background-color: #E6E6E6 !important;
    border: 2px solid #CCCCCC !important;
    color: #666666 !important;
}

.info-panel {
    padding: 8px;
    background-color: #f8f9fa;
    border-radius: 8px;
    height: 340px;
    font-size: 13px;
}

/* Reduce spacing for compact layout */
.stRadio > div {
    gap: 0.5rem;
}

.element-container {
    margin-bottom: 0.5rem !important;
}

h4 {
    margin-top: 0.5rem !important;
    margin-bottom: 0.3rem !important;
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)

# Main layout: Board on left, Info panel on right
main_col1, main_col2 = st.columns([1.2, 1])

with main_col1:
    # Game mode selection and reset button
    mode_col1, mode_col2 = st.columns([2, 1])
    with mode_col1:
        game_mode = st.radio("Game Mode:", ["Two Player", "Single Player (vs Computer)"], 
                            index=0 if st.session_state.game_mode == 'Two Player' else 1)
        if game_mode != st.session_state.game_mode:
            st.session_state.game_mode = game_mode
            reset_game()
    
    with mode_col2:
        if st.button("🔄 Reset", type="secondary"):
            reset_game()
            st.rerun()
    
    # Game status
    if not st.session_state.game_over:
        if st.session_state.game_mode == 'Two Player':
            st.info(f"Current Player: **{st.session_state.current_player}**")
        else:
            if st.session_state.current_player == 'X':
                st.info("Your turn: **X**")
            else:
                st.info("Computer thinking... **O**")
    else:
        if st.session_state.winner:
            if st.session_state.game_mode == 'Single Player' and st.session_state.winner == 'O':
                st.error("🤖 Computer wins!")
            elif st.session_state.game_mode == 'Single Player' and st.session_state.winner == 'X':
                st.success("🎉 You win!")
            else:
                st.success(f"🎉 Player {st.session_state.winner} wins!")
        else:
            st.warning("🤝 It's a tie!")
    
    # Game board
    st.markdown("**Game Board:**")
    
    # Create the 3x3 grid
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            with cols[j]:
                button_text = st.session_state.board[i][j] if st.session_state.board[i][j] != '' else ' '
                
                # Apply custom styling for winning line
                if (i, j) in st.session_state.winning_line:
                    st.markdown(f"""
                    <style>
                    div[data-testid="column"]:nth-child({j+1}) .stButton > button {{
                        background-color: #90EE90 !important;
                        border: 3px solid #228B22 !important;
                        color: #000000 !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                elif st.session_state.board[i][j] == '':
                    # Apply blue styling for empty buttons
                    st.markdown(f"""
                    <style>
                    div[data-testid="column"]:nth-child({j+1}) .stButton > button {{
                        background-color: #4472C4 !important;
                        border: 2px solid #2E5AAC !important;
                        color: white !important;
                    }}
                    div[data-testid="column"]:nth-child({j+1}) .stButton > button:hover {{
                        background-color: #5A82D4 !important;
                        border: 2px solid #4472C4 !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                else:
                    # Styling for filled buttons (X or O)
                    st.markdown(f"""
                    <style>
                    div[data-testid="column"]:nth-child({j+1}) .stButton > button {{
                        background-color: #E6E6E6 !important;
                        border: 2px solid #CCCCCC !important;
                        color: #000000 !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                
                if st.button(button_text, key=f"btn_{i}_{j}", disabled=st.session_state.board[i][j] != '' or st.session_state.game_over):
                    make_move(i, j)
                    st.rerun()

with main_col2:
        
    # Instructions
    st.markdown("#### How to Play:")
    st.markdown("""
    **Two Player Mode:**
    - Players take turns (X goes first)
    - Click empty squares to make moves
    
    **Single Player Mode:**
    - You are X, computer is O
    - Computer makes random moves
    
    **Winning:**
    - Get 3 in a row (horizontally, vertically, or diagonally)
    - Winning line highlights in green
    - Click 'Reset' to start over
    """)
    
    st.markdown("---")

    
    # Game Statistics
    if st.session_state.games_played > 0:
        st.markdown("#### Game Statistics:")
        st.write(f"**Games Played:** {st.session_state.games_played}")
        st.write(f"**X Wins:** {st.session_state.x_wins}")
        st.write(f"**O Wins:** {st.session_state.o_wins}")
        st.write(f"**Ties:** {st.session_state.ties}")
        
        if st.session_state.games_played > 0:
            x_win_rate = (st.session_state.x_wins / st.session_state.games_played) * 100
            st.write(f"**X Win Rate:** {x_win_rate:.1f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)