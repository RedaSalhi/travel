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

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_suggested_budget(travel_style, days):
    """Calculate suggested budget based on travel style and duration"""
    daily_rates = {
        "Budget Backpacker": (25, 40),
        "Mid-range Explorer": (40, 70),
        "Comfort Traveller": (70, 120)
    }
    
    style_key = travel_style.split('(')[0].strip()
    
    if style_key in daily_rates:
        low, high = daily_rates[style_key]
        return (low + high) / 2 * days
    
    return 50 * days

def calculate_day_completion(day_data):
    """Calculate completion percentage for a day's planning"""
    required_fields = ['location', 'transport_from', 'transport_to', 'accommodation_type']
    optional_fields = ['date', 'transport_time', 'accommodation_name', 'notes']
    
    required_completed = sum(1 for field in required_fields if day_data.get(field))
    required_score = (required_completed / len(required_fields)) * 0.7
    
    optional_completed = sum(1 for field in optional_fields if day_data.get(field))
    optional_score = (optional_completed / len(optional_fields)) * 0.3
    
    return required_score + optional_score

def get_transport_emoji(transport_type):
    """Get emoji for transport type"""
    emoji_map = {
        'Bus': '🚌', 'Bus (overnight)': '🚌', 'Train': '🚂', 'Train (overnight)': '🚂',
        'Plane': '✈️', 'Ferry': '⛴️', 'Car/Taxi': '🚗', 'Walking': '🚶',
        'Local Transport': '🚊', 'Cycling': '🚴'
    }
    return emoji_map.get(transport_type, '🚌')

def get_accommodation_emoji(accommodation_type):
    """Get emoji for accommodation type"""
    emoji_map = {
        'Hostel': '🏠', 'Hotel': '🏨', 'Guesthouse': '🏡', 'Camping': '⛺',
        'Bus (sleeping)': '🚌', 'Train (sleeping)': '🚂', 'Airbnb': '🏠',
        'Couchsurfing': '🛋️', "Friend's place": '👥', 'None (transit day)': '🚶'
    }
    return emoji_map.get(accommodation_type, '🏠')

# ============================================================================
# CSS STYLING
# ============================================================================

