"""
Trip Overview Component
Handles basic trip information and preferences
"""

import streamlit as st
from datetime import datetime
from utils.helpers import save_trip_info, calculate_suggested_budget


def render_trip_overview():
    """Render the trip overview component"""
    st.markdown('<h2 class="section-header">🌍 Trip Overview</h2>', unsafe_allow_html=True)
    
    # Trip basic information
    _render_basic_info()
    
    # Travel preferences
    _render_travel_preferences()
    
    # Save functionality
    _render_save_section()


def _render_basic_info():
    """Render basic trip information section"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Basic Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trip_name = st.text_input(
            "🎯 Trip Name", 
            value=st.session_state.trip_info.get('name', ''),
            placeholder="e.g., European Adventure, Southeast Asia Explorer",
            help="Give your adventure a memorable name!",
            key="overview_trip_name"
        )
        
        start_date = st.date_input(
            "📅 Start Date", 
            value=st.session_state.trip_info.get('start_date'),
            help="When does your adventure begin?",
            key="overview_start_date"
        )
        
        end_date = st.date_input(
            "🏁 End Date", 
            value=st.session_state.trip_info.get('end_date'),
            help="When do you plan to return?",
            key="overview_end_date"
        )
        
    with col2:
        destinations = st.text_area(
            "🗺️ Main Destinations", 
            value=st.session_state.trip_info.get('destinations', ''),
            placeholder="List the places you're most excited to visit...",
            height=120,
            help="Describe your must-visit destinations",
            key="overview_destinations"
        )
        
        total_budget = st.number_input(
            "💰 Total Budget (£)", 
            min_value=0.0, 
            value=st.session_state.budget_data.get('total_budget', 1000.0),
            step=100.0,
            help="Set your overall trip budget - be realistic!",
            key="overview_budget"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Store values in session state for access by save function
    st.session_state._temp_overview = {
        'trip_name': trip_name,
        'start_date': start_date,
        'end_date': end_date,
        'destinations': destinations,
        'total_budget': total_budget
    }


def _render_travel_preferences():
    """Render travel preferences section"""
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
            help="Choose your travel comfort level",
            key="overview_travel_style"
        )
    
    with col2:
        group_size = st.number_input(
            "👥 Group Size", 
            min_value=1, 
            max_value=20, 
            value=st.session_state.trip_info.get('group_size', 1), 
            step=1,
            help="How many travelers in your group?",
            key="overview_group_size"
        )
    
    with col3:
        transport_preference = st.selectbox(
            "🚌 Preferred Transport", 
            ["🚌 Bus", "🚂 Train", "🔄 Mix of Both", "✈️ Budget Airlines", "🚗 Car Rental"],
            help="Your preferred way to get around",
            key="overview_transport_pref"
        )
    
    with col4:
        accommodation_preference = st.selectbox(
            "🏨 Accommodation Style",
            ["🏠 Hostels", "🏨 Hotels", "🏡 Mix of Both", "⛺ Camping", "🏘️ Local Stays"],
            help="Where do you prefer to stay?",
            key="overview_accommodation_pref"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Store preferences in session state
    st.session_state._temp_overview.update({
        'travel_style': travel_style,
        'group_size': group_size,
        'transport_preference': transport_preference,
        'accommodation_preference': accommodation_preference
    })


def _render_save_section():
    """Render save functionality section"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("💾 Save Trip Overview", type="primary", use_container_width=True, key="save_overview"):
            temp_data = st.session_state._temp_overview
            
            # Update session state
            st.session_state.trip_info.update({
                'name': temp_data['trip_name'],
                'start_date': temp_data['start_date'],
                'end_date': temp_data['end_date'],
                'destinations': temp_data['destinations'],
                'travel_style': temp_data['travel_style'],
                'group_size': temp_data['group_size'],
                'transport_preference': temp_data['transport_preference'],
                'accommodation_preference': temp_data['accommodation_preference']
            })
            
            st.session_state.budget_data['total_budget'] = temp_data['total_budget']
            
            st.success("✅ Trip overview saved! Ready to plan your adventure!")
            
            # Auto-suggest days and budget
            _provide_suggestions(temp_data)


def _provide_suggestions(data):
    """Provide helpful suggestions based on input data"""
    start_date = data['start_date']
    end_date = data['end_date']
    travel_style = data['travel_style']
    total_budget = data['total_budget']
    
    if start_date and end_date and end_date > start_date:
        suggested_days = (end_date - start_date).days + 1
        
        if suggested_days > len(st.session_state.trip_data):
            st.info(f"📅 Based on your dates, you might want to plan {suggested_days} days. Head to Day-by-Day Planning to add more days!")
        
        # Budget suggestions
        suggested_budget = calculate_suggested_budget(travel_style, suggested_days)
        
        if total_budget < suggested_budget * 0.8:
            st.warning(f"💡 For a {suggested_days}-day {travel_style.split('(')[0].strip()}, consider budgeting £{suggested_budget:.0f}-£{suggested_budget*1.3:.0f}")
        elif total_budget > suggested_budget * 1.5:
            st.info(f"💰 Great budget! You have plenty of room for upgrades and spontaneous adventures!")


def _render_tips_section():
    """Render helpful tips section"""
    st.info("""
    💡 **Planning Tips:**
    • Book transport in advance for better deals
    • Consider overnight journeys to save on accommodation
    • Always have backup plans and emergency contacts
    • Research visa requirements early
    • Pack light - you'll thank yourself later!
    """)
