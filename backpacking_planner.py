import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Backpacking Trip Planner",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS styling with modern interactive theme
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Hide sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Modern color palette */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        
        --primary: #667eea;
        --primary-light: #8b9aff;
        --secondary: #f5576c;
        --background: #ffffff;
        --surface: #f8fafc;
        --surface-elevated: #ffffff;
        --border: #e2e8f0;
        --border-light: #f1f5f9;
        --text-primary: #1a202c;
        --text-secondary: #4a5568;
        --text-light: #718096;
        
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        
        --radius-sm: 6px;
        --radius: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Main container */
    .main .block-container {
        padding: 1rem;
        max-width: 1400px;
        background: var(--background);
    }
    
    /* Animated header */
    .app-header {
        background: var(--primary-gradient);
        color: white;
        padding: 4rem 2rem;
        border-radius: var(--radius-xl);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
        animation: headerSlideIn 1s ease-out;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes headerSlideIn {
        from {
            transform: translateY(-50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .app-header h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        letter-spacing: -0.02em;
    }
    
    .app-header p {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        margin: 1rem 0 0 0;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Interactive cards */
    .card {
        background: var(--surface-elevated);
        border-radius: var(--radius-lg);
        padding: 2rem;
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-sm);
        margin-bottom: 2rem;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
        transform: scaleX(0);
        transition: var(--transition);
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary);
    }
    
    .card:hover::before {
        transform: scaleX(1);
    }
    
    /* Stats overview with animations */
    .stats-overview {
        background: var(--surface);
        padding: 2rem;
        border-radius: var(--radius-lg);
        border: 1px solid var(--border);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-md);
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            transform: translateY(30px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    /* Enhanced section headers */
    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 3rem 0 2rem 0;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: var(--primary-gradient);
        border-radius: 2px;
    }
    
    /* Modern transport section */
    .transport-section {
        background: linear-gradient(135deg, #e6f3ff 0%, #cce7ff 100%);
        padding: 1.5rem;
        border-radius: var(--radius-lg);
        border: 2px solid #b3d9ff;
        margin-bottom: 1rem;
        transition: var(--transition);
        position: relative;
    }
    
    .transport-section::before {
        content: '🚌';
        position: absolute;
        top: -10px;
        right: 15px;
        font-size: 1.5rem;
        background: white;
        padding: 5px 10px;
        border-radius: 20px;
        box-shadow: var(--shadow-sm);
    }
    
    .transport-section:hover {
        transform: translateX(5px);
        border-color: var(--primary);
    }
    
    /* Modern accommodation section */
    .accommodation-section {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4e8 100%);
        padding: 1.5rem;
        border-radius: var(--radius-lg);
        border: 2px solid #ffb3c1;
        margin-bottom: 1rem;
        transition: var(--transition);
        position: relative;
    }
    
    .accommodation-section::before {
        content: '🏨';
        position: absolute;
        top: -10px;
        right: 15px;
        font-size: 1.5rem;
        background: white;
        padding: 5px 10px;
        border-radius: 20px;
        box-shadow: var(--shadow-sm);
    }
    
    .accommodation-section:hover {
        transform: translateX(5px);
        border-color: var(--secondary);
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: var(--radius-lg);
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        padding: 1rem 2rem;
        transition: var(--transition);
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: var(--transition);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-xl);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Enhanced inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input {
        border: 2px solid var(--border);
        border-radius: var(--radius);
        font-family: 'Inter', sans-serif;
        background: var(--surface-elevated);
        transition: var(--transition);
        padding: 0.75rem 1rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
        transform: translateY(-2px);
    }
    
    /* Modern tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: var(--surface);
        padding: 0.75rem;
        border-radius: var(--radius-lg);
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-radius: var(--radius);
        color: var(--text-secondary);
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 1rem 1.5rem;
        transition: var(--transition);
        position: relative;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient);
        color: white;
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    
    /* Enhanced expander */
    .streamlit-expanderHeader {
        background: var(--surface-elevated);
        border: 2px solid var(--border);
        border-radius: var(--radius-lg) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        transition: var(--transition);
        padding: 1rem 1.5rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--surface);
        border-color: var(--primary);
        transform: translateX(5px);
        box-shadow: var(--shadow-md);
    }
    
    /* Enhanced alerts */
    .stSuccess {
        background: var(--success-gradient);
        border-radius: var(--radius-lg);
        border: none;
        box-shadow: var(--shadow-md);
        animation: slideInRight 0.5s ease-out;
    }
    
    .stWarning {
        background: var(--warning-gradient);
        border-radius: var(--radius-lg);
        border: none;
        box-shadow: var(--shadow-md);
        animation: slideInRight 0.5s ease-out;
    }
    
    .stError {
        background: var(--secondary-gradient);
        border-radius: var(--radius-lg);
        border: none;
        box-shadow: var(--shadow-md);
        animation: slideInRight 0.5s ease-out;
    }
    
    .stInfo {
        background: var(--primary-gradient);
        border-radius: var(--radius-lg);
        border: none;
        box-shadow: var(--shadow-md);
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Enhanced charts */
    .js-plotly-plot {
        border-radius: var(--radius-lg);
        border: 1px solid var(--border);
        background: var(--surface-elevated);
        box-shadow: var(--shadow-md);
        transition: var(--transition);
    }
    
    .js-plotly-plot:hover {
        box-shadow: var(--shadow-lg);
    }
    
    /* Typography improvements */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        line-height: 1.2 !important;
    }
    
    p, div, span, label {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-secondary) !important;
        line-height: 1.6 !important;
    }
    
    /* Metrics enhancement */
    [data-testid="metric-container"] {
        background: var(--surface-elevated);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        transition: var(--transition);
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--primary);
    }
    
    /* Footer enhancement */
    .footer {
        background: var(--primary-gradient);
        color: white;
        text-align: center;
        padding: 3rem 2rem;
        border-radius: var(--radius-xl);
        margin-top: 4rem;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>');
        opacity: 0.1;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .app-header h1 {
            font-size: 2.5rem;
        }
        
        .main .block-container {
            padding: 0.5rem;
        }
        
        .card {
            padding: 1rem;
        }
        
        .section-header {
            font-size: 2rem;
        }
    }
    
    /* Scroll animations */
    .animate-on-scroll {
        opacity: 0;
        transform: translateY(30px);
        transition: var(--transition);
    }
    
    .animate-on-scroll.visible {
        opacity: 1;
        transform: translateY(0);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state with enhanced structure
def init_session_state():
    if 'trip_data' not in st.session_state:
        st.session_state.trip_data = []
    if 'budget_data' not in st.session_state:
        st.session_state.budget_data = {
            'total_budget': 1000.0,
            'spent': 0.0,
            'categories': {},
            'currency': '£'
        }
    if 'trip_info' not in st.session_state:
        st.session_state.trip_info = {
            'name': '',
            'start_date': None,
            'end_date': None,
            'destinations': '',
            'travel_style': 'Budget Backpacker',
            'group_size': 1
        }
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {
            'theme': 'light',
            'currency': 'GBP',
            'notifications': True
        }

def main():
    # Initialize session state
    init_session_state()
    
    # Load CSS
    load_css()
    
    # Enhanced header with animation
    st.markdown("""
    <div class="app-header">
        <h1>🎒 Adventure Planner</h1>
        <p>Plan your perfect backpacking journey with style and precision</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats if trip data exists
    if st.session_state.trip_data:
        show_enhanced_stats()
    
    # Enhanced navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌍 Trip Overview", 
        "📅 Day-by-Day Planning", 
        "💰 Budget Calculator", 
        "📊 Analytics", 
        "📋 Trip Summary"
    ])
    
    with tab1:
        trip_overview()
    
    with tab2:
        day_by_day_planning()
    
    with tab3:
        budget_calculator()
    
    with tab4:
        analytics_dashboard()
    
    with tab5:
        trip_summary()
    
    # Enhanced footer
    st.markdown("""
    <div class="footer">
        <p>🎒 Crafted with ❤️ for adventurers worldwide | Safe travels! 🌟</p>
        <p style="opacity: 0.8; font-size: 0.9rem; margin-top: 1rem;">
            Plan • Explore • Adventure • Repeat
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_enhanced_stats():
    """Display enhanced trip statistics with animations"""
    total_days = len(st.session_state.trip_data)
    total_transport = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
    total_accommodation = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
    total_cost = total_transport + total_accommodation
    budget = st.session_state.budget_data['total_budget']
    remaining = budget - total_cost
    
    st.markdown("""
    <div class="stats-overview">
        <h3 style="text-align: center; margin-bottom: 2rem; font-family: 'Space Grotesk', sans-serif;">
            📊 Your Adventure at a Glance
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "📅 Duration", 
            f"{total_days} days",
            delta=f"{total_days/7:.1f} weeks" if total_days > 7 else None
        )
    with col2:
        st.metric(
            "🚌 Transport", 
            f"£{total_transport:.0f}",
            delta=f"{total_transport/total_days:.0f}/day" if total_days > 0 else None
        )
    with col3:
        st.metric(
            "🏨 Accommodation", 
            f"£{total_accommodation:.0f}",
            delta=f"{total_accommodation/total_days:.0f}/day" if total_days > 0 else None
        )
    with col4:
        st.metric(
            "💰 Total Cost", 
            f"£{total_cost:.0f}",
            delta=f"{(total_cost/budget*100):.1f}% of budget"
        )
    with col5:
        st.metric(
            "💸 Remaining", 
            f"£{remaining:.0f}",
            delta="Over budget!" if remaining < 0 else "Within budget",
            delta_color="inverse" if remaining < 0 else "normal"
        )

def trip_overview():
    """Enhanced trip overview with better UX"""
    st.markdown('<h2 class="section-header">🌍 Trip Overview</h2>', unsafe_allow_html=True)
    
    # Trip basic information
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Basic Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trip_name = st.text_input(
            "🎯 Trip Name", 
            value=st.session_state.trip_info['name'],
            placeholder="e.g., European Adventure, Southeast Asia Explorer",
            help="Give your adventure a memorable name!"
        )
        
        start_date = st.date_input(
            "📅 Start Date", 
            value=st.session_state.trip_info['start_date'],
            help="When does your adventure begin?"
        )
        
        end_date = st.date_input(
            "🏁 End Date", 
            value=st.session_state.trip_info['end_date'],
            help="When do you plan to return?"
        )
        
    with col2:
        destinations = st.text_area(
            "🗺️ Main Destinations", 
            value=st.session_state.trip_info['destinations'],
            placeholder="List the places you're most excited to visit...",
            height=120,
            help="Describe your must-visit destinations"
        )
        
        total_budget = st.number_input(
            "💰 Total Budget (£)", 
            min_value=0.0, 
            value=st.session_state.budget_data['total_budget'],
            step=100.0,
            help="Set your overall trip budget - be realistic!"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Travel preferences with enhanced UI
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Travel Preferences")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        travel_style = st.selectbox(
            "✈️ Travel Style", 
            [
                "🎒 Budget Backpacker (£25-40/day)", 
                "🌟 Mid-range Explorer (£40-70/day)", 
                "💎 Comfort Traveller (£70+/day)"
            ],
            help="Choose your travel comfort level"
        )
    with col2:
        group_size = st.number_input(
            "👥 Group Size", 
            min_value=1, 
            max_value=20, 
            value=st.session_state.trip_info.get('group_size', 1), 
            step=1,
            help="How many travelers in your group?"
        )
    with col3:
        transport_preference = st.selectbox(
            "🚌 Preferred Transport", 
            ["🚌 Bus", "🚂 Train", "🔄 Mix of Both", "✈️ Budget Airlines", "🚗 Car Rental"],
            help="Your preferred way to get around"
        )
    with col4:
        accommodation_preference = st.selectbox(
            "🏨 Accommodation Style",
            ["🏠 Hostels", "🏨 Hotels", "🏡 Mix of Both", "⛺ Camping", "🏘️ Local Stays"],
            help="Where do you prefer to stay?"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced save functionality
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Save Trip Overview", type="primary", use_container_width=True):
            st.session_state.trip_info.update({
                'name': trip_name,
                'start_date': start_date,
                'end_date': end_date,
                'destinations': destinations,
                'travel_style': travel_style,
                'group_size': group_size
            })
            st.session_state.budget_data['total_budget'] = total_budget
            
            st.success("✅ Trip overview saved! Ready to plan your adventure!")
            
            # Auto-suggest days with enhanced logic
            if start_date and end_date and end_date > start_date:
                suggested_days = (end_date - start_date).days + 1
                if suggested_days > len(st.session_state.trip_data):
                    st.info(f"📅 Based on your dates, you might want to plan {suggested_days} days. Head to Day-by-Day Planning to add more days!")
                
                # Budget suggestions based on travel style
                daily_budget_low = 25 if "Budget" in travel_style else 40 if "Mid-range" in travel_style else 70
                daily_budget_high = 40 if "Budget" in travel_style else 70 if "Mid-range" in travel_style else 120
                suggested_budget = (daily_budget_low + daily_budget_high) / 2 * suggested_days
                
                if total_budget < suggested_budget * 0.8:
                    st.warning(f"💡 For a {suggested_days}-day {travel_style.split('(')[0].strip()}, consider budgeting £{suggested_budget:.0f}-£{suggested_budget*1.3:.0f}")

def day_by_day_planning():
    """Enhanced day-by-day planning with better UX"""
    st.markdown('<h2 class="section-header">📅 Day-by-Day Planning</h2>', unsafe_allow_html=True)
    
    # Enhanced add days section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        if st.button("➕ Add New Day", type="primary"):
            add_new_day()
    
    with col2:
        days_to_add = st.number_input("Add Multiple", min_value=1, max_value=30, value=1, step=1)
    
    with col3:
        if st.button(f"Add {days_to_add} Days"):
            for _ in range(int(days_to_add)):
                add_new_day()
            st.rerun()
    
    with col4:
        if st.session_state.trip_data and st.button("🗑️ Clear All", type="secondary"):
            if st.checkbox("Confirm clear all days"):
                st.session_state.trip_data = []
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 4rem 2rem;">
            <h3>🎒 Ready to start your adventure?</h3>
            <p style="font-size: 1.1rem; margin: 1rem 0;">Click "Add New Day" above to begin planning your journey!</p>
            <p style="color: var(--text-light);"><strong>💡 Pro Tip:</strong> Plan transport between locations first, then add accommodation</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display days with enhanced UI
    for i, day_data in enumerate(st.session_state.trip_data):
        day_cost = day_data.get('transport_cost', 0.0) + day_data.get('accommodation_cost', 0.0)
        
        # Enhanced expander with progress indicator
        progress_indicator = "🟢" if day_data.get('location') and day_data.get('transport_from') else "🟡" if day_data.get('location') else "🔴"
        
        with st.expander(f"{progress_indicator} Day {day_data['day']} - {day_data.get('location', 'Location TBD')} | £{day_cost:.2f}", 
                        expanded=i == len(st.session_state.trip_data) - 1):
            
            # Enhanced date and location section
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("📅 Date", key=f"date_{i}", value=pd.to_datetime(day_data.get('date')) if day_data.get('date') else None)
            with col2:
                location = st.text_input(
                    "📍 Location/City", 
                    key=f"location_{i}", 
                    value=day_data.get('location', ''),
                    placeholder="e.g., Paris, Bangkok, Edinburgh"
                )
            
            # Enhanced transport and accommodation sections
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="transport-section">', unsafe_allow_html=True)
                st.markdown("#### 🚌 Transportation")
                
                transport_type = st.selectbox(
                    "Transport Type", 
                    ["Bus", "Bus (overnight)", "Train", "Train (overnight)", "Plane", 
                     "Ferry", "Car/Taxi", "Walking", "Local Transport", "Cycling"],
                    key=f"transport_type_{i}",
                    index=get_transport_index(day_data.get('transport_type', 'Bus'))
                )
                
                col_from, col_to = st.columns(2)
                with col_from:
                    transport_from = st.text_input(
                        "From", 
                        key=f"transport_from_{i}", 
                        value=day_data.get('transport_from', ''),
                        placeholder="Departure"
                    )
                with col_to:
                    transport_to = st.text_input(
                        "To", 
                        key=f"transport_to_{i}", 
                        value=day_data.get('transport_to', ''),
                        placeholder="Arrival"
                    )
                
                col_time, col_cost = st.columns(2)
                with col_time:
                    transport_time = st.text_input(
                        "⏰ Time", 
                        key=f"transport_time_{i}", 
                        value=day_data.get('transport_time', ''),
                        placeholder="09:30"
                    )
                with col_cost:
                    transport_cost = st.number_input(
                        "💰 Cost (£)", 
                        key=f"transport_cost_{i}", 
                        value=float(day_data.get('transport_cost', 0.0)), 
                        min_value=0.0, 
                        step=1.0
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col2:
                st.markdown('<div class="accommodation-section">', unsafe_allow_html=True)
                st.markdown("#### 🏨 Accommodation")
                
                accommodation_type = st.selectbox(
                    "Accommodation Type",
                    ["Hostel", "Hotel", "Guesthouse", "Camping", "Bus (sleeping)", "Train (sleeping)", 
                     "Airbnb", "Couchsurfing", "Friend's place", "None (transit day)"],
                    key=f"accommodation_type_{i}",
                    index=get_accommodation_index(day_data.get('accommodation_type', 'Hostel'))
                )
                
                if accommodation_type in ["Bus (sleeping)", "Train (sleeping)"]:
                    st.success("💤 Sleeping on transport - saving money!")
                    accommodation_name = ""
                    accommodation_cost = 0.0
                elif accommodation_type == "None (transit day)":
                    st.info("🚶 Transit day - no accommodation needed")
                    accommodation_name = ""
                    accommodation_cost = 0.0
                else:
                    accommodation_name = st.text_input(
                        "🏠 Name/Location", 
                        key=f"accommodation_name_{i}", 
                        value=day_data.get('accommodation_name', ''),
                        placeholder="Hotel/Hostel name"
                    )
                    accommodation_cost = st.number_input(
                        "💰 Cost (£)", 
                        key=f"accommodation_cost_{i}", 
                        value=float(day_data.get('accommodation_cost', 0.0)), 
                        min_value=0.0, 
                        step=1.0
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Enhanced notes section
            notes = st.text_area(
                "📝 Notes & Activities", 
                key=f"notes_{i}", 
                value=day_data.get('notes', ''),
                placeholder="Things to do, places to visit, important info...",
                height=100
            )
            
            # Enhanced action buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            with col1:
                if st.button(f"🗑️ Delete", key=f"delete_{i}", type="secondary"):
                    delete_day(i)
            with col2:
                if st.button(f"📋 Copy", key=f"copy_{i}"):
                    copy_day(i)
            with col3:
                if i > 0 and st.button(f"⬆️ Move Up", key=f"move_up_{i}"):
                    move_day_up(i)
            with col4:
                completion_percentage = calculate_day_completion(day_data)
                st.progress(completion_percentage, text=f"Completion: {completion_percentage:.0%}")
            
            # Update session state
            update_day_data(i, {
                'date': str(date) if date else '',
                'location': location,
                'transport_type': transport_type,
                'transport_from': transport_from,
                'transport_to': transport_to,
                'transport_time': transport_time,
                'transport_cost': transport_cost,
                'accommodation_type': accommodation_type,
                'accommodation_name': accommodation_name,
                'accommodation_cost': accommodation_cost,
                'notes': notes
            })

def budget_calculator():
    """Enhanced budget calculator with visual insights"""
    st.markdown('<h2 class="section-header">💰 Budget Calculator</h2>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 4rem 2rem;">
            <h3>💰 Ready to crunch the numbers?</h3>
            <p style="font-size: 1.1rem;">Add your itinerary first, then come back here to see your budget breakdown!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Calculate base costs
    total_transport = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
    total_accommodation = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
    
    # Enhanced budget categories
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💳 Additional Budget Categories")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🍽️ Daily Expenses**")
        food_budget = st.number_input("Food & Drink (£)", min_value=0.0, value=st.session_state.budget_data.get('food_budget', 0.0), step=5.0)
        activities_budget = st.number_input("Activities & Attractions (£)", min_value=0.0, value=st.session_state.budget_data.get('activities_budget', 0.0), step=5.0)
        
    with col2:
        st.markdown("**🛍️ Shopping & Extras**")
        shopping_budget = st.number_input("Shopping & Souvenirs (£)", min_value=0.0, value=st.session_state.budget_data.get('shopping_budget', 0.0), step=5.0)
        misc_costs = st.number_input("Miscellaneous (£)", min_value=0.0, value=st.session_state.budget_data.get('misc_costs', 0.0), step=5.0)
    
    with col3:
        st.markdown("**🛡️ Safety & Security**")
        emergency_budget = st.number_input("Emergency Fund (£)", min_value=0.0, value=st.session_state.budget_data.get('emergency_budget', 0.0), step=10.0)
        insurance_cost = st.number_input("Travel Insurance (£)", min_value=0.0, value=st.session_state.budget_data.get('insurance_cost', 0.0), step=5.0)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Save additional budget data
    st.session_state.budget_data.update({
        'food_budget': food_budget,
        'activities_budget': activities_budget,
        'shopping_budget': shopping_budget,
        'misc_costs': misc_costs,
        'emergency_budget': emergency_budget,
        'insurance_cost': insurance_cost
    })
    
    # Calculate totals
    additional_costs = food_budget + activities_budget + shopping_budget + emergency_budget + insurance_cost + misc_costs
    total_planned = total_transport + total_accommodation + additional_costs
    total_budget = st.session_state.budget_data['total_budget']
    remaining = total_budget - total_planned
    
    # Enhanced budget overview
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Budget Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("💰 Total Budget", f"£{total_budget:,.0f}")
    with col2:
        st.metric("📝 Planned", f"£{total_planned:,.0f}")
    with col3:
        st.metric("💸 Remaining", f"£{remaining:,.0f}")
    with col4:
        percentage = (total_planned / total_budget * 100) if total_budget > 0 else 0
        st.metric("📈 Used", f"{percentage:.1f}%")
    with col5:
        daily_avg = total_planned / len(st.session_state.trip_data) if st.session_state.trip_data else 0
        st.metric("📅 Daily Avg", f"£{daily_avg:.0f}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Budget status with enhanced feedback
    if remaining < 0:
        st.error(f"💸 You're over budget by £{abs(remaining):,.0f}! Consider adjusting your plans.")
    elif remaining < total_budget * 0.1:
        st.warning("🔶 You're cutting it close with your budget! Consider adding a buffer.")
    else:
        st.success("✅ Great! You're well within budget!")
    
    # Enhanced visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        if total_planned > 0:
            budget_breakdown = {
                'Transport': total_transport,
                'Accommodation': total_accommodation,
                'Food & Drink': food_budget,
                'Activities': activities_budget,
                'Shopping': shopping_budget,
                'Emergency': emergency_budget,
                'Insurance': insurance_cost,
                'Miscellaneous': misc_costs
            }
            
            budget_breakdown = {k: v for k, v in budget_breakdown.items() if v > 0}
            
            if budget_breakdown:
                fig = px.pie(
                    values=list(budget_breakdown.values()),
                    names=list(budget_breakdown.keys()),
                    title="💰 Budget Breakdown",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(
                    font=dict(family="Inter, sans-serif"),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if st.session_state.trip_data:
            df = pd.DataFrame(st.session_state.trip_data)
            df['total_daily_cost'] = df['transport_cost'].astype(float) + df['accommodation_cost'].astype(float)
            
            fig = px.bar(
                df, 
                x='day', 
                y='total_daily_cost',
                title="📈 Daily Expenses",
                labels={'day': 'Day', 'total_daily_cost': 'Cost (£)'},
                color='total_daily_cost',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                font=dict(family="Inter, sans-serif"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

def analytics_dashboard():
    """New analytics dashboard for trip insights"""
    st.markdown('<h2 class="section-header">📊 Trip Analytics</h2>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 4rem 2rem;">
            <h3>📊 No data to analyze yet!</h3>
            <p style="font-size: 1.1rem;">Add your trip details first to see amazing insights!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Trip completion analysis
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Trip Completion Status")
    
    completed_days = sum(1 for day in st.session_state.trip_data if calculate_day_completion(day) >= 0.8)
    total_days = len(st.session_state.trip_data)
    completion_rate = completed_days / total_days if total_days > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏁 Completed Days", f"{completed_days}/{total_days}")
    with col2:
        st.metric("📈 Completion Rate", f"{completion_rate:.1%}")
    with col3:
        missing_locations = sum(1 for day in st.session_state.trip_data if not day.get('location'))
        st.metric("📍 Missing Locations", missing_locations)
    with col4:
        missing_transport = sum(1 for day in st.session_state.trip_data if not day.get('transport_from'))
        st.metric("🚌 Missing Transport", missing_transport)
    
    # Progress bar
    st.progress(completion_rate, text=f"Overall Trip Planning: {completion_rate:.1%}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Transport and accommodation analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🚌 Transport Analysis")
        
        transport_stats = {}
        for day in st.session_state.trip_data:
            transport = day.get('transport_type', 'Unknown')
            transport_stats[transport] = transport_stats.get(transport, 0) + 1
        
        if transport_stats:
            fig = px.bar(
                x=list(transport_stats.keys()),
                y=list(transport_stats.values()),
                title="Transport Usage",
                labels={'x': 'Transport Type', 'y': 'Number of Days'},
                color=list(transport_stats.values()),
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                font=dict(family="Inter, sans-serif"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏨 Accommodation Analysis")
        
        accommodation_stats = {}
        for day in st.session_state.trip_data:
            accommodation = day.get('accommodation_type', 'Unknown')
            accommodation_stats[accommodation] = accommodation_stats.get(accommodation, 0) + 1
        
        if accommodation_stats:
            fig = px.pie(
                values=list(accommodation_stats.values()),
                names=list(accommodation_stats.keys()),
                title="Accommodation Distribution",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                font=dict(family="Inter, sans-serif"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Cost trend analysis
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💰 Cost Trend Analysis")
    
    df = pd.DataFrame(st.session_state.trip_data)
    if not df.empty:
        df['total_cost'] = df['transport_cost'].astype(float) + df['accommodation_cost'].astype(float)
        df['cumulative_cost'] = df['total_cost'].cumsum()
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Daily Costs', 'Cumulative Spending'),
            vertical_spacing=0.1
        )
        
        # Daily costs
        fig.add_trace(
            go.Scatter(x=df['day'], y=df['total_cost'], mode='lines+markers', 
                      name='Daily Cost', line=dict(color='#667eea', width=3)),
            row=1, col=1
        )
        
        # Cumulative costs
        fig.add_trace(
            go.Scatter(x=df['day'], y=df['cumulative_cost'], mode='lines+markers',
                      name='Cumulative Cost', line=dict(color='#f5576c', width=3)),
            row=2, col=1
        )
        
        fig.update_layout(
            height=500,
            font=dict(family="Inter, sans-serif"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Day", row=2, col=1)
        fig.update_yaxes(title_text="Cost (£)", row=1, col=1)
        fig.update_yaxes(title_text="Cumulative Cost (£)", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def trip_summary():
    """Enhanced trip summary with better presentation"""
    st.markdown('<h2 class="section-header">📋 Trip Summary</h2>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 4rem 2rem;">
            <h3>📋 No trip data yet!</h3>
            <p style="font-size: 1.1rem;">Start planning in the Day-by-Day section, then come back for your summary!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Enhanced trip header
    trip_name = st.session_state.trip_info.get('name', 'My Adventure')
    start_date = st.session_state.trip_info.get('start_date')
    end_date = st.session_state.trip_info.get('end_date')
    
    st.markdown(f"""
    <div style="background: var(--primary-gradient); 
                color: white; padding: 3rem 2rem; border-radius: var(--radius-xl); 
                text-align: center; margin-bottom: 2rem; box-shadow: var(--shadow-xl);">
        <h1 style="margin: 0; font-family: 'Space Grotesk', sans-serif; font-size: 3rem;">🎒 {trip_name}</h1>
        <p style="margin: 1rem 0 0 0; opacity: 0.95; font-size: 1.3rem;">Your amazing adventure awaits!</p>
        {f'<p style="margin: 0.5rem 0 0 0; opacity: 0.8;">{start_date} → {end_date}</p>' if start_date and end_date else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced statistics
    show_enhanced_stats()
    
    # Detailed itinerary with enhanced presentation
    st.subheader("🗓️ Your Detailed Itinerary")
    
    for i, day in enumerate(st.session_state.trip_data):
        day_cost = day.get('transport_cost', 0.0) + day.get('accommodation_cost', 0.0)
        
        # Enhanced day card
        st.markdown(f"""
        <div class="card" style="margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin: 0; color: var(--primary);">📍 Day {day['day']} - {day.get('location', 'TBD')}</h3>
                <span style="background: var(--primary-gradient); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">£{day_cost:.2f}</span>
            </div>
        """, unsafe_allow_html=True)
        
        if day.get('date'):
            st.markdown(f"**📅 Date:** {day['date']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🚌 Transportation:**")
            if day.get('transport_from') and day.get('transport_to'):
                st.write(f"• **Route:** {day['transport_from']} → {day['transport_to']}")
                st.write(f"• **Mode:** {day.get('transport_type', 'TBD')}")
                if day.get('transport_time'):
                    st.write(f"• **Departure:** {day['transport_time']}")
                st.write(f"• **Cost:** £{day.get('transport_cost', 0):.2f}")
            else:
                st.write("• Transport details to be added")
                
        with col2:
            st.markdown("**🏨 Accommodation:**")
            acc_type = day.get('accommodation_type', 'TBD')
            if acc_type in ["Bus (sleeping)", "Train (sleeping)"]:
                st.write(f"• **Sleeping on:** {acc_type}")
                st.write("• **Cost:** Included in transport")
            elif acc_type == "None (transit day)":
                st.write("• **Transit day** - on the move!")
            elif day.get('accommodation_name'):
                st.write(f"• **Type:** {acc_type}")
                st.write(f"• **Place:** {day['accommodation_name']}")
                st.write(f"• **Cost:** £{day.get('accommodation_cost', 0):.2f}")
            else:
                st.write("• Accommodation to be booked")
        
        if day.get('notes'):
            st.markdown(f"**📝 Plans & Notes:** {day['notes']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced export functionality
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📤 Share Your Adventure")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📁 Download CSV", type="primary", use_container_width=True):
            df = pd.DataFrame(st.session_state.trip_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="💾 Download Trip Data",
                data=csv,
                file_name=f"{trip_name.replace(' ', '_')}_adventure.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col2:
        if st.button("📋 Generate Text Summary", use_container_width=True):
            itinerary_text = generate_enhanced_text_itinerary()
            st.text_area("Copy this itinerary:", value=itinerary_text, height=200)
            st.success("✅ Perfect for sharing or keeping as backup!")
    
    with col3:
        if st.button("📊 Detailed Stats", use_container_width=True):
            show_detailed_statistics()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Helper functions
def add_new_day():
    """Add a new day with enhanced defaults"""
    new_day = {
        'day': len(st.session_state.trip_data) + 1,
        'date': '',
        'location': '',
        'transport_type': 'Bus',
        'transport_from': '',
        'transport_to': '',
        'transport_time': '',
        'transport_cost': 0.0,
        'accommodation_type': 'Hostel',
        'accommodation_name': '',
        'accommodation_cost': 0.0,
        'notes': ''
    }
    st.session_state.trip_data.append(new_day)
    st.rerun()

def delete_day(index):
    """Delete a day and renumber"""
    st.session_state.trip_data.pop(index)
    for j, remaining_day in enumerate(st.session_state.trip_data):
        remaining_day['day'] = j + 1
    st.rerun()

def copy_day(index):
    """Copy a day with incremented day number"""
    original_day = st.session_state.trip_data[index].copy()
    original_day['day'] = len(st.session_state.trip_data) + 1
    original_day['date'] = ''
    st.session_state.trip_data.append(original_day)
    st.rerun()

def move_day_up(index):
    """Move day up in the list"""
    if index > 0:
        st.session_state.trip_data[index], st.session_state.trip_data[index-1] = \
            st.session_state.trip_data[index-1], st.session_state.trip_data[index]
        # Renumber days
        for j, day in enumerate(st.session_state.trip_data):
            day['day'] = j + 1
        st.rerun()

def calculate_day_completion(day_data):
    """Calculate completion percentage for a day"""
    required_fields = ['location', 'transport_from', 'transport_to', 'accommodation_type']
    completed_fields = sum(1 for field in required_fields if day_data.get(field))
    return completed_fields / len(required_fields)

def update_day_data(index, data):
    """Update day data in session state"""
    st.session_state.trip_data[index].update(data)

def get_transport_index(transport_type):
    """Get index for transport type selectbox"""
    transport_types = ["Bus", "Bus (overnight)", "Train", "Train (overnight)", "Plane", 
                      "Ferry", "Car/Taxi", "Walking", "Local Transport", "Cycling"]
    try:
        return transport_types.index(transport_type)
    except ValueError:
        return 0

def get_accommodation_index(accommodation_type):
    """Get index for accommodation type selectbox"""
    accommodation_types = ["Hostel", "Hotel", "Guesthouse", "Camping", "Bus (sleeping)", "Train (sleeping)", 
                          "Airbnb", "Couchsurfing", "Friend's place", "None (transit day)"]
    try:
        return accommodation_types.index(accommodation_type)
    except ValueError:
        return 0

def generate_enhanced_text_itinerary():
    """Generate an enhanced text version of the itinerary"""
    trip_name = st.session_state.trip_info.get('name', 'My Adventure')
    start_date = st.session_state.trip_info.get('start_date', '')
    end_date = st.session_state.trip_info.get('end_date', '')
    
    text = f"🎒 {trip_name}\n{'='*len(trip_name)+4}\n"
    if start_date and end_date:
        text += f"📅 {start_date} → {end_date}\n"
    text += f"🌍 {len(st.session_state.trip_data)} days of adventure\n\n"
    
    total_cost = 0
    for day in st.session_state.trip_data:
        day_cost = day.get('transport_cost', 0) + day.get('accommodation_cost', 0)
        total_cost += day_cost
        
        text += f"📍 Day {day['day']} - {day.get('location', 'TBD')}\n"
        text += f"📅 Date: {day.get('date', 'TBD')}\n"
        text += f"🚌 Transport: {day.get('transport_type', 'TBD')} from {day.get('transport_from', 'TBD')} to {day.get('transport_to', 'TBD')}\n"
        
        if day.get('transport_time'):
            text += f"⏰ Departure: {day['transport_time']}\n"
            
        text += f"🏨 Accommodation: {day.get('accommodation_type', 'TBD')}"
        if day.get('accommodation_name'):
            text += f" - {day['accommodation_name']}"
        text += "\n"
        
        if day.get('notes'):
            text += f"📝 Notes: {day['notes']}\n"
        text += f"💰 Daily Cost: £{day_cost:.2f}\n"
        text += "-" * 50 + "\n\n"
    
    text += f"💰 Total Trip Cost: £{total_cost:.2f}\n"
    text += f"🎒 Total Days: {len(st.session_state.trip_data)}\n"
    text += f"📊 Average Daily Cost: £{total_cost/len(st.session_state.trip_data):.2f}\n\n"
    text += "🌟 Have an amazing adventure! Safe travels! 🎒"
    
    return text

def show_detailed_statistics():
    """Show enhanced detailed trip statistics"""
    if not st.session_state.trip_data:
        return
    
    st.subheader("📊 Your Adventure Statistics")
    
    # Transport statistics
    transport_counts = {}
    transport_costs = {}
    for day in st.session_state.trip_data:
        transport = day.get('transport_type', 'Unknown')
        transport_counts[transport] = transport_counts.get(transport, 0) + 1
        transport_costs[transport] = transport_costs.get(transport, 0) + day.get('transport_cost', 0)
    
    # Accommodation statistics
    accommodation_counts = {}
    accommodation_costs = {}
    for day in st.session_state.trip_data:
        accommodation = day.get('accommodation_type', 'Unknown')
        accommodation_counts[accommodation] = accommodation_counts.get(accommodation, 0) + 1
        accommodation_costs[accommodation] = accommodation_costs.get(accommodation, 0) + day.get('accommodation_cost', 0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚌 Transportation Breakdown:**")
        for transport, count in transport_counts.items():
            cost = transport_costs.get(transport, 0)
            emoji = "🚌" if "Bus" in transport else "🚂" if "Train" in transport else "🚶" if transport == "Walking" else "🚗"
            st.write(f"{emoji} {transport}: {count} journey{'s' if count != 1 else ''} (£{cost:.2f})")
    
    with col2:
        st.markdown("**🏨 Accommodation Breakdown:**")
        for accommodation, count in accommodation_counts.items():
            cost = accommodation_costs.get(accommodation, 0)
            emoji = "🏨" if "Hotel" in accommodation else "🏠" if "Hostel" in accommodation else "⛺" if accommodation == "Camping" else "🛏️"
            st.write(f"{emoji} {accommodation}: {count} night{'s' if count != 1 else ''} (£{cost:.2f})")
    
    # Enhanced cost analysis
    st.markdown("**💰 Detailed Cost Analysis:**")
    total_transport = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
    total_accommodation = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
    total_cost = total_transport + total_accommodation
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🚌 Total Transport", f"£{total_transport:.2f}")
    with col2:
        st.metric("🏨 Total Accommodation", f"£{total_accommodation:.2f}")
    with col3:
        avg_daily = total_cost / len(st.session_state.trip_data) if st.session_state.trip_data else 0
        st.metric("📊 Avg Daily Cost", f"£{avg_daily:.2f}")
    with col4:
        budget_used = (total_cost / st.session_state.budget_data['total_budget'] * 100) if st.session_state.budget_data['total_budget'] > 0 else 0
        st.metric("📈 Budget Used", f"{budget_used:.1f}%")

if __name__ == "__main__":
    main()