def load_css():
    st.markdown("""
    <style>
    /* Hide sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Modern color palette */
    :root {
        --primary: #667eea;
        --secondary: #f5576c;
        --success: #4facfe;
        --warning: #fa709a;
    }
    
    /* Main container */
    .main .block-container {
        padding: 1rem;
        max-width: 1400px;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .app-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .app-header p {
        font-size: 1.2rem;
        margin: 1rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Section headers */
    .section-header {
        font-size: 2.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 2rem 0;
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Transport section styling */
    .transport-section {
        background: linear-gradient(135deg, #e6f3ff 0%, #cce7ff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #b3d9ff;
        margin-bottom: 1rem;
    }
    
    /* Accommodation section styling */
    .accommodation-section {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4e8 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #ffb3c1;
        margin-bottom: 1rem;
    }
    
    /* Session warning */
    .session-warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #f39c12;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .app-header h1 { font-size: 2rem; }
        .main .block-container { padding: 0.5rem; }
        .card { padding: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION (No File Storage)
# ============================================================================

def init_session_state():
    """Initialize session state - each user gets their own data"""
    
    # Initialize trip data (empty for each new session)
    if 'trip_data' not in st.session_state:
        st.session_state.trip_data = []

    # Initialize budget data with defaults
    if 'budget_data' not in st.session_state:
        st.session_state.budget_data = {
            'total_budget': 1000.0,
            'food_budget': 0.0,
            'activities_budget': 0.0,
            'shopping_budget': 0.0,
            'misc_costs': 0.0,
            'emergency_budget': 0.0,
            'insurance_cost': 0.0,
            'currency': 'GBP'
        }

    # Initialize trip info with defaults
    if 'trip_info' not in st.session_state:
        st.session_state.trip_info = {
            'name': '',
            'start_date': None,
            'end_date': None,
            'destinations': '',
            'travel_style': '🎒 Budget Backpacker (£25-40/day)',
            'group_size': 1,
            'transport_preference': '🚌 Bus',
            'accommodation_preference': '🏠 Hostels'
        }
    
    # Track if this is a new session
    if 'session_initialized' not in st.session_state:
        st.session_state.session_initialized = True
        st.session_state.is_new_session = True
    else:
        st.session_state.is_new_session = False

# ============================================================================
# COMPONENT FUNCTIONS
# ============================================================================

def session_info_banner():
    """Display session information banner"""
    st.markdown("""
    <div class="session-warning">
        <h4>ℹ️ Session-Based Storage</h4>
        <p><strong>Your data is private!</strong> Each user gets their own session. 
        Your trip data will be lost when you close your browser or the session expires. 
        Use the export feature to save your plans permanently.</p>
    </div>
    """, unsafe_allow_html=True)

def trip_overview():
    """Trip overview component"""
    st.markdown('<h2 class="section-header">🌍 Trip Overview</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📝 Basic Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            trip_name = st.text_input(
                "🎯 Trip Name", 
                value=st.session_state.trip_info.get('name', ''),
                placeholder="e.g., European Adventure",
                key="trip_name_input"
            )
            
            start_date = st.date_input(
                "📅 Start Date", 
                value=st.session_state.trip_info.get('start_date'),
                key="start_date_input"
            )
            
            end_date = st.date_input(
                "🏁 End Date", 
                value=st.session_state.trip_info.get('end_date'),
                key="end_date_input"
            )
            
        with col2:
            destinations = st.text_area(
                "🗺️ Main Destinations", 
                value=st.session_state.trip_info.get('destinations', ''),
                placeholder="List your must-visit places...",
                height=120,
                key="destinations_input"
            )
            
            total_budget = st.number_input(
                "💰 Total Budget (£)", 
                min_value=0.0, 
                value=st.session_state.budget_data.get('total_budget', 1000.0),
                step=100.0,
                key="total_budget_input"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Travel preferences
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
                index=0,
                key="travel_style_input"
            )
        
        with col2:
            group_size = st.number_input(
                "👥 Group Size", 
                min_value=1, 
                max_value=20, 
                value=st.session_state.trip_info.get('group_size', 1),
                key="group_size_input"
            )
        
        with col3:
            transport_preference = st.selectbox(
                "🚌 Preferred Transport", 
                ["🚌 Bus", "🚂 Train", "🔄 Mix of Both", "✈️ Airlines", "🚗 Car Rental"],
                key="transport_pref_input"
            )
        
        with col4:
            accommodation_preference = st.selectbox(
                "🏨 Accommodation Style",
                ["🏠 Hostels", "🏨 Hotels", "🏡 Mix of Both", "⛺ Camping", "🏘️ Local Stays"],
                key="accommodation_pref_input"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Save button
        if st.button("💾 Save Trip Overview", type="primary", key="save_overview_btn"):
            # Update session state directly
            st.session_state.trip_info.update({
                'name': trip_name,
                'start_date': start_date,
                'end_date': end_date,
                'destinations': destinations,
                'travel_style': travel_style,
                'group_size': group_size,
                'transport_preference': transport_preference,
                'accommodation_preference': accommodation_preference
            })

            st.session_state.budget_data['total_budget'] = total_budget
            st.success("✅ Trip overview saved to your session!")
            
            # Budget suggestions
            if start_date and end_date and end_date > start_date:
                suggested_days = (end_date - start_date).days + 1
                suggested_budget = calculate_suggested_budget(travel_style, suggested_days)
                
                if total_budget < suggested_budget * 0.8:
                    st.warning(f"💡 Consider budgeting £{suggested_budget:.0f} for {suggested_days} days")

def day_by_day_planning():
    """Day-by-day planning component"""
    st.markdown('<h2 class="section-header">📅 Day-by-Day Planning</h2>', unsafe_allow_html=True)
    
    # Add days section
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("➕ Add New Day", type="primary", key="add_day_btn"):
            add_new_day()
            st.rerun()
    
    with col2:
        days_to_add = st.number_input("Add Multiple", min_value=1, max_value=10, value=1, key="days_to_add_input")
    
    with col3:
        if st.button(f"Add {days_to_add} Days", key="add_multiple_days_btn"):
            for _ in range(int(days_to_add)):
                add_new_day()
            st.rerun()
    
    if not st.session_state.trip_data:
        st.info("👆 Click 'Add New Day' to start planning your itinerary!")
        return
    
    # Clear all button
    if len(st.session_state.trip_data) > 0:
        if st.button("🗑️ Clear All Days", type="secondary", key="clear_all_btn"):
            st.session_state.trip_data = []
            st.rerun()
    
    # Display days
    for i, day_data in enumerate(st.session_state.trip_data):
        day_cost = day_data.get('transport_cost', 0.0) + day_data.get('accommodation_cost', 0.0)
        completion = calculate_day_completion(day_data)
        progress_indicator = "🟢" if completion >= 0.8 else "🟡" if completion >= 0.4 else "🔴"
        
        with st.expander(f"{progress_indicator} Day {day_data['day']} - {day_data.get('location', 'Location TBD')} | £{day_cost:.2f}", 
                        expanded=i == len(st.session_state.trip_data) - 1):
            
            # Date and location
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("📅 Date", key=f"date_{i}", 
                                   value=pd.to_datetime(day_data.get('date')).date() if day_data.get('date') else None)
            with col2:
                location = st.text_input("📍 Location", key=f"location_{i}", 
                                       value=day_data.get('location', ''))
            
            # Transport and accommodation
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="transport-section">', unsafe_allow_html=True)
                st.markdown("#### 🚌 Transportation")
                
                transport_type = st.selectbox("Type", 
                    ["Bus", "Train", "Plane", "Ferry", "Car/Taxi", "Walking"], 
                    key=f"transport_type_{i}",
                    index=["Bus", "Train", "Plane", "Ferry", "Car/Taxi", "Walking"].index(day_data.get('transport_type', 'Bus')))
                
                col_from, col_to = st.columns(2)
                with col_from:
                    transport_from = st.text_input("From", key=f"transport_from_{i}", 
                                                 value=day_data.get('transport_from', ''))
                with col_to:
                    transport_to = st.text_input("To", key=f"transport_to_{i}", 
                                               value=day_data.get('transport_to', ''))
                
                col_time, col_cost = st.columns(2)
                with col_time:
                    transport_time = st.text_input("Time", key=f"transport_time_{i}", 
                                                 value=day_data.get('transport_time', ''))
                with col_cost:
                    transport_cost = st.number_input("Cost (£)", key=f"transport_cost_{i}", 
                                                   value=float(day_data.get('transport_cost', 0.0)),
                                                   min_value=0.0, step=1.0)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col2:
                st.markdown('<div class="accommodation-section">', unsafe_allow_html=True)
                st.markdown("#### 🏨 Accommodation")
                
                accommodation_types = ["Hostel", "Hotel", "Guesthouse", "Camping", "Airbnb", "None"]
                accommodation_type = st.selectbox("Type",
                    accommodation_types, 
                    key=f"accommodation_type_{i}",
                    index=accommodation_types.index(day_data.get('accommodation_type', 'Hostel')))
                
                if accommodation_type != "None":
                    accommodation_name = st.text_input("Name", key=f"accommodation_name_{i}", 
                                                     value=day_data.get('accommodation_name', ''))
                    accommodation_cost = st.number_input("Cost (£)", key=f"accommodation_cost_{i}", 
                                                       value=float(day_data.get('accommodation_cost', 0.0)),
                                                       min_value=0.0, step=1.0)
                else:
                    accommodation_name = ""
                    accommodation_cost = 0.0
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Notes
            notes = st.text_area("📝 Notes & Activities", key=f"notes_{i}", 
                               value=day_data.get('notes', ''), height=80)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("🗑️ Delete", key=f"delete_{i}"):
                    delete_day(i)
                    st.rerun()
            with col2:
                if st.button("📋 Copy", key=f"copy_{i}"):
                    copy_day(i)
                    st.rerun()
            with col3:
                st.progress(completion, text=f"Completion: {completion:.0%}")
            
            # Update session state immediately
            st.session_state.trip_data[i].update({
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
    """Budget calculator component"""
    st.markdown('<h2 class="section-header">💰 Budget Calculator</h2>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.info("Add your itinerary first to see budget calculations!")
        return
    
    # Calculate base costs
    total_transport = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
    total_accommodation = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
    
    # Additional budget categories
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💳 Additional Budget Categories")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        food_budget = st.number_input("🍽️ Food & Drink (£)", min_value=0.0, 
                                    value=st.session_state.budget_data.get('food_budget', 0.0),
                                    step=5.0, key="food_budget_input")
        activities_budget = st.number_input("🎯 Activities (£)", min_value=0.0, 
                                          value=st.session_state.budget_data.get('activities_budget', 0.0),
                                          step=5.0, key="activities_budget_input")
        
    with col2:
        shopping_budget = st.number_input("🛍️ Shopping (£)", min_value=0.0, 
                                        value=st.session_state.budget_data.get('shopping_budget', 0.0),
                                        step=5.0, key="shopping_budget_input")
        misc_costs = st.number_input("📱 Miscellaneous (£)", min_value=0.0, 
                                   value=st.session_state.budget_data.get('misc_costs', 0.0),
                                   step=5.0, key="misc_budget_input")
    
    with col3:
        emergency_budget = st.number_input("🚨 Emergency Fund (£)", min_value=0.0, 
                                         value=st.session_state.budget_data.get('emergency_budget', 0.0),
                                         step=10.0, key="emergency_budget_input")
        insurance_cost = st.number_input("🛡️ Insurance (£)", min_value=0.0, 
                                       value=st.session_state.budget_data.get('insurance_cost', 0.0),
                                       step=5.0, key="insurance_budget_input")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Update budget data in session state
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
    
    # Budget overview
    st.subheader("📊 Budget Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Budget", f"£{total_budget:,.0f}")
    with col2:
        st.metric("📝 Planned", f"£{total_planned:,.0f}")
    with col3:
        st.metric("💸 Remaining", f"£{remaining:,.0f}")
    with col4:
        percentage = (total_planned / total_budget * 100) if total_budget > 0 else 0
        st.metric("📈 Used", f"{percentage:.1f}%")
    
    # Budget status
    if remaining < 0:
        st.error(f"💸 Over budget by £{abs(remaining):,.0f}!")
    elif remaining < total_budget * 0.1:
        st.warning("🔶 Cutting it close with budget!")
    else:
        st.success("✅ Within budget!")
    
    # Budget breakdown chart
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

def trip_summary():
    """Trip summary component"""
    st.markdown('<h2 class="section-header">📋 Trip Summary</h2>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.info("No trip data yet! Start planning to see your summary.")
        return
    
    # Trip header
    trip_name = st.session_state.trip_info.get('name', 'My Adventure')
    
    st.markdown(f"""
    <div class="app-header">
        <h1>🎒 {trip_name}</h1>
        <p>Your adventure summary</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics
    show_trip_stats()
    
    # Detailed itinerary
    st.subheader("🗓️ Your Detailed Itinerary")
    
    for day in st.session_state.trip_data:
        day_cost = day.get('transport_cost', 0.0) + day.get('accommodation_cost', 0.0)
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### 📍 Day {day['day']} - {day.get('location', 'TBD')}")
            with col2:
                st.markdown(f"**£{day_cost:.2f}**")
            
            if day.get('date'):
                st.markdown(f"**📅 Date:** {day['date']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🚌 Transportation:**")
                if day.get('transport_from') and day.get('transport_to'):
                    st.write(f"• {day['transport_from']} → {day['transport_to']}")
                    st.write(f"• {day.get('transport_type', 'TBD')} at {day.get('transport_time', 'TBD')}")
                    st.write(f"• £{day.get('transport_cost', 0):.2f}")
                else:
                    st.write("• Transport details TBD")
                    
            with col2:
                st.markdown("**🏨 Accommodation:**")
                if day.get('accommodation_type') and day.get('accommodation_type') != 'None':
                    st.write(f"• {day.get('accommodation_type', 'TBD')}")
                    if day.get('accommodation_name'):
                        st.write(f"• {day['accommodation_name']}")
                    st.write(f"• £{day.get('accommodation_cost', 0):.2f}")
                else:
                    st.write("• No accommodation")
            
            if day.get('notes'):
                st.markdown(f"**📝 Notes:** {day['notes']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Export options
    st.subheader("📤 Export Your Trip")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📁 Download CSV", type="primary", key="download_csv_btn"):
            try:
                df = pd.DataFrame(st.session_state.trip_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Download Trip Data",
                    data=csv,
                    file_name=f"{trip_name.replace(' ', '_')}_trip.csv",
                    mime="text/csv",
                    key="download_csv_button"
                )
            except Exception as e:
                st.error(f"Error creating CSV: {e}")
    
    with col2:
        if st.button("📋 Generate Text Summary", key="generate_text_btn"):
            try:
                text_summary = generate_text_itinerary()
                st.text_area("Copy this itinerary:", value=text_summary, height=200, key="text_summary_area")
            except Exception as e:
                st.error(f"Error generating summary: {e}")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def show_trip_stats():
    """Display trip statistics"""
    if not st.session_state.trip_data:
        return
        
    total_days = len(st.session_state.trip_data)
    total_transport = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
    total_accommodation = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
    total_cost = total_transport + total_accommodation
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📅 Duration", f"{total_days} days")
    with col2:
        st.metric("🚌 Transport", f"£{total_transport:.0f}")
    with col3:
        st.metric("🏨 Accommodation", f"£{total_accommodation:.0f}")
    with col4:
        st.metric("💰 Total Cost", f"£{total_cost:.0f}")

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

def delete_day(index):
    """Delete a day and renumber remaining days"""
    st.session_state.trip_data.pop(index)
    # Renumber days
    for j, day in enumerate(st.session_state.trip_data):
        day['day'] = j + 1

def copy_day(index):
    """Copy a day with incremented day number"""
    original_day = st.session_state.trip_data[index].copy()
    original_day['day'] = len(st.session_state.trip_data) + 1
    original_day['date'] = ''
    st.session_state.trip_data.append(original_day)

def generate_text_itinerary():
    """Generate text version of the itinerary"""
    trip_name = st.session_state.trip_info.get('name', 'My Adventure')
    start_date = st.session_state.trip_info.get('start_date', '')
    end_date = st.session_state.trip_info.get('end_date', '')
    
    text = f"🎒 {trip_name}\n{'='*50}\n\n"
    
    if start_date and end_date:
        text += f"📅 {start_date} → {end_date}\n"
    
    text += f"🌍 {len(st.session_state.trip_data)} days of adventure\n\n"
    
    total_cost = 0
    for day in st.session_state.trip_data:
        day_cost = day.get('transport_cost', 0) + day.get('accommodation_cost', 0)
        total_cost += day_cost
        
        text += f"📍 Day {day['day']} - {day.get('location', 'TBD')}\n"
        text += f"📅 Date: {day.get('date', 'TBD')}\n"
        text += f"🚌 Transport: {day.get('transport_from', 'TBD')} → {day.get('transport_to', 'TBD')}\n"
        text += f"   Type: {day.get('transport_type', 'TBD')}\n"
        
        if day.get('transport_time'):
            text += f"   Time: {day['transport_time']}\n"
            
        text += f"🏨 Accommodation: {day.get('accommodation_type', 'TBD')}\n"
        
        if day.get('accommodation_name'):
            text += f"   Place: {day['accommodation_name']}\n"
        
        if day.get('notes'):
            text += f"📝 Notes: {day['notes']}\n"
            
        text += f"💰 Daily Cost: £{day_cost:.2f}\n"
        text += "-" * 50 + "\n\n"
    
    text += f"💰 Total Trip Cost: £{total_cost:.2f}\n"
    text += f"🎒 Total Days: {len(st.session_state.trip_data)}\n"
    
    if len(st.session_state.trip_data) > 0:
        avg_daily = total_cost / len(st.session_state.trip_data)
        text += f"📊 Average Daily Cost: £{avg_daily:.2f}\n"
    
    text += "\n🌟 Have an amazing adventure! Safe travels! 🎒"
    
    return text

def analytics_dashboard():
    """Analytics dashboard for trip insights"""
    st.markdown('<h2 class="section-header">📊 Trip Analytics</h2>', unsafe_allow_html=True)
    
    if not st.session_state.trip_data:
        st.info("No data to analyze yet! Add your trip details first.")
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
                labels={'x': 'Transport Type', 'y': 'Number of Days'}
            )
            fig.update_layout(showlegend=False)
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
                title="Accommodation Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Daily costs chart
    if st.session_state.trip_data:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💰 Daily Expenses")
        
        days = [day['day'] for day in st.session_state.trip_data]
        costs = [day.get('transport_cost', 0) + day.get('accommodation_cost', 0) for day in st.session_state.trip_data]
        
        fig = px.bar(
            x=days,
            y=costs,
            title="Daily Cost Breakdown",
            labels={'x': 'Day', 'y': 'Cost (£)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function"""
    # Initialize session state
    init_session_state()
    
    # Load CSS
    load_css()
    
    # Session info banner
    session_info_banner()
    
    # Header
    st.markdown("""
    <div class="app-header">
        <h1>🎒 Adventure Planner</h1>
        <p>Plan your perfect backpacking journey - your data stays private!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats if trip data exists
    if st.session_state.trip_data:
        show_trip_stats()
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌍 Trip Overview", 
        "📅 Day Planning", 
        "💰 Budget", 
        "📊 Analytics",
        "📋 Summary"
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
    
    # Footer with session reminder
    st.markdown("""
    <div style="text-align: center; padding: 2rem; margin-top: 3rem; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; border-radius: 12px;">
        <p>🎒 Made with ❤️ for adventurers | Your data is session-only and private! 🌟</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            💡 Tip: Export your trip data before closing the browser to save your plans permanently
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
