import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Backpacking Trip Planner",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS styling with clean light theme
def load_css():
    st.markdown("""
    <style>
    /* Import clean fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Hide sidebar completely */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Clean light theme variables */
    :root {
        --primary: #2563eb;
        --primary-light: #3b82f6;
        --secondary: #f59e0b;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --background: #ffffff;
        --surface: #f8fafc;
        --border: #e2e8f0;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --radius: 8px;
        --radius-lg: 12px;
    }
    
    /* Main container */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1200px;
        background: var(--background);
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: var(--radius-lg);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
    }
    
    .app-header h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .app-header p {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        margin: 1rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Stats overview */
    .stats-overview {
        background: var(--surface);
        padding: 2rem;
        border-radius: var(--radius-lg);
        border: 1px solid var(--border);
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }
    
    /* Card styling */
    .card {
        background: var(--background);
        border-radius: var(--radius-lg);
        padding: 2rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        margin-bottom: 2rem;
        transition: all 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        color: var(--text-primary);
        text-align: center;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid var(--primary);
    }
    
    /* Transport section */
    .transport-section {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        padding: 1.5rem;
        border-radius: var(--radius);
        border: 1px solid #93c5fd;
        margin-bottom: 1rem;
    }
    
    /* Accommodation section */
    .accommodation-section {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        padding: 1.5rem;
        border-radius: var(--radius);
        border: 1px solid #fca5a5;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: var(--radius);
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        background: var(--primary-light);
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input {
        border: 1px solid var(--border);
        border-radius: var(--radius);
        font-family: 'Inter', sans-serif;
        background: var(--background);
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        outline: none;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--surface);
        padding: 0.5rem;
        border-radius: var(--radius);
        border: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-radius: var(--radius);
        color: var(--text-secondary);
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary);
        color: white;
        box-shadow: var(--shadow);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f1f5f9;
        border-color: var(--primary);
    }
    
    /* Alert styling */
    .stSuccess {
        background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
        border-radius: var(--radius);
        border: none;
    }
    
    .stWarning {
        background: linear-gradient(135deg, var(--warning) 0%, #d97706 100%);
        border-radius: var(--radius);
        border: none;
    }
    
    .stError {
        background: linear-gradient(135deg, var(--error) 0%, #dc2626 100%);
        border-radius: var(--radius);
        border: none;
    }
    
    .stInfo {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        border-radius: var(--radius);
        border: none;
    }
    
    /* Chart styling */
    .js-plotly-plot {
        border-radius: var(--radius);
        border: 1px solid var(--border);
        background: var(--background);
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    p, div, span, label {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-secondary) !important;
        line-height: 1.6 !important;
    }
    
    /* Footer */
    .footer {
        background: var(--surface);
        color: var(--text-secondary);
        text-align: center;
        padding: 2rem;
        border-radius: var(--radius-lg);
        border: 1px solid var(--border);
        margin-top: 3rem;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .app-header h1 {
            font-size: 2.5rem;
        }
        
        .main .block-container {
            padding: 1rem 0.5rem;
        }
        
        .card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'trip_data' not in st.session_state:
    st.session_state.trip_data = []
if 'budget_data' not in st.session_state:
    st.session_state.budget_data = {
        'total_budget': 500.0,
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
    
    # Header
    st.markdown("""
    <div class="app-header">
        <h1>🎒 Backpacking Trip Planner</h1>
        <p>Plan your perfect adventure with ease and style</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats if trip data exists
    if st.session_state.trip_data:
        show_trip_stats()
    
    # Main navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🌍 Trip Overview", "📅 Day-by-Day Planning", "💰 Budget Calculator", "📋 Trip Summary"])
    
    with tab1:
        trip_overview()
    
    with tab2:
        day_by_day_planning()
    
    with tab3:
        budget_calculator()
    
    with tab4:
        trip_summary()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🎒 Made with ❤️ for adventurers everywhere | Safe travels! 🌟</p>
    </div>
    """, unsafe_allow_html=True)

def show_trip_stats():
    """Display quick trip statistics"""
    total_days = len(st.session_state.trip_data)
    total_cost = sum(day.get('transport_cost', 0.0) + day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
    budget = st.session_state.budget_data['total_budget']
    remaining = budget - total_cost
    percentage_used = (total_cost / budget * 100) if budget > 0 else 0
    
    st.markdown("""
    <div class="stats-overview">
        <h3 style="text-align: center; margin-bottom: 1.5rem;">📊 Trip Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
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
    st.subheader("🗓️ Your Detailed Itinerary")
    
    for day in st.session_state.trip_data:
        day_cost = day.get('transport_cost', 0.0) + day.get('accommodation_cost', 0.0)
        
        st.markdown(f"""
        <div class="card">
            <h3>📍 Day {day['day']} - {day.get('location', 'TBD')} | £{day_cost:.2f}</h3>
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
        
        st.markdown("---")
    
    # Export functionality
    st.markdown('<div class="card">', unsafe_allow_html=True)
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
            st.success("✅ Perfect for sharing!")
    
    with col3:
        if st.button("📊 Detailed Stats"):
            show_detailed_statistics()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Helper functions
def add_new_day():
    """Add a new day to the trip"""
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
    """Delete a day from the trip"""
    st.session_state.trip_data.pop(index)
    # Renumber remaining days
    for j, remaining_day in enumerate(st.session_state.trip_data):
        remaining_day['day'] = j + 1
    st.rerun()

def copy_day(index):
    """Copy a day"""
    original_day = st.session_state.trip_data[index].copy()
    original_day['day'] = len(st.session_state.trip_data) + 1
    original_day['date'] = ''
    st.session_state.trip_data.append(original_day)
    st.rerun()

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

def generate_text_itinerary():
    """Generate a text version of the itinerary"""
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

def show_detailed_statistics():
    """Show detailed trip statistics"""
    if not st.session_state.trip_data:
        return
    
    st.subheader("📊 Detailed Trip Statistics")
    
    # Transport statistics
    transport_counts = {}
    for day in st.session_state.trip_data:
        transport = day.get('transport_type', 'Unknown')
        transport_counts[transport] = transport_counts.get(transport, 0) + 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚌 Transport Breakdown:**")
        for transport, count in transport_counts.items():
            emoji = "🚌" if "Bus" in transport else "🚂" if "Train" in transport else "🚶" if transport == "Walking" else "🚗"
            st.write(f"{emoji} {transport}: {count} journey{'s' if count != 1 else ''}")
    
    with col2:
        # Accommodation statistics
        accommodation_counts = {}
        for day in st.session_state.trip_data:
            accommodation = day.get('accommodation_type', 'Unknown')
            accommodation_counts[accommodation] = accommodation_counts.get(accommodation, 0) + 1
        
        st.markdown("**🏨 Accommodation Breakdown:**")
        for accommodation, count in accommodation_counts.items():
            emoji = "🏨" if "Hotel" in accommodation else "🏠" if "Hostel" in accommodation else "⛺" if accommodation == "Camping" else "🛏️"
            st.write(f"{emoji} {accommodation}: {count} night{'s' if count != 1 else ''}")
    
    # Cost analysis
    st.markdown("**💰 Cost Analysis:**")
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

if __name__ == "__main__":
    main()

def trip_overview():
    """Trip overview and basic information"""
    st.markdown('<h2 class="section-header">🌍 Trip Overview</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        trip_name = st.text_input(
            "Trip Name", 
            value=st.session_state.trip_info['name'],
            placeholder="e.g., European Adventure, UK Road Trip"
        )
        
        start_date = st.date_input(
            "Start Date", 
            value=st.session_state.trip_info['start_date']
        )
        
        end_date = st.date_input(
            "End Date", 
            value=st.session_state.trip_info['end_date']
        )
        
    with col2:
        destinations = st.text_area(
            "Main Destinations", 
            value=st.session_state.trip_info['destinations'],
            placeholder="List your must-visit places...",
            height=100
        )
        
        total_budget = st.number_input(
            "Total Budget (£)", 
            min_value=0.0, 
            value=st.session_state.budget_data['total_budget'],
            step=50.0,
            help="Set your overall trip budget"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Travel preferences
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Travel Preferences")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        travel_style = st.selectbox(
            "Travel Style", 
            ["Budget Backpacker (£25-40/day)", "Mid-range Explorer (£40-70/day)", "Comfort Traveller (£70+/day)"]
        )
    with col2:
        group_size = st.number_input("Group Size", min_value=1, max_value=20, value=1, step=1)
    with col3:
        transport_preference = st.selectbox(
            "Preferred Transport", 
            ["Bus", "Train", "Mix of Both", "Budget Airlines", "Car Rental"]
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Travel tips
    st.info("💡 **Travel Tips:** Book transport in advance for better deals, consider overnight journeys to save on accommodation, and always have backup plans!")
    
    if st.button("💾 Save Trip Overview", type="primary"):
        st.session_state.trip_info.update({
            'name': trip_name,
            'start_date': start_date,
            'end_date': end_date,
            'destinations': destinations
        })
        st.session_state.budget_data['total_budget'] = total_budget
        st.success("✅ Trip overview saved! Ready to plan your adventure!")
        
        # Auto-suggest days
        if start_date and end_date and end_date > start_date:
            suggested_days = (end_date - start_date).days
            if suggested_days > len(st.session_state.trip_data):
                st.info(f"📅 Based on your dates, you might want to plan {suggested_days} days. Head to Day-by-Day Planning to add more days!")

def day_by_day_planning():
    """Day by day trip planning"""
    st.markdown('<h2 class="section-header">📅 Day-by-Day Planning</h2>', unsafe_allow_html=True)
    
    # Add new days section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("➕ Add New Day", type="primary"):
            add_new_day()
    
    with col2:
        days_to_add = st.number_input("Add Multiple Days", min_value=1, max_value=30, value=1, step=1)
    
    with col3:
        if st.button(f"Add {days_to_add} Days"):
            for _ in range(int(days_to_add)):
                add_new_day()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.markdown("""
        <div class="card">
            <h3 style="text-align: center;">🎒 Ready to start your adventure?</h3>
            <p style="text-align: center;">Click "Add New Day" above to begin planning your journey!</p>
            <p style="text-align: center;"><small>💡 Tip: Plan transport between locations first, then add accommodation</small></p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display days
    for i, day_data in enumerate(st.session_state.trip_data):
        day_cost = day_data.get('transport_cost', 0.0) + day_data.get('accommodation_cost', 0.0)
        
        with st.expander(f"📍 Day {day_data['day']} - {day_data.get('location', 'Location TBD')} | £{day_cost:.2f}", 
                        expanded=i == len(st.session_state.trip_data) - 1):
            
            # Date and location
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Date", key=f"date_{i}")
            with col2:
                location = st.text_input(
                    "Location/City", 
                    key=f"location_{i}", 
                    value=day_data.get('location', ''),
                    placeholder="e.g., Paris, Bangkok, Edinburgh"
                )
            
            # Transport and accommodation
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="transport-section">', unsafe_allow_html=True)
                st.markdown("#### 🚌 Transport")
                
                transport_type = st.selectbox(
                    "Transport Type", 
                    ["Bus", "Bus (overnight)", "Train", "Train (overnight)", "Plane", 
                     "Ferry", "Car/Taxi", "Walking", "Local Transport", "Cycling"],
                    key=f"transport_type_{i}",
                    index=get_transport_index(day_data.get('transport_type', 'Bus'))
                )
                
                transport_from = st.text_input(
                    "From", 
                    key=f"transport_from_{i}", 
                    value=day_data.get('transport_from', ''),
                    placeholder="Departure location"
                )
                
                transport_to = st.text_input(
                    "To", 
                    key=f"transport_to_{i}", 
                    value=day_data.get('transport_to', ''),
                    placeholder="Arrival location"
                )
                
                col_time, col_cost = st.columns(2)
                with col_time:
                    transport_time = st.text_input(
                        "Time", 
                        key=f"transport_time_{i}", 
                        value=day_data.get('transport_time', ''),
                        placeholder="09:30"
                    )
                with col_cost:
                    transport_cost = st.number_input(
                        "Cost (£)", 
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
                        "Name/Location", 
                        key=f"accommodation_name_{i}", 
                        value=day_data.get('accommodation_name', ''),
                        placeholder="Hotel/Hostel name"
                    )
                    accommodation_cost = st.number_input(
                        "Cost (£)", 
                        key=f"accommodation_cost_{i}", 
                        value=float(day_data.get('accommodation_cost', 0.0)), 
                        min_value=0.0, 
                        step=1.0
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Notes
            notes = st.text_area(
                "📝 Notes & Activities", 
                key=f"notes_{i}", 
                value=day_data.get('notes', ''),
                placeholder="Things to do, places to visit, important info..."
            )
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                    delete_day(i)
            with col2:
                if st.button(f"📋 Copy", key=f"copy_{i}"):
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
    """Budget planning and tracking"""
    st.markdown('<h2 class="section-header">💰 Budget Calculator</h2>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.markdown("""
        <div class="card">
            <h3 style="text-align: center;">💰 Ready to crunch the numbers?</h3>
            <p style="text-align: center;">Add your itinerary first, then come back here to see your budget breakdown!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Calculate totals
    total_transport = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
    total_accommodation = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
    
    # Additional budget categories
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💳 Additional Budget Categories")
    
    col1, col2 = st.columns(2)
    
    with col1:
        food_budget = st.number_input("Food & Drink (£)", min_value=0.0, value=0.0, step=5.0)
        activities_budget = st.number_input("Activities & Attractions (£)", min_value=0.0, value=0.0, step=5.0)
        
    with col2:
        shopping_budget = st.number_input("Shopping & Souvenirs (£)", min_value=0.0, value=0.0, step=5.0)
        emergency_budget = st.number_input("Emergency Fund (£)", min_value=0.0, value=0.0, step=10.0)
    
    col1, col2 = st.columns(2)
    with col1:
        insurance_cost = st.number_input("Travel Insurance (£)", min_value=0.0, value=0.0, step=5.0)
    with col2:
        misc_costs = st.number_input("Miscellaneous (£)", min_value=0.0, value=0.0, step=5.0)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate totals
    additional_costs = food_budget + activities_budget + shopping_budget + emergency_budget + insurance_cost + misc_costs
    total_planned = total_transport + total_accommodation + additional_costs
    total_budget = st.session_state.budget_data['total_budget']
    remaining = total_budget - total_planned
    
    # Budget overview
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Budget Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Budget", f"£{total_budget:,.2f}")
    with col2:
        st.metric("📝 Planned Expenses", f"£{total_planned:,.2f}")
    with col3:
        st.metric("💸 Remaining", f"£{remaining:,.2f}")
    with col4:
        percentage = (total_planned / total_budget * 100) if total_budget > 0 else 0
        st.metric("📈 Budget Used", f"{percentage:.1f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Budget status
    if remaining < 0:
        st.error(f"💸 You're over budget by £{abs(remaining):,.2f}!")
    elif remaining < total_budget * 0.1:
        st.warning("🔶 You're cutting it close with your budget!")
    else:
        st.success("✅ Great! You're well within budget!")
    
    # Charts
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
                    title="💰 Budget Breakdown"
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
                labels={'day': 'Day', 'total_daily_cost': 'Cost (£)'}
            )
            st.plotly_chart(fig, use_container_width=True)

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

if __name__ == "__main__":
    main()
