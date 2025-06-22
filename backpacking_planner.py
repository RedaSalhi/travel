# Helper functions with modern adaptations
def add_new_day():
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
    st.session_state.trip_data.pop(index)
    # Renumber remaining days
    for j, remaining_day in enumerate(st.session_state.trip_data):
        remaining_day['day'] = j + 1
    st.rerun()

def copy_day(index):
    original_day = st.session_state.trip_data[index].copy()
    original_day['day'] = len(st.session_state.trip_data) + 1
    original_day['date'] = ''  # Clear date for new day
    st.session_state.trip_data.append(original_day)
    st.rerun()

def update_day_data(index, data):
    st.session_state.trip_data[index].update(data)

def get_transport_index(transport_type):
    transport_types = ["Bus", "Bus (overnight)", "Train", "Train (overnight)", "Plane", 
                      "Ferry", "Car/Taxi", "Walking", "Local Transport", "Cycling"]
    try:
        return transport_types.index(transport_type)
    except ValueError:
        return 0

def get_accommodation_index(accommodation_type):
    accommodation_types = ["Hostel", "Hotel", "Guesthouse", "Camping", "Bus (sleeping)", "Train (sleeping)", 
                          "Airbnb", "Couchsurfing", "Friend's place", "None (transit day)"]
    try:
        return accommodation_types.index(accommodation_type)
    except ValueError:
        return 0

def generate_text_itinerary():
    trip_name = st.session_state.trip_info.get('name', 'My Adventure')
    text = f"🎒 {trip_name}\n{'='*len(trip_name)+4}\n\n"
    
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
        text += "-" * 40 + "\n\n"
    
    text += f"💰 Total Trip Cost: £{total_cost:.2f}\n"
    text += f"🎒 Total Days: {len(st.session_state.trip_data)}\n"
    text += f"📊 Average Daily Cost: £{total_cost/len(st.session_state.trip_data):.2f}\n\n"
    text += "🌟 Have an amazing trip! Safe travels! 🎒"
    
    return text

def show_trip_statistics():
    st.subheader("📊 Your Adventure Statistics")
    
    if not st.session_state.trip_data:
        return
    
    # Transport statistics
    transport_counts = {}
    for day in st.session_state.trip_data:
        transport = day.get('transport_type', 'Unknown')
        transportimport streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Backpacking Trip Planner",
    page_icon="🎒",
    layout="wide"
)

