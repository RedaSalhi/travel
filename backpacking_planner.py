import streamlit as st
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

# Initialize session state
if 'trip_data' not in st.session_state:
    st.session_state.trip_data = []
if 'budget_data' not in st.session_state:
    st.session_state.budget_data = {
        'total_budget': 1000.0,
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
    st.title("🎒 Backpacking Trip Planner")
    st.markdown("Plan your adventure day by day with transport, accommodation, and budget tracking!")
    
    # Sidebar for navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox("Choose a section:", 
                                ["🌍 Trip Overview", "📅 Day-by-Day Planning", "💰 Budget Calculator", "📋 Trip Summary"])
    
    # Quick stats in sidebar
    if st.session_state.trip_data:
        st.sidebar.markdown("### 📊 Quick Stats")
        total_days = len(st.session_state.trip_data)
        total_cost = sum(day.get('transport_cost', 0.0) + day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
        st.sidebar.metric("Days Planned", total_days)
        st.sidebar.metric("Total Cost", f"${total_cost:.2f}")
        
        budget = st.session_state.budget_data['total_budget']
        remaining = budget - total_cost
        st.sidebar.metric("Budget Remaining", f"${remaining:.2f}", 
                         delta=f"{((remaining/budget)*100):.1f}% left" if budget > 0 else "")
    
    if page == "🌍 Trip Overview":
        trip_overview()
    elif page == "📅 Day-by-Day Planning":
        day_by_day_planning()
    elif page == "💰 Budget Calculator":
        budget_calculator()
    elif page == "📋 Trip Summary":
        trip_summary()

def trip_overview():
    st.header("🌍 Trip Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trip_name = st.text_input("Trip Name", 
                                 value=st.session_state.trip_info['name'],
                                 placeholder="e.g., Southeast Asia Adventure")
        start_date = st.date_input("Start Date", 
                                  value=st.session_state.trip_info['start_date'])
        end_date = st.date_input("End Date", 
                                value=st.session_state.trip_info['end_date'])
        
    with col2:
        destinations = st.text_area("Main Destinations", 
                                   value=st.session_state.trip_info['destinations'],
                                   placeholder="List your main destinations...")
        total_budget = st.number_input("Total Budget ($)", 
                                      min_value=0.0, 
                                      value=st.session_state.budget_data['total_budget'],
                                      step=50.0)
    
    # Travel style preferences
    st.subheader("🎯 Travel Preferences")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        travel_style = st.selectbox("Travel Style", 
                                   ["Budget Backpacker", "Mid-range Explorer", "Comfort Traveler"])
    with col2:
        group_size = st.number_input("Group Size", min_value=1, max_value=20, value=1)
    with col3:
        transport_preference = st.selectbox("Preferred Transport", 
                                          ["Bus", "Train", "Mix of Both", "Flights when needed"])
    
    if st.button("💾 Save Trip Overview", type="primary"):
        st.session_state.trip_info.update({
            'name': trip_name,
            'start_date': start_date,
            'end_date': end_date,
            'destinations': destinations
        })
        st.session_state.budget_data['total_budget'] = total_budget
        st.success("✅ Trip overview saved!")
        
        # Auto-suggest days based on date range
        if start_date and end_date and end_date > start_date:
            suggested_days = (end_date - start_date).days
            if suggested_days > len(st.session_state.trip_data):
                st.info(f"💡 Based on your dates, you might want to plan {suggested_days} days. Go to Day-by-Day Planning to add more days!")

def day_by_day_planning():
    st.header("📅 Day-by-Day Planning")
    
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
        st.info("👆 Start by adding your first day!")
        return
    
    # Display existing days with better organization
    for i, day_data in enumerate(st.session_state.trip_data):
        day_cost = day_data.get('transport_cost', 0.0) + day_data.get('accommodation_cost', 0.0)
        
        with st.expander(f"📍 Day {day_data['day']} - {day_data.get('location', 'Location TBD')} | ${day_cost:.2f}", 
                        expanded=i == len(st.session_state.trip_data) - 1):  # Expand last added day
            
            # Date and location
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Date", key=f"date_{i}", 
                                   help="When will you be in this location?")
            with col2:
                location = st.text_input("Location/City", key=f"location_{i}", 
                                       value=day_data.get('location', ''),
                                       placeholder="e.g., Bangkok, Thailand")
            
            # Transport and accommodation sections
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🚌 Transport")
                transport_type = st.selectbox(
                    "Transport Type", 
                    ["Bus", "Bus (overnight)", "Train", "Train (overnight)", "Plane", "Ferry", "Car/Taxi", "Walking", "Local Transport"],
                    key=f"transport_type_{i}",
                    index=get_transport_index(day_data.get('transport_type', 'Bus'))
                )
                
                transport_from = st.text_input("From", key=f"transport_from_{i}", 
                                             value=day_data.get('transport_from', ''),
                                             placeholder="Departure location")
                transport_to = st.text_input("To", key=f"transport_to_{i}", 
                                           value=day_data.get('transport_to', ''),
                                           placeholder="Arrival location")
                
                col_time, col_cost = st.columns(2)
                with col_time:
                    transport_time = st.text_input("Time", key=f"transport_time_{i}", 
                                                 value=day_data.get('transport_time', ''),
                                                 placeholder="09:30")
                with col_cost:
                    transport_cost = st.number_input("Cost ($)", key=f"transport_cost_{i}", 
                                                   value=float(day_data.get('transport_cost', 0.0)), 
                                                   min_value=0.0, step=1.0)
                
            with col2:
                st.markdown("### 🏨 Accommodation")
                accommodation_type = st.selectbox(
                    "Accommodation Type",
                    ["Hostel", "Hotel", "Guesthouse", "Camping", "Bus (sleeping)", "Train (sleeping)", 
                     "Airbnb", "Couchsurfing", "Friend's place", "None (transit day)"],
                    key=f"accommodation_type_{i}",
                    index=get_accommodation_index(day_data.get('accommodation_type', 'Hostel'))
                )
                
                # Show different inputs based on accommodation type
                if accommodation_type in ["Bus (sleeping)", "Train (sleeping)"]:
                    st.success("💤 Sleeping on transport - no accommodation cost!")
                    accommodation_name = ""
                    accommodation_cost = 0.0
                elif accommodation_type == "None (transit day)":
                    st.info("🚶 Transit day - no accommodation needed")
                    accommodation_name = ""
                    accommodation_cost = 0.0
                else:
                    accommodation_name = st.text_input("Name/Address", key=f"accommodation_name_{i}", 
                                                     value=day_data.get('accommodation_name', ''),
                                                     placeholder="Hotel/Hostel name")
                    accommodation_cost = st.number_input("Cost ($)", key=f"accommodation_cost_{i}", 
                                                       value=float(day_data.get('accommodation_cost', 0.0)), 
                                                       min_value=0.0, step=1.0)
            
            # Notes and additional info
            notes = st.text_area("📝 Notes & Activities", key=f"notes_{i}", 
                               value=day_data.get('notes', ''),
                               placeholder="Things to do, restaurants to try, important info...")
            
            # Action buttons
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
    st.header("💰 Budget Calculator & Tracker")
    
    if not st.session_state.trip_data:
        st.warning("⚠️ Add some days in the Day-by-Day Planning section first!")
        st.info("👆 Go to the Day-by-Day Planning tab to start adding your itinerary")
        return
    
    # Calculate totals from trip data
    total_transport = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
    total_accommodation = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
    
    # Budget categories
    st.subheader("💳 Additional Budget Categories")
    col1, col2 = st.columns(2)
    
    with col1:
        food_budget = st.number_input("Food Budget ($)", min_value=0.0, value=0.0, step=10.0,
                                    help="Daily meals, snacks, drinks")
        activities_budget = st.number_input("Activities & Tours ($)", min_value=0.0, value=0.0, step=10.0,
                                          help="Excursions, museums, entertainment")
        
    with col2:
        shopping_budget = st.number_input("Shopping & Souvenirs ($)", min_value=0.0, value=0.0, step=10.0,
                                        help="Gifts, clothes, souvenirs")
        emergency_budget = st.number_input("Emergency Fund ($)", min_value=0.0, value=0.0, step=10.0,
                                         help="Unexpected expenses, medical")
    
    # Insurance and visas
    col1, col2 = st.columns(2)
    with col1:
        insurance_cost = st.number_input("Travel Insurance ($)", min_value=0.0, value=0.0, step=5.0)
    with col2:
        visa_costs = st.number_input("Visas & Documents ($)", min_value=0.0, value=0.0, step=5.0)
    
    # Calculate totals
    additional_costs = food_budget + activities_budget + shopping_budget + emergency_budget + insurance_cost + visa_costs
    total_planned = total_transport + total_accommodation + additional_costs
    total_budget = st.session_state.budget_data['total_budget']
    remaining = total_budget - total_planned
    
    # Display budget summary with metrics
    st.subheader("📊 Budget Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Budget", f"${total_budget:,.2f}")
    with col2:
        st.metric("📝 Planned Expenses", f"${total_planned:,.2f}")
    with col3:
        color = "normal" if remaining >= 0 else "inverse"
        st.metric("💸 Remaining", f"${remaining:,.2f}", 
                 delta=f"${remaining:.2f}" if remaining >= 0 else f"-${abs(remaining):.2f}")
    with col4:
        percentage = (total_planned / total_budget * 100) if total_budget > 0 else 0
        st.metric("📈 Budget Used", f"{percentage:.1f}%")
    
    # Budget status
    if remaining < 0:
        st.error(f"⚠️ You're over budget by ${abs(remaining):,.2f}!")
    elif remaining < total_budget * 0.1:
        st.warning("🔶 You're close to your budget limit!")
    else:
        st.success("✅ You're within budget!")
    
    # Detailed breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget breakdown pie chart
        if total_planned > 0:
            budget_breakdown = {
                'Transport': total_transport,
                'Accommodation': total_accommodation,
                'Food': food_budget,
                'Activities': activities_budget,
                'Shopping': shopping_budget,
                'Emergency': emergency_budget,
                'Insurance': insurance_cost,
                'Visas': visa_costs
            }
            
            # Remove zero values
            budget_breakdown = {k: v for k, v in budget_breakdown.items() if v > 0}
            
            if budget_breakdown:
                fig = px.pie(
                    values=list(budget_breakdown.values()),
                    names=list(budget_breakdown.keys()),
                    title="💰 Budget Breakdown",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Daily expenses chart
        if st.session_state.trip_data:
            df = pd.DataFrame(st.session_state.trip_data)
            df['total_daily_cost'] = df['transport_cost'].astype(float) + df['accommodation_cost'].astype(float)
            df['day_label'] = df['day'].astype(str) + ' - ' + df['location'].fillna('TBD')
            
            fig = px.bar(
                df, 
                x='day', 
                y='total_daily_cost',
                title="📈 Daily Expenses (Transport + Accommodation)",
                labels={'day': 'Day', 'total_daily_cost': 'Cost ($)'},
                color='total_daily_cost',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Budget recommendations
    if total_planned > 0:
        st.subheader("💡 Budget Tips")
        avg_daily_cost = total_planned / len(st.session_state.trip_data) if st.session_state.trip_data else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📊 Average daily cost: ${avg_daily_cost:.2f}")
            if avg_daily_cost > 100:
                st.warning("💰 High daily average - consider budget accommodations or local transport")
        
        with col2:
            transport_percent = (total_transport / total_planned * 100) if total_planned > 0 else 0
            st.info(f"🚌 Transport is {transport_percent:.1f}% of your budget")
            if transport_percent > 40:
                st.warning("🚌 Transport costs are high - look for overnight buses/trains to save on accommodation")

def trip_summary():
    st.header("📋 Trip Summary & Export")
    
    if not st.session_state.trip_data:
        st.warning("⚠️ No trip data available. Start planning in the Day-by-Day section!")
        return
    
    # Trip overview
    trip_name = st.session_state.trip_info.get('name', 'My Backpacking Trip')
    st.subheader(f"🌍 {trip_name}")
    
    # Trip statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📅 Total Days", len(st.session_state.trip_data))
    with col2:
        total_transport_cost = sum(day.get('transport_cost', 0.0) for day in st.session_state.trip_data)
        st.metric("🚌 Transport Cost", f"${total_transport_cost:.2f}")
    with col3:
        total_accommodation_cost = sum(day.get('accommodation_cost', 0.0) for day in st.session_state.trip_data)
        st.metric("🏨 Accommodation Cost", f"${total_accommodation_cost:.2f}")
    with col4:
        total_cost = total_transport_cost + total_accommodation_cost
        st.metric("💰 Total Cost", f"${total_cost:.2f}")
    
    # Detailed itinerary
    st.subheader("🗓️ Detailed Itinerary")
    
    for day in st.session_state.trip_data:
        with st.container():
            # Day header with cost
            day_cost = day.get('transport_cost', 0.0) + day.get('accommodation_cost', 0.0)
            st.markdown(f"### 📍 Day {day['day']} - {day.get('location', 'TBD')} | ${day_cost:.2f}")
            
            if day.get('date'):
                st.markdown(f"**📅 Date:** {day['date']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🚌 Transport:**")
                if day.get('transport_from') and day.get('transport_to'):
                    st.write(f"• **Route:** {day['transport_from']} → {day['transport_to']}")
                    st.write(f"• **Type:** {day.get('transport_type', 'TBD')}")
                    if day.get('transport_time'):
                        st.write(f"• **Time:** {day['transport_time']}")
                    st.write(f"• **Cost:** ${day.get('transport_cost', 0):.2f}")
                else:
                    st.write("• Transport details to be added")
                    
            with col2:
                st.markdown("**🏨 Accommodation:**")
                acc_type = day.get('accommodation_type', 'TBD')
                if acc_type in ["Bus (sleeping)", "Train (sleeping)"]:
                    st.write(f"• **Type:** Sleeping on {acc_type.replace(' (sleeping)', '').lower()}")
                    st.write("• **Cost:** Included in transport")
                elif acc_type == "None (transit day)":
                    st.write("• **Type:** Transit day - no accommodation")
                elif day.get('accommodation_name'):
                    st.write(f"• **Type:** {acc_type}")
                    st.write(f"• **Name:** {day['accommodation_name']}")
                    st.write(f"• **Cost:** ${day.get('accommodation_cost', 0):.2f}")
                else:
                    st.write("• Accommodation details to be added")
            
            if day.get('notes'):
                st.markdown(f"**📝 Notes:** {day['notes']}")
            
            st.markdown("---")
    
    # Export functionality
    st.subheader("📤 Export & Share")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📁 Download CSV", type="primary"):
            df = pd.DataFrame(st.session_state.trip_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="💾 Download Trip Data",
                data=csv,
                file_name=f"{trip_name.replace(' ', '_')}_itinerary.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Copy Itinerary"):
            itinerary_text = generate_text_itinerary()
            st.code(itinerary_text, language="text")
            st.success("✅ Itinerary text generated above - copy and paste as needed!")
    
    with col3:
        if st.button("🎯 Trip Statistics"):
            show_trip_statistics()

# Helper functions
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
    transport_types = ["Bus", "Bus (overnight)", "Train", "Train (overnight)", "Plane", "Ferry", "Car/Taxi", "Walking", "Local Transport"]
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
    trip_name = st.session_state.trip_info.get('name', 'My Backpacking Trip')
    text = f"{trip_name}\n{'='*len(trip_name)}\n\n"
    
    for day in st.session_state.trip_data:
        text += f"Day {day['day']} - {day.get('location', 'TBD')}\n"
        text += f"Date: {day.get('date', 'TBD')}\n"
        text += f"Transport: {day.get('transport_type', 'TBD')} from {day.get('transport_from', 'TBD')} to {day.get('transport_to', 'TBD')}\n"
        text += f"Accommodation: {day.get('accommodation_type', 'TBD')} - {day.get('accommodation_name', 'TBD')}\n"
        if day.get('notes'):
            text += f"Notes: {day['notes']}\n"
        text += f"Cost: ${day.get('transport_cost', 0) + day.get('accommodation_cost', 0):.2f}\n\n"
    
    return text

def show_trip_statistics():
    st.subheader("📊 Trip Statistics")
    
    if not st.session_state.trip_data:
        return
    
    # Transport statistics
    transport_counts = {}
    for day in st.session_state.trip_data:
        transport = day.get('transport_type', 'Unknown')
        transport_counts[transport] = transport_counts.get(transport, 0) + 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚌 Transport Breakdown:**")
        for transport, count in transport_counts.items():
            st.write(f"• {transport}: {count} day{'s' if count != 1 else ''}")
    
    with col2:
        # Accommodation statistics
        accommodation_counts = {}
        for day in st.session_state.trip_data:
            accommodation = day.get('accommodation_type', 'Unknown')
            accommodation_counts[accommodation] = accommodation_counts.get(accommodation, 0) + 1
        
        st.markdown("**🏨 Accommodation Breakdown:**")
        for accommodation, count in accommodation_counts.items():
            st.write(f"• {accommodation}: {count} night{'s' if count != 1 else ''}")

if __name__ == "__main__":
    main()
