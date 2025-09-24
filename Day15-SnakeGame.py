import streamlit as st
import random
import time
import pandas as pd
from typing import List, Tuple, Optional

# Configure the page
st.set_page_config(
    page_title="Snake Game Pro",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .game-stats {
        display: flex;
        justify-content: space-around;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stat-box {
        text-align: center;
        color: white;
        font-weight: bold;
    }
    
    .stat-value {
        font-size: 2rem;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .game-board {
        background: #f8f9fa;
        border: 3px solid #2E8B57;
        border-radius: 10px;
        padding: 10px;
        margin: 20px auto;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .control-panel {
        background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .game-over {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .instructions {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    div.stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        margin: 0.2rem;
        transition: all 0.3s ease;
    }
    
    .direction-buttons {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        max-width: 200px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

class SnakeGame:
    def __init__(self, width: int = 20, height: int = 15):
        self.width = width
        self.height = height
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (1, 0)  # Moving right initially
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.game_won = False
    
    def generate_food(self) -> Tuple[int, int]:
        """Generate food at a random position not occupied by snake"""
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake:
                return food
    
    def move_snake(self):
        """Move the snake in the current direction"""
        if self.game_over:
            return
        
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            
            # Check win condition (snake fills most of the board)
            if len(self.snake) >= (self.width * self.height * 0.8):
                self.game_won = True
        else:
            self.snake.pop()  # Remove tail if no food eaten
    
    def change_direction(self, new_direction: Tuple[int, int]):
        """Change snake direction, preventing 180-degree turns"""
        current_dx, current_dy = self.direction
        new_dx, new_dy = new_direction
        
        # Prevent 180-degree turns
        if (current_dx, current_dy) != (-new_dx, -new_dy):
            self.direction = new_direction
    
    def get_board_display(self) -> List[List[str]]:
        """Get the current board state for display"""
        board = [['⬜' for _ in range(self.width)] for _ in range(self.height)]
        
        # Place food
        food_x, food_y = self.food
        board[food_y][food_x] = '🍎'
        
        # Place snake
        for i, (x, y) in enumerate(self.snake):
            if i == 0:  # Head
                board[y][x] = '🟢'
            else:  # Body
                board[y][x] = '🟩'
        
        return board

# Initialize session state
if 'game' not in st.session_state:
    st.session_state.game = SnakeGame()
if 'auto_move' not in st.session_state:
    st.session_state.auto_move = False
if 'game_speed' not in st.session_state:
    st.session_state.game_speed = 0.3

# Main game interface
st.markdown('<h1 class="main-header">🐍 Snake Game Pro</h1>', unsafe_allow_html=True)

# Game statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="stat-box">
        <span class="stat-value">{st.session_state.game.score}</span>
        <span class="stat-label">SCORE</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-box">
        <span class="stat-value">{len(st.session_state.game.snake)}</span>
        <span class="stat-label">LENGTH</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    status = "🔴 Game Over" if st.session_state.game.game_over else "🏆 You Won!" if st.session_state.game.game_won else "🟢 Playing"
    st.markdown(f"""
    <div class="stat-box">
        <span class="stat-value" style="font-size: 1.2rem;">{status}</span>
        <span class="stat-label">STATUS</span>
    </div>
    """, unsafe_allow_html=True)

# Game board
st.markdown('<div class="game-board">', unsafe_allow_html=True)
board = st.session_state.game.get_board_display()

# Create board display using columns
board_container = st.container()
with board_container:
    for row in board:
        cols = st.columns(len(row))
        for j, cell in enumerate(row):
            with cols[j]:
                st.markdown(f"<div style='text-align: center; font-size: 1.5rem;'>{cell}</div>", 
                           unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Control panel
st.markdown('<div class="control-panel">', unsafe_allow_html=True)
st.markdown("### 🎮 Game Controls")

# Direction buttons
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col1:
    if st.button("⬅️ Left", key="left"):
        st.session_state.game.change_direction((-1, 0))

with col2:
    if st.button("⬆️ Up", key="up"):
        st.session_state.game.change_direction((0, -1))

with col3:
    if st.button("⬇️ Down", key="down"):
        st.session_state.game.change_direction((0, 1))

with col4:
    if st.button("➡️ Right", key="right"):
        st.session_state.game.change_direction((1, 0))

with col5:
    if st.button("🔄 Move", key="manual_move"):
        if not st.session_state.game.game_over and not st.session_state.game.game_won:
            st.session_state.game.move_snake()
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Auto-play controls
col1, col2 = st.columns(2)
with col1:
    auto_play = st.checkbox("🤖 Auto Play", value=st.session_state.auto_move)
    st.session_state.auto_move = auto_play

with col2:
    speed = st.selectbox(
        "⚡ Speed",
        options=[0.5, 0.3, 0.2, 0.1],
        index=1,
        format_func=lambda x: f"{'🐌 Slow' if x == 0.5 else '🚶 Normal' if x == 0.3 else '🏃 Fast' if x == 0.2 else '⚡ Lightning'}"
    )
    st.session_state.game_speed = speed

# Auto-move logic
if st.session_state.auto_move and not st.session_state.game.game_over and not st.session_state.game.game_won:
    time.sleep(st.session_state.game_speed)
    st.session_state.game.move_snake()
    st.rerun()

# Game over/won screen
if st.session_state.game.game_over:
    st.markdown(f"""
    <div class="game-over">
        <h2>🎮 Game Over!</h2>
        <p>Your snake crashed! Final Score: <strong>{st.session_state.game.score}</strong></p>
        <p>Snake Length: <strong>{len(st.session_state.game.snake)}</strong></p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.game.game_won:
    st.markdown(f"""
    <div class="game-over" style="background: linear-gradient(135deg, #48c6ef 0%, #6f86d6 100%);">
        <h2>🏆 Congratulations!</h2>
        <p>You won! Final Score: <strong>{st.session_state.game.score}</strong></p>
        <p>You're a Snake Master! 🐍👑</p>
    </div>
    """, unsafe_allow_html=True)

# Restart button
if st.button("🔄 Start New Game", key="restart"):
    st.session_state.game = SnakeGame()
    st.session_state.auto_move = False
    st.rerun()

# Instructions
with st.expander("📖 How to Play", expanded=False):
    st.markdown("""
    <div class="instructions">
        <h4>🎯 Objective</h4>
        <p>Control the snake to eat apples (🍎) and grow longer while avoiding walls and your own body!</p>
        
        <h4>🎮 Controls</h4>
        <ul>
            <li><strong>Direction Buttons:</strong> Use ⬅️⬆️⬇️➡️ buttons to change direction</li>
            <li><strong>Manual Move:</strong> Click "🔄 Move" to advance one step</li>
            <li><strong>Auto Play:</strong> Enable for automatic movement</li>
            <li><strong>Speed Control:</strong> Adjust how fast the snake moves</li>
        </ul>
        
        <h4>📊 Scoring</h4>
        <ul>
            <li>Each apple eaten = <strong>+10 points</strong></li>
            <li>Snake grows by 1 segment per apple</li>
            <li>Try to achieve the highest score possible!</li>
        </ul>
        
        <h4>🏆 Win Condition</h4>
        <p>Fill 80% of the board to achieve victory!</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "🐍 Snake Game Pro | Built with Streamlit | Enjoy Playing! 🎮"
    "</div>", 
    unsafe_allow_html=True
)