# CSS styling with enhanced modern design
def load_css():
    st.markdown("""
    <style>
    /* Import sophisticated Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Global Variables */
    :root {
        --primary-blue: #2563eb;
        --primary-red: #dc2626;
        --dark-blue: #1e40af;
        --light-blue: #dbeafe;
        --gray-50: #f8fafc;
        --gray-100: #f1f5f9;
        --gray-200: #e2e8f0;
        --gray-300: #cbd5e1;
        --gray-600: #475569;
        --gray-800: #1e293b;
        --gray-900: #0f172a;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --border-radius: 12px;
        --border-radius-lg: 16px;
    }
    
    /* Main app styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        background: linear-gradient(135deg, var(--gray-50) 0%, #ffffff 100%);
    }
    
    /* Enhanced header styling */
    .main-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--dark-blue) 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: var(--border-radius-lg);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.05) 100%);
        pointer-events: none;
    }
    
    .main-header h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 400;
        margin: 1rem 0 0 0;
        opacity: 0.95;
        letter-spacing: 0.025em;
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--gray-900) 0%, var(--gray-800) 100%);
        border-right: 1px solid var(--gray-300);
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern section headers */
    .section-header {
        background: linear-gradient(135deg, #ffffff 0%, var(--gray-100) 100%);
        color: var(--gray-800);
        padding: 1.5rem 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        margin: 2rem 0 1.5rem 0;
        border: 2px solid var(--gray-200);
        box-shadow: var(--shadow-md);
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-blue), var(--primary-red));
        border-radius: 2px;
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, var(--gray-50) 100%);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border: 1px solid var(--gray-200);
        box-shadow: var(--shadow-md);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--primary-blue), var(--primary-red));
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Enhanced expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #ffffff 0%, var(--gray-50) 100%);
        border: 1px solid var(--gray-200);
        border-radius: var(--border-radius) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--primary-blue);
    }
    
    /* Modern button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-red) 0%, #b91c1c 100%);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
        letter-spacing: 0.025em;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #b91c1c 0%, #991b1b 100%);
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-sm);
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--dark-blue) 100%);
        box-shadow: var(--shadow-md);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--dark-blue) 0%, #1e40af 100%);
        box-shadow: var(--shadow-xl);
    }
    
    /* Enhanced input field styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input {
        border: 2px solid var(--gray-200);
        border-radius: var(--border-radius);
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        background: #ffffff;
        box-shadow: var(--shadow-sm);
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1), var(--shadow-md);
        outline: none;
    }
    
    /* Enhanced section styling */
    .transport-section {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border: 1px solid #0ea5e9;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-sm);
        position: relative;
    }
    
    .transport-section::before {
        content: '🚌';
        position: absolute;
        top: -10px;
        left: 20px;
        background: white;
        padding: 0 8px;
        font-size: 1.2rem;
    }
    
    .accommodation-section {
        background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border: 1px solid #ec4899;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-sm);
        position: relative;
    }
    
    .accommodation-section::before {
        content: '🏨';
        position: absolute;
        top: -10px;
        left: 20px;
        background: white;
        padding: 0 8px;
        font-size: 1.2rem;
    }
    
    /* Enhanced alert styling */
    .stSuccess {
        background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        border: none;
    }
    
    .stWarning {
        background: linear-gradient(135deg, var(--warning) 0%, #d97706 100%);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        border: none;
    }
    
    .stError {
        background: linear-gradient(135deg, var(--error) 0%, #dc2626 100%);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        border: none;
    }
    
    .stInfo {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--dark-blue) 100%);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        border: none;
    }
    
    /* Modern footer styling */
    .footer {
        background: linear-gradient(135deg, var(--gray-800) 0%, var(--gray-900) 100%);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: var(--border-radius);
        margin-top: 3rem;
        font-family: 'Inter', sans-serif;
        box-shadow: var(--shadow-lg);
    }
    
    /* Enhanced scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--gray-100);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary-blue) 0%, var(--primary-red) 100%);
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--dark-blue) 0%, #b91c1c 100%);
    }
    
    /* Typography improvements */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--gray-800) !important;
        font-weight: 600 !important;
        letter-spacing: -0.025em !important;
    }
    
    p, div, span, label {
        font-family: 'Inter', sans-serif !important;
        color: var(--gray-600) !important;
        line-height: 1.6 !important;
    }
    
    /* Enhanced chart styling */
    .js-plotly-plot {
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        border: 1px solid var(--gray-200);
        background: white;
    }
    
    /* Modern divider */
    .modern-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--primary-blue) 50%, transparent 100%);
        margin: 2rem 0;
        border-radius: 1px;
    }
    
    /* Card container styling */
    .card-container {
        background: white;
        border-radius: var(--border-radius);
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--gray-200);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .card-container:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-1px);
    }
    
    /* Stats container */
    .stats-container {
        background: linear-gradient(135deg, var(--gray-50) 0%, white 100%);
        padding: 2rem;
        border-radius: var(--border-radius);
        border: 1px solid var(--gray-200);
        box-shadow: var(--shadow-md);
        margin: 1rem 0;
    }
    
    /* Improved sidebar stats */
    .sidebar-stats {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2.5rem;
        }
        
        .main-header p {
            font-size: 1.1rem;
        }
        
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .section-header {
            padding: 1rem;
        }
        
        .transport-section,
        .accommodation-section {
            padding: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            padding: 2rem 1rem;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .card-container {
            padding: 1rem;
        }
    }
    
    /* Loading animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main .block-container > div {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Focus indicators for accessibility */
    *:focus-visible {
        outline: 2px solid var(--primary-blue) !important;
        outline-offset: 2px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'trip_data' not in st.session_state:
    st.session_state.trip_data = []
if 'budget_data' not in st.session_state:
    st.session_state.budget_data = {
        'total_budget': 500.0,  # UK-appropriate starting budget
        'spent': 0.0,
        'categories': {}
    }
if 'trip_info' not in st.session_state:
    st.session_state.trip_info = {
        'name': '',
        'start_date': None,
        'end_date': None,
        'destinations': ''
    }

def main():
    # Load CSS
    load_css()
    
    # Custom header with modern design
    st.markdown("""
    <div class="main-header">
        <h1>🎒 Backpacking Trip Planner</h1>
        <p>Plan your perfect adventure - from local escapes to epic journeys!</p>
    </div>
    <div class="modern-divider"></div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.markdown("""
    <div class="sidebar-stats">
        <h2 style="color: white; text-align: center; margin: 0; font-size: 1.5rem;">🧭 Navigation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox("Choose your section:", 
                                ["🌍 Trip Overview", "📅 Day-by-Day Planning", "💰 Budget Calculator", "📋 Trip Summary"])
    
    # Quick stats in sidebar with modern styling
    if st.session_state.trip_data:
        st.sidebar.markdown("""
        <div class="sidebar-stats">
            <h3 style="color: white; text-align: center; margin-bottom: 1rem; font-size: 1.25rem;">📊 Trip Stats</h3>
        </div>
        """, unsafe_allow_html=True)
        
        total_days = len(st.session_state.trip_data)
        total_cost = sum(day.get('transport_cost', 0.0) + day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
        
        st.sidebar.markdown(f"""
        <div style="color: white; text-align: center; font-family: 'Inter', sans-serif;">
            <p><strong>Days Planned:</strong> {total_days}</p>
            <p><strong>Total Cost:</strong> £{total_cost:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        budget = st.session_state.budget_data['total_budget']
        remaining = budget - total_cost
        percentage_left = (remaining/budget)*100 if budget > 0 else 0
        
        st.sidebar.markdown(f"""
        <div style="color: white; text-align: center; font-family: 'Inter', sans-serif;">
            <p><strong>Budget Remaining:</strong> £{remaining:.2f}</p>
            <p><strong>Budget Left:</strong> {percentage_left:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add inspirational travel quote
    st.sidebar.markdown("""
    <div class="sidebar-stats">
        <p style="color: white; font-style: italic; text-align: center; margin: 0; font-family: 'Inter', sans-serif;">
            "Adventure awaits those who plan well"<br>
            <small>- Happy travels! 🌟</small>
        </p>
    </div>
    """, unsafe_allow_html=True);">🧭 Navigation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    
    if page == "🌍 Trip Overview":
        trip_overview()
    elif page == "📅 Day-by-Day Planning":
        day_by_day_planning()
    elif page == "💰 Budget Calculator":
        budget_calculator()
    elif page == "📋 Trip Summary":
        trip_summary()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🎒 Made with ❤️ for adventurers everywhere | Safe travels! 🌟</p>
    </div>
    """, unsafe_allow_html=True)

def trip_overview():
    st.markdown('<div class="section-header"><h2>🏴󠁧󠁢󠁥󠁮󠁧󠁿 Trip Overview</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        trip_name = st.text_input("Trip Name", 
                                 value=st.session_state.trip_info['name'],
                                 placeholder="e.g., Scottish Highlands & Lake District Adventure")
        start_date = st.date_input("Start Date", 
                                  value=st.session_state.trip_info['start_date'])
        end_date = st.date_input("End Date", 
                                value=st.session_state.trip_info['end_date'])
        
    with col2:
        destinations = st.text_area("Main Destinations", 
                                   value=st.session_state.trip_info['destinations'],
                                   placeholder="Edinburgh, Glasgow, Lake District, Cornwall, London...")
        total_budget = st.number_input("Total Budget (£)", 
                                      min_value=0.0, 
                                      value=st.session_state.budget_data['total_budget'],
                                      step=50.0,
                                      help="Average UK backpacking: £30-60 per day")
    
    # Travel style preferences with UK focus
    st.subheader("🎯 Travel Preferences")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        travel_style = st.selectbox("Travel Style", 
                                   ["Budget Backpacker (£25-40/day)", 
                                    "Mid-range Explorer (£40-70/day)", 
                                    "Comfort Traveller (£70+/day)"])
    with col2:
        group_size = st.number_input("Group Size", min_value=1, max_value=20, value=1)
    with col3:
        transport_preference = st.selectbox("Preferred Transport", 
                                          ["National Express Bus", "Train (Off-peak)", 
                                           "Mix of Bus & Train", "Megabus Budget", "Car Hire"])
    
    # UK-specific travel tips
    st.info("💡 **Top UK Travel Tips:** Book buses in advance for £1-5 fares, get a 16-25 Railcard for 1/3 off trains, stay in YHA hostels, and always pack a brolly! ☔")
    
    if st.button("💾 Save Trip Overview", type="primary"):
        st.session_state.trip_info.update({
            'name': trip_name,
            'start_date': start_date,
            'end_date': end_date,
            'destinations': destinations
        })
        st.session_state.budget_data['total_budget'] = total_budget
        st.success("✅ Trip overview saved! Ready to plan your British adventure!")
        
        # Auto-suggest days based on date range
        if start_date and end_date and end_date > start_date:
            suggested_days = (end_date - start_date).days
            if suggested_days > len(st.session_state.trip_data):
                st.info(f"📅 Based on your dates, you might want to plan {suggested_days} days. Head to Day-by-Day Planning to add more days!")

def day_by_day_planning():
    st.markdown('<div class="section-header"><h2>🚌 Day-by-Day Planning</h2></div>', unsafe_allow_html=True)
    
    # Quick add multiple days
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        if st.button("➕ Add New Day", type="primary"):
            add_new_day()
    with col2:
        days_to_add = st.number_input("Add Multiple Days", min_value=1, max_value=30, value=1)
    with col3:
        if st.button(f"Add {days_to_add} Days"):
            for _ in range(days_to_add):
                add_new_day()
            st.rerun()
    
    if not st.session_state.trip_data:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; margin: 2rem 0;">
            <h3>🎒 Ready to start your British adventure?</h3>
            <p>Click "Add New Day" above to begin planning your journey through Britain!</p>
            <p><small>💡 Tip: Plan transport between cities first, then add local accommodation</small></p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display existing days with UK styling
    for i, day_data in enumerate(st.session_state.trip_data):
        day_cost = day_data.get('transport_cost', 0.0) + day_data.get('accommodation_cost', 0.0)
        
        with st.expander(f"📍 Day {day_data['day']} - {day_data.get('location', 'Location TBD')} | £{day_cost:.2f}", 
                        expanded=i == len(st.session_state.trip_data) - 1):
            
            # Date and location
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Date", key=f"date_{i}", 
                                   help="When will you be in this location?")
            with col2:
                location = st.text_input("Location/City", key=f"location_{i}", 
                                       value=day_data.get('location', ''),
                                       placeholder="e.g., Edinburgh, Cornwall, Lake District")
            
            # Transport and accommodation sections with UK styling
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="transport-section">', unsafe_allow_html=True)
                st.markdown("### 🚌 Transport")
                
                # UK-specific transport options
                transport_type = st.selectbox(
                    "Transport Type", 
                    ["National Express Bus", "Megabus", "Train", "Sleeper Train", 
                     "Local Bus", "Underground/Tube", "Ferry", "Car", "Walking", "Cycling"],
                    key=f"transport_type_{i}",
                    index=get_uk_transport_index(day_data.get('transport_type', 'National Express Bus'))
                )
                
                transport_from = st.text_input("From", key=f"transport_from_{i}", 
                                             value=day_data.get('transport_from', ''),
                                             placeholder="Manchester, London Victoria...")
                transport_to = st.text_input("To", key=f"transport_to_{i}", 
                                           value=day_data.get('transport_to', ''),
                                           placeholder="Edinburgh, Brighton...")
                
                col_time, col_cost = st.columns(2)
                with col_time:
                    transport_time = st.text_input("Time", key=f"transport_time_{i}", 
                                                 value=day_data.get('transport_time', ''),
                                                 placeholder="09:30")
                with col_cost:
                    transport_cost = st.number_input("Cost (£)", key=f"transport_cost_{i}", 
                                                   value=float(day_data.get('transport_cost', 0.0)), 
                                                   min_value=0.0, step=1.0,
                                                   help="Megabus: £1-15, Trains: £15-100+")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col2:
                st.markdown('<div class="accommodation-section">', unsafe_allow_html=True)
                st.markdown("### 🏨 Accommodation")
                
                # UK-specific accommodation options
                accommodation_type = st.selectbox(
                    "Accommodation Type",
                    ["YHA Hostel", "Independent Hostel", "Premier Inn", "Travelodge", 
                     "B&B", "Pub with Rooms", "Camping", "Sleeper Train", "Night Bus", 
                     "University Halls", "Airbnb", "Friend's Sofa", "None (transit day)"],
                    key=f"accommodation_type_{i}",
                    index=get_uk_accommodation_index(day_data.get('accommodation_type', 'YHA Hostel'))
                )
                
                # Show different inputs based on accommodation type
                if accommodation_type in ["Sleeper Train", "Night Bus"]:
                    st.success("💤 Sleeping on transport - saving money! 🎉")
                    accommodation_name = ""
                    accommodation_cost = 0.0
                elif accommodation_type == "None (transit day)":
                    st.info("🚶 Transit day - no accommodation needed")
                    accommodation_name = ""
                    accommodation_cost = 0.0
                else:
                    accommodation_name = st.text_input("Name/Location", key=f"accommodation_name_{i}", 
                                                     value=day_data.get('accommodation_name', ''),
                                                     placeholder="YHA Edinburgh Central, The Crown Inn...")
                    
                    # UK-specific cost guidance
                    cost_help = {
                        "YHA Hostel": "£15-25/night in dorms",
                        "Independent Hostel": "£12-30/night",
                        "Premier Inn": "£40-80/night",
                        "B&B": "£30-60/night",
                        "Camping": "£10-20/night"
                    }.get(accommodation_type, "Check booking sites for prices")
                    
                    accommodation_cost = st.number_input("Cost (£)", key=f"accommodation_cost_{i}", 
                                                       value=float(day_data.get('accommodation_cost', 0.0)), 
                                                       min_value=0.0, step=1.0,
                                                       help=cost_help)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Notes with UK suggestions
            notes = st.text_area("📝 Notes & Activities", key=f"notes_{i}", 
                               value=day_data.get('notes', ''),
                               placeholder="Visit Edinburgh Castle, try fish & chips, explore the Highlands, check out local pubs...")
            
            # Action buttons with UK styling
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button(f"🗑️ Delete", key=f"delete_{i}", help="Delete this day"):
                    delete_day(i)
            with col2:
                if st.button(f"📋 Copy", key=f"copy_{i}", help="Duplicate this day"):
                    copy_day(i)
            
            # Update session state
            update_day_data(i, {
                'date': str(date),
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
    st.markdown('<div class="section-header"><h2>💷 Budget Calculator</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.warning("⚠️ Add some days in the Day-by-Day Planning section first!")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; margin: 2rem 0;">
            <h3>💷 Ready to crunch the numbers?</h3>
            <p>Add your itinerary first, then come back here to see your budget breakdown!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Calculate totals from trip data
    total_transport = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
    total_accommodation = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
    
    # UK-specific budget categories
    st.subheader("💳 Additional Budget Categories")
    
    col1, col2 = st.columns(2)
    
    with col1:
        food_budget = st.number_input("Food & Drink (£)", min_value=0.0, value=0.0, step=5.0,
                                    help="Meals: £15-25/day, Pub meals: £8-15, Supermarket: £5-10/day")
        activities_budget = st.number_input("Activities & Attractions (£)", min_value=0.0, value=0.0, step=5.0,
                                          help="Museums: £5-20, Castles: £10-25, Walking tours: £10-15")
        
    with col2:
        shopping_budget = st.number_input("Shopping & Souvenirs (£)", min_value=0.0, value=0.0, step=5.0,
                                        help="Souvenirs, local goods, charity shop finds")
        emergency_budget = st.number_input("Emergency Fund (£)", min_value=0.0, value=0.0, step=10.0,
                                         help="10-15% of total budget recommended")
    
    # UK-specific additional costs
    col1, col2 = st.columns(2)
    with col1:
        insurance_cost = st.number_input("Travel Insurance (£)", min_value=0.0, value=0.0, step=5.0,
                                       help="Usually £10-30 for UK trips")
    with col2:
        misc_costs = st.number_input("Miscellaneous (£)", min_value=0.0, value=0.0, step=5.0,
                                   help="Laundry, phone credit, unexpected costs")
    
    # Calculate totals
    additional_costs = food_budget + activities_budget + shopping_budget + emergency_budget + insurance_cost + misc_costs
    total_planned = total_transport + total_accommodation + additional_costs
    total_budget = st.session_state.budget_data['total_budget']
    remaining = total_budget - total_planned
    
    # Display budget summary with UK styling
    st.markdown('<div class="uk-divider"></div>', unsafe_allow_html=True)
    st.subheader("📊 Budget Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Budget", f"£{total_budget:,.2f}")
    with col2:
        st.metric("📝 Planned Expenses", f"£{total_planned:,.2f}")
    with col3:
        st.metric("💸 Remaining", f"£{remaining:,.2f}", 
                 delta=f"£{remaining:.2f}" if remaining >= 0 else f"-£{abs(remaining):.2f}")
    with col4:
        percentage = (total_planned / total_budget * 100) if total_budget > 0 else 0
        st.metric("📈 Budget Used", f"{percentage:.1f}%")
    
    # Budget status with British flair
    if remaining < 0:
        st.error(f"💸 Blimey! You're over budget by £{abs(remaining):,.2f}! Time to find some bargains!")
    elif remaining < total_budget * 0.1:
        st.warning("🔶 Crikey! You're cutting it close with your budget!")
    else:
        st.success("✅ Brilliant! You're well within budget - might even have money for a proper Sunday roast! 🥩")
    
    # Detailed breakdown with UK charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget breakdown pie chart with UK colors
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
            
            # Remove zero values
            budget_breakdown = {k: v for k, v in budget_breakdown.items() if v > 0}
            
            if budget_breakdown:
                fig = px.pie(
                    values=list(budget_breakdown.values()),
                    names=list(budget_breakdown.keys()),
                    title="💷 Budget Breakdown",
                    color_discrete_sequence=['#dc2626', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#06b6d4', '#84cc16']
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    font=dict(family="Source Sans Pro", size=12),
                    title_font=dict(family="Playfair Display", size=16, color="#1e3a8a")
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Daily expenses chart with UK styling
        if st.session_state.trip_data:
            df = pd.DataFrame(st.session_state.trip_data)
            df['total_daily_cost'] = df['transport_cost'].astype(float) + df['accommodation_cost'].astype(float)
            df['day_label'] = df['day'].astype(str) + ' - ' + df['location'].fillna('TBD')
            
            fig = px.bar(
                df, 
                x='day', 
                y='total_daily_cost',
                title="📈 Daily Expenses (Transport + Accommodation)",
                labels={'day': 'Day', 'total_daily_cost': 'Cost (£)'},
                color='total_daily_cost',
                color_continuous_scale=['#3b82f6', '#dc2626']
            )
            fig.update_layout(
                showlegend=False,
                font=dict(family="Source Sans Pro", size=12),
                title_font=dict(family="Playfair Display", size=16, color="#1e3a8a")
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # UK-specific budget recommendations
    if total_planned > 0:
        st.markdown('<div class="uk-divider"></div>', unsafe_allow_html=True)
        st.subheader("💡 British Budget Tips")
        
        avg_daily_cost = total_planned / len(st.session_state.trip_data) if st.session_state.trip_data else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📊 Average daily cost: £{avg_daily_cost:.2f}")
            if avg_daily_cost > 60:
                st.warning("💰 Quite pricey! Try Wetherspoons for cheap meals, book buses early, and consider hostels")
            elif avg_daily_cost < 30:
                st.success("🎉 Brilliant budget! You're traveling like a proper backpacker!")
        
        with col2:
            transport_percent = (total_transport / total_planned * 100) if total_planned > 0 else 0
            st.info(f"🚌 Transport is {transport_percent:.1f}% of your budget")
            if transport_percent > 40:
                st.warning("🚌 Transport costs are high - try Megabus advance bookings or split train tickets!")
            
        # UK-specific money-saving tips
        st.markdown("""
        **💸 Money-Saving Tips for Britain:**
        - 🚌 Book Megabus/National Express in advance for £1-5 fares
        - 🚂 Use split-ticketing apps like Trainline for cheaper train fares
        - 🏨 Stay in YHA hostels or book Premier Inn early for deals
        - 🍺 Eat at Wetherspoons for cheap pub grub (£4-8 meals)
        - 🛍️ Shop at Tesco/ASDA for groceries, avoid M&S for budget trips
        - 🎭 Many museums are free! Tate Modern, British Museum, National Gallery
        - ☕ Grab coffee from Greggs or Pret for under £3
        """)

def trip_summary():
    st.markdown('<div class="section-header"><h2>📋 Trip Summary</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; margin: 2rem 0;">
            <h3>📋 No trip data yet!</h3>
            <p>Start planning in the Day-by-Day section, then come back for your summary!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Trip overview with British styling
    trip_name = st.session_state.trip_info.get('name', 'My British Adventure')
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 50%, #dc2626 100%); 
                color: white; padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;">
        <h2 style="margin: 0; font-family: 'Playfair Display', serif;">🇬🇧 {trip_name}</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Your brilliant British adventure awaits!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Trip statistics with UK styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📅 Total Days", len(st.session_state.trip_data))
    with col2:
        total_transport_cost = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
        st.metric("🚌 Transport Cost", f"£{total_transport_cost:.2f}")
    with col3:
        total_accommodation_cost = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
        st.metric("🏨 Accommodation Cost", f"£{total_accommodation_cost:.2f}")
    with col4:
        total_cost = total_transport_cost + total_accommodation_cost
        st.metric("💰 Total Cost", f"£{total_cost:.2f}")
    
    # Detailed itinerary with British flair
    st.markdown('<div class="uk-divider"></div>', unsafe_allow_html=True)
    st.subheader("🗓️ Your British Itinerary")
    
    for day in st.session_state.trip_data:
        with st.container():
            # Day header with cost and British styling
            day_cost = day.get('transport_cost', 0.0) + day.get('accommodation_cost', 0.0)
            
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #f8fafc 0%, #e2e8f0 100%); 
                        padding: 1rem; border-radius: 8px; border-left: 4px solid #dc2626; margin: 1rem 0;">
                <h3 style="margin: 0; color: #1e3a8a;">📍 Day {day['day']} - {day.get('location', 'TBD')} | £{day_cost:.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if day.get('date'):
                st.markdown(f"**📅 Date:** {day['date']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🚌 Getting There:**")
                if day.get('transport_from') and day.get('transport_to'):
                    st.write(f"• **Route:** {day['transport_from']} → {day['transport_to']}")
                    st.write(f"• **Transport:** {day.get('transport_type', 'TBD')}")
                    if day.get('transport_time'):
                        st.write(f"• **Departure:** {day['transport_time']}")
                    st.write(f"• **Cost:** £{day.get('transport_cost', 0):.2f}")
                else:
                    st.write("• Transport details to be sorted")
                    
            with col2:
                st.markdown("**🏨 Where You're Staying:**")
                acc_type = day.get('accommodation_type', 'TBD')
                if acc_type in ["Sleeper Train", "Night Bus"]:
                    st.write(f"• **Sleeping on:** {acc_type}")
                    st.write("• **Cost:** Included in transport (brilliant!)")
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
            
            st.markdown('<div class="uk-divider"></div>', unsafe_allow_html=True)
    
    # Export functionality with British flair
    st.subheader("📤 Share Your Adventure")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📁 Download CSV", type="primary"):
            df = pd.DataFrame(st.session_state.trip_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="💾 Download Trip Data",
                data=csv,
                file_name=f"{trip_name.replace(' ', '_')}_british_adventure.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Generate Text Summary"):
            itinerary_text = generate_uk_text_itinerary()
            st.text_area("Copy this itinerary:", value=itinerary_text, height=200)
            st.success("✅ Perfect for sharing with mates or keeping as backup!")
    
    with col3:
        if st.button("📊 Detailed Stats"):
            show_uk_trip_statistics()

def show_trip_statistics():
    st.subheader("📊 Your Adventure Statistics")
    
    if not st.session_state.trip_data:
        return
    
    # Transport statistics
    transport_counts = {}
    for day in st.session_state.trip_data:
        transport = day.get('transport_type', 'Unknown')
        transport_counts[transport] = transport_counts.get(transport, 0) + 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚌 How You're Getting Around:**")
        for transport, count in transport_counts.items():
            emoji = "🚌" if "Bus" in transport else "🚂" if "Train" in transport else "🚶" if transport == "Walking" else "🚗"
            st.write(f"{emoji} {transport}: {count} journey{'s' if count != 1 else ''}")
    
    with col2:
        # Accommodation statistics
        accommodation_counts = {}
        for day in st.session_state.trip_data:
            accommodation = day.get('accommodation_type', 'Unknown')
            accommodation_counts[accommodation] = accommodation_counts.get(accommodation, 0) + 1
        
        st.markdown("**🏨 Where You're Staying:**")
        for accommodation, count in accommodation_counts.items():
            emoji = "🏨" if "Hotel" in accommodation else "🏠" if "Hostel" in accommodation else "⛺" if accommodation == "Camping" else "🛏️"
            st.write(f"{emoji} {accommodation}: {count} night{'s' if count != 1 else ''}")
    
    # Cost analysis
    st.markdown("**💰 Cost Breakdown:**")
    total_transport = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
    total_accommodation = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🚌 Total Transport", f"£{total_transport:.2f}")
    with col2:
        st.metric("🏨 Total Accommodation", f"£{total_accommodation:.2f}")
    with col3:
        avg_daily = (total_transport + total_accommodation) / len(st.session_state.trip_data) if st.session_state.trip_data else 0
        st.metric("📊 Avg Daily Cost", f"£{avg_daily:.2f}")

def budget_calculator():
    st.markdown('<div class="section-header"><h2>💰 Budget Calculator</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.markdown("""
        <div class="stats-container">
            <h3 style="text-align: center;">💰 Ready to crunch the numbers?</h3>
            <p style="text-align: center;">Add your itinerary first, then come back here to see your budget breakdown!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Calculate totals from trip data
    total_transport = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
    total_accommodation = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
    
    # Budget categories
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.subheader("💳 Additional Budget Categories")
    
    col1, col2 = st.columns(2)
    
    with col1:
        food_budget = st.number_input("Food & Drink (£)", min_value=0.0, value=0.0, step=5.0,
                                    help="Daily meals, snacks, drinks")
        activities_budget = st.number_input("Activities & Attractions (£)", min_value=0.0, value=0.0, step=5.0,
                                          help="Tours, museums, entertainment")
        
    with col2:
        shopping_budget = st.number_input("Shopping & Souvenirs (£)", min_value=0.0, value=0.0, step=5.0,
                                        help="Souvenirs, local goods, gifts")
        emergency_budget = st.number_input("Emergency Fund (£)", min_value=0.0, value=0.0, step=10.0,
                                         help="10-15% of total budget recommended")
    
    # Additional costs
    col1, col2 = st.columns(2)
    with col1:
        insurance_cost = st.number_input("Travel Insurance (£)", min_value=0.0, value=0.0, step=5.0,
                                       help="Travel protection and coverage")
    with col2:
        misc_costs = st.number_input("Miscellaneous (£)", min_value=0.0, value=0.0, step=5.0,
                                   help="Laundry, phone credit, unexpected costs")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate totals
    additional_costs = food_budget + activities_budget + shopping_budget + emergency_budget + insurance_cost + misc_costs
    total_planned = total_transport + total_accommodation + additional_costs
    total_budget = st.session_state.budget_data['total_budget']
    remaining = total_budget - total_planned
    
    # Display budget summary
    st.markdown('<div class="modern-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    st.subheader("📊 Budget Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Budget", f"£{total_budget:,.2f}")
    with col2:
        st.metric("📝 Planned Expenses", f"£{total_planned:,.2f}")
    with col3:
        st.metric("💸 Remaining", f"£{remaining:,.2f}", 
                 delta=f"£{remaining:.2f}" if remaining >= 0 else f"-£{abs(remaining):.2f}")
    with col4:
        percentage = (total_planned / total_budget * 100) if total_budget > 0 else 0
        st.metric("📈 Budget Used", f"{percentage:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Budget status
    if remaining < 0:
        st.error(f"💸 You're over budget by £{abs(remaining):,.2f}! Time to find some savings!")
    elif remaining < total_budget * 0.1:
        st.warning("🔶 You're cutting it close with your budget!")
    else:
        st.success("✅ Excellent! You're well within budget - room for spontaneous adventures! 🎉")
    
    # Detailed breakdown with charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget breakdown pie chart
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
            
            # Remove zero values
            budget_breakdown = {k: v for k, v in budget_breakdown.items() if v > 0}
            
            if budget_breakdown:
                fig = px.pie(
                    values=list(budget_breakdown.values()),
                    names=list(budget_breakdown.keys()),
                    title="💰 Budget Breakdown",
                    color_discrete_sequence=['#dc2626', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#06b6d4', '#84cc16']
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    font=dict(family="Inter", size=12),
                    title_font=dict(family="Space Grotesk", size=16, color="#1e293b")
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Daily expenses chart
        if st.session_state.trip_data:
            df = pd.DataFrame(st.session_state.trip_data)
            df['total_daily_cost'] = df['transport_cost'].astype(float) + df['accommodation_cost'].astype(float)
            
            fig = px.bar(
                df, 
                x='day', 
                y='total_daily_cost',
                title="📈 Daily Expenses (Transport + Accommodation)",
                labels={'day': 'Day', 'total_daily_cost': 'Cost (£)'},
                color='total_daily_cost',
                color_continuous_scale=['#3b82f6', '#dc2626']
            )
            fig.update_layout(
                showlegend=False,
                font=dict(family="Inter", size=12),
                title_font=dict(family="Space Grotesk", size=16, color="#1e293b")
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Budget recommendations
    if total_planned > 0:
        st.markdown('<div class="modern-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("💡 Budget Tips")
        
        avg_daily_cost = total_planned / len(st.session_state.trip_data) if st.session_state.trip_data else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📊 Average daily cost: £{avg_daily_cost:.2f}")
            if avg_daily_cost > 60:
                st.warning("💰 Quite expensive! Consider budget accommodations, local transport, and cooking your own meals")
            elif avg_daily_cost < 30:
                st.success("🎉 Great budget management! You're traveling efficiently!")
        
        with col2:
            transport_percent = (total_transport / total_planned * 100) if total_planned > 0 else 0
            st.info(f"🚌 Transport is {transport_percent:.1f}% of your budget")
            if transport_percent > 40:
                st.warning("🚌 Transport costs are high - try booking in advance or overnight journeys!")
            
        # Money-saving tips
        st.markdown("""
        **💸 Money-Saving Tips:**
        - 🚌 Book transport in advance for better deals
        - 🏨 Stay in hostels or consider overnight transport
        - 🍽️ Cook your own meals or eat at local markets
        - 🎭 Look for free activities and walking tours
        - 🛍️ Set a daily spending limit and stick to it
        - 💳 Use travel-friendly bank cards to avoid fees
        """)
        st.markdown('</div>', unsafe_allow_html=True)

def trip_summary():
    st.markdown('<div class="section-header"><h2>📋 Trip Summary</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.markdown("""
        <div class="stats-container">
            <h3 style="text-align: center;">📋 No trip data yet!</h3>
            <p style="text-align: center;">Start planning in the Day-by-Day section, then come back for your summary!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Trip overview
    trip_name = st.session_state.trip_info.get('name', 'My Adventure')
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, var(--primary-blue) 0%, var(--dark-blue) 100%); 
                color: white; padding: 2.5rem 2rem; border-radius: var(--border-radius-lg); 
                text-align: center; margin-bottom: 2rem; box-shadow: var(--shadow-xl);">
        <h2 style="margin: 0; font-family: 'Space Grotesk', sans-serif; font-size: 2.5rem;">🎒 {trip_name}</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 1.2rem;">Your amazing adventure awaits!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Trip statistics
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📅 Total Days", len(st.session_state.trip_data))
    with col2:
        total_transport_cost = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
        st.metric("🚌 Transport Cost", f"£{total_transport_cost:.2f}")
    with col3:
        total_accommodation_cost = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
        st.metric("🏨 Accommodation Cost", f"£{total_accommodation_cost:.2f}")
    with col4:
        total_cost = total_transport_cost + total_accommodation_cost
        st.metric("💰 Total Cost", f"£{total_cost:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed itinerary
    st.markdown('<div class="modern-divider"></div>', unsafe_allow_html=True)
    st.subheader("🗓️ Your Detailed Itinerary")
    
    for day in st.session_state.trip_data:
        with st.container():
            # Day header with cost
            day_cost = day.get('transport_cost', 0.0) + day.get('accommodation_cost', 0.0)
            
            st.markdown(f"""
            <div class="card-container">
                <h3 style="margin: 0; color: var(--gray-800);">📍 Day {day['day']} - {day.get('location', 'TBD')} | £{day_cost:.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if day.get('date'):
                st.markdown(f"**📅 Date:** {day['date']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🚌 Getting There:**")
                if day.get('transport_from') and day.get('transport_to'):
                    st.write(f"• **Route:** {day['transport_from']} → {day['transport_to']}")
                    st.write(f"• **Transport:** {day.get('transport_type', 'TBD')}")
                    if day.get('transport_time'):
                        st.write(f"• **Departure:** {day['transport_time']}")
                    st.write(f"• **Cost:** £{day.get('transport_cost', 0):.2f}")
                else:
                    st.write("• Transport details to be added")
                    
            with col2:
                st.markdown("**🏨 Where You're Staying:**")
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
            
            st.markdown('<div class="modern-divider"></div>', unsafe_allow_html=True)
    
    # Export functionality
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.subheader("📤 Share Your Adventure")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📁 Download CSV", type="primary"):
            df = pd.DataFrame(st.session_state.trip_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="💾 Download Trip Data",
                data=csv,
                file_name=f"{trip_name.replace(' ', '_')}_adventure.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Generate Text Summary"):
            itinerary_text = generate_text_itinerary()
            st.text_area("Copy this itinerary:", value=itinerary_text, height=200)
            st.success("✅ Perfect for sharing or keeping as backup!")
    
    with col3:
        if st.button("📊 Detailed Stats"):
            show_trip_statistics()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
