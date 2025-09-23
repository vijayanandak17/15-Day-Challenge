import streamlit as st
import time
from datetime import timedelta
import math

def create_circular_stopwatch_html(elapsed_time):
    # Calculate progress percentage (360 degrees = 60 seconds)
    progress_degrees = (elapsed_time % 60) * 6  # 6 degrees per second
    progress_percentage = (elapsed_time % 60) / 60 * 100
    
    # Format time display
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time * 1000) % 1000)
    time_text = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    # Create circular progress bar using CSS
    html_code = f"""
    <style>
    .stopwatch-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }}
    
    .circular-progress {{
        position: relative;
        height: 300px;
        width: 300px;
        border-radius: 50%;
        background: conic-gradient(#4CAF50 {progress_degrees}deg, #ededed 0deg);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    
    .circular-progress::before {{
        content: '';
        position: absolute;
        height: 270px;
        width: 270px;
        border-radius: 50%;
        background-color: white;
    }}
    
    .progress-content {{
        position: relative;
        font-size: 32px;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        z-index: 1;
    }}
    
    .time-display {{
        font-family: 'Courier New', monospace;
        font-size: 28px;
        margin-bottom: 5px;
    }}
    
    .progress-text {{
        font-size: 16px;
        color: #666;
    }}
    
    /* Animation for running state */
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.02); }}
        100% {{ transform: scale(1); }}
    }}
    
    .running {{
        animation: pulse 2s infinite;
    }}
    </style>
    
    <div class="stopwatch-container">
        <div class="circular-progress {'running' if st.session_state.running else ''}">
            <div class="progress-content">
                <div class="time-display">{time_text}</div>
                <div class="progress-text">{'RUNNING' if st.session_state.running else 'PAUSED'}</div>
            </div>
        </div>
    </div>
    """
    return html_code

def main():
    st.set_page_config(page_title="Circular Stopwatch", page_icon="⏱️", layout="centered")
    
    st.title("⏱️ Circular Stopwatch")
    st.markdown("---")
    
    # Initialize session state variables
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = 0
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = 0
    if 'last_update' not in st.session_state:
        st.session_state.last_update = 0
    
    # Display the circular stopwatch
    html_content = create_circular_stopwatch_html(st.session_state.elapsed_time)
    st.markdown(html_content, unsafe_allow_html=True)
    
    # Control buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col2:
        if not st.session_state.running:
            if st.button("🚀 **Start**", use_container_width=True, key="start"):
                st.session_state.running = True
                if st.session_state.elapsed_time == 0:
                    st.session_state.start_time = time.time()
                else:
                    # Resume from paused time
                    st.session_state.start_time = time.time() - st.session_state.elapsed_time
                st.session_state.last_update = time.time()
                st.rerun()
        else:
            if st.button("⏸️ **Stop**", use_container_width=True, key="stop"):
                st.session_state.running = False
                # Update elapsed time when stopping
                current_time = time.time()
                st.session_state.elapsed_time = current_time - st.session_state.start_time
                st.rerun()
    
    with col3:
        if st.button("🔄 **Reset**", use_container_width=True, key="reset"):
            st.session_state.running = False
            st.session_state.elapsed_time = 0
            st.session_state.start_time = 0
            st.rerun()
    
    # Update timer if running
    if st.session_state.running:
        current_time = time.time()
        st.session_state.elapsed_time = current_time - st.session_state.start_time
        
        # Auto-refresh every 100ms for smooth animation
        if current_time - st.session_state.last_update > 0.1:
            st.session_state.last_update = current_time
            st.rerun()
    
    # Display additional time information in cards
    st.markdown("---")
    st.subheader("Time Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        minutes = int(st.session_state.elapsed_time // 60)
        st.info(f"**Minutes:** {minutes:02d}")
    
    with col2:
        seconds = int(st.session_state.elapsed_time % 60)
        st.warning(f"**Seconds:** {seconds:02d}")
    
    with col3:
        milliseconds = int((st.session_state.elapsed_time * 1000) % 1000)
        st.success(f"**Milliseconds:** {milliseconds:03d}")
    
    # Status indicator
    status_color = "🟢" if st.session_state.running else "🔴"
    status_text = "Running" if st.session_state.running else "Stopped"
    st.markdown(f"**Status:** {status_color} {status_text}")
    
    # Add some custom CSS for better styling
    st.markdown("""
    <style>
    .stButton>button {
        height: 3em;
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    /* Style the metric cards */
    .stAlert {
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()