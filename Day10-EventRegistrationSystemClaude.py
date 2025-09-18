import streamlit as st
import pandas as pd
from datetime import datetime, date
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="A.R. Rahman Concert - Chennai 2025",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for laptop-optimized design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .concert-info {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 0.8rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .registration-form {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: #333;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .event-date-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 0.5rem;
        border-radius: 8px;
        margin: 0.2rem 0;
        text-align: center;
        color: #333;
        font-size: 0.85rem;
    }
    
    .compact-info {
        background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        color: #333;
    }
    
    .music-emoji {
        font-size: 1.5rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-5px);
        }
        60% {
            transform: translateY(-2px);
        }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.4rem 1.5rem;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    h1 { font-size: 1.8rem !important; margin: 0.5rem 0 !important; }
    h2 { font-size: 1.3rem !important; margin: 0.3rem 0 !important; }
    h3 { font-size: 1.1rem !important; margin: 0.5rem 0 !important; }
    
    .stSelectbox > div > div > div { padding: 0.3rem 0.5rem; }
    .stTextInput > div > div > input { padding: 0.3rem 0.5rem; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'registrations' not in st.session_state:
    st.session_state.registrations = []

# Helper function to create downloadable CSV
def create_csv_download():
    if st.session_state.registrations:
        df = pd.DataFrame(st.session_state.registrations)
        return df
    return None

# Main header - compact
st.markdown("""
<div class="main-header">
    <div class="music-emoji">🎵🎤🎸🎹🎵</div>
    <h1>A.R. RAHMAN CONCERT 2025</h1>
    <h2>The Mozart of Madras Live in Chennai!</h2>
</div>
""", unsafe_allow_html=True)

# Concert information - compact
st.markdown("""
<div class="compact-info">
    <strong>📅 Nov 1-7, 2025</strong> | <strong>📍 Nehru Stadium, Chennai</strong> | <strong>🕒 7:00 PM</strong> | <strong>🎫 A magical evening with A.R. Rahman!</strong>
</div>
""", unsafe_allow_html=True)

# Create three columns for better laptop layout
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # Registration form - compact
    st.markdown('<div class="registration-form">', unsafe_allow_html=True)
    st.markdown("### 🎫 Register Now")
    
    with st.form("registration_form"):
        # Form inputs in two columns to save space
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            name = st.text_input("👤 Full Name", placeholder="Your name")
        with form_col2:
            email = st.text_input("📧 Email", placeholder="Your email")
        
        # Event date selection - more compact
        event_dates = [
            "Nov 1 (Fri)", "Nov 2 (Sat)", "Nov 3 (Sun)", "Nov 4 (Mon)",
            "Nov 5 (Tue)", "Nov 6 (Wed)", "Nov 7 (Thu)"
        ]
        
        selected_date = st.selectbox("🗓️ Concert Date:", event_dates)
        
        # Submit button
        submitted = st.form_submit_button("🎵 Register!", use_container_width=True)
        
        if submitted:
            if name and email and selected_date:
                if '@' in email and '.' in email.split('@')[1]:
                    registration = {
                        'Name': name,
                        'Email': email,
                        'Event Date': selected_date,
                        'Registration Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    st.session_state.registrations.append(registration)
                    st.success(f"🎉 Registered for {selected_date}!")
                    st.balloons()
                else:
                    st.error("❌ Invalid email")
            else:
                st.error("❌ Fill all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Live registration count
    st.markdown(f"""
    <div class="stats-card">
        <h3>📊 Registrations</h3>
        <h1 style="color: #667eea; font-size: 2.5rem;">{len(st.session_state.registrations)}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Recent registrations - compact
    if st.session_state.registrations:
        st.markdown("**🕒 Recent:**")
        recent_regs = st.session_state.registrations[-3:]
        for reg in reversed(recent_regs):
            st.write(f"• {reg['Name']} ({reg['Event Date']})")

with col3:
    # Event dates - compact grid
    st.markdown("**🗓️ Concert Dates:**")
    dates_info = [
        ("Nov 1", "🌟"), ("Nov 2", "🎭"), ("Nov 3", "🎵"), ("Nov 4", "🎤"),
        ("Nov 5", "🎸"), ("Nov 6", "🎹"), ("Nov 7", "🥁")
    ]
    
    for date_info, emoji in dates_info:
        st.markdown(f"""
        <div class="event-date-card">
            {emoji} {date_info}
        </div>
        """, unsafe_allow_html=True)

# Analytics and tools - compact layout
if st.session_state.registrations:
    st.markdown("---")
    
    # Four columns for compact analytics
    anal_col1, anal_col2, anal_col3, anal_col4 = st.columns(4)
    
    df = pd.DataFrame(st.session_state.registrations)
    date_counts = df['Event Date'].value_counts()
    
    with anal_col1:
        st.markdown("**📈 By Date:**")
        for date, count in list(date_counts.items())[:3]:
            st.write(f"• {date}: {count}")
    
    with anal_col2:
        st.markdown("**🔢 Stats:**")
        st.write(f"• Total: {len(st.session_state.registrations)}")
        st.write(f"• Most popular: {date_counts.index[0] if not date_counts.empty else 'None'}")
    
    with anal_col3:
        if st.button("📋 View All", use_container_width=True):
            st.dataframe(df, use_container_width=True, height=200)
    
    with anal_col4:
        if st.session_state.registrations:
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="💾 Export CSV",
                data=csv_data,
                file_name=f"registrations_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# Compact footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem; margin-top: 1rem; border-top: 1px solid #eee;">
    <p>🎵 <strong>A.R. Rahman Concert 2025</strong> - Experience the magic of music! 🎵</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh button - compact
col_refresh, col_space = st.columns([1, 3])
with col_refresh:
    if st.button("🔄 Refresh"):
        st.rerun()