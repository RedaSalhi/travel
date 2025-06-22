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
        'total_budget': 0,
        'spent': 0,
        'categories': {}
    }

def main():
    st.title("🎒 Backpacking Trip Planner")
    st.markdown("Plan your adventure day by day with transport, accommodation, and budget tracking!")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a section:", 
                                ["Trip Overview", "Day-by-Day Planning", "Budget Calculator", "Trip Summary"])
    
    if page == "Trip Overview":
        trip_overview()
    elif page == "Day-by-Day Planning":
        day_by_day_planning()
    elif page == "Budget Calculator":
        budget_calculator()
    elif page == "Trip Summary":
        trip_summary()

def trip_overview():
    st.header("🌍 Trip Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trip_name = st.text_input("Trip Name", placeholder="e.g., Southeast Asia Adventure")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        
    with col2:
        destinations = st.text_area("Main Destinations", 
                                   placeholder="List your main destinations...")
        total_budget = st.number_input("Total Budget ($)", min_value=0, value=1000)
        st.session_state.budget_data['total_budget'] = total_budget
    
    if st.button("Save Trip Overview"):
        st.success("Trip overview saved!")

def day_by_day_planning():
    st.header("📅 Day-by-Day Planning")
    
    # Add new day
    if st.button("➕ Add New Day"):
        new_day = {
            'day': len(st.session_state.trip_data) + 1,
            'date': '',
            'location': '',
            'transport_type': 'Bus',
            'transport_from': '',
            'transport_to': '',
            'transport_time': '',
            'transport_cost': 0,
            'accommodation_type': 'Hostel',
            'accommodation_name': '',
            'accommodation_cost': 0,
            'notes': ''
        }
        st.session_state.trip_data.append(new_day)
        st.rerun()
    
    # Display existing days
    for i, day_data in enumerate(st.session_state.trip_data):
        with st.expander(f"Day {day_data['day']} - {day_data.get('location', 'Location TBD')}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🚌 Transport")
                transport_type = st.selectbox(
                    "Transport Type", 
                    ["Bus", "Bus (overnight)", "Train", "Train (overnight)", "Plane", "Car", "Walking", "Boat"],
                    key=f"transport_type_{i}",
                    index=["Bus", "Bus (overnight)", "Train", "Train (overnight)", "Plane", "Car", "Walking", "Boat"].index(day_data.get('transport_type', 'Bus'))
                )
                
                transport_from = st.text_input("From", key=f"transport_from_{i}", value=day_data.get('transport_from', ''))
                transport_to = st.text_input("To", key=f"transport_to_{i}", value=day_data.get('transport_to', ''))
                transport_time = st.text_input("Departure Time", key=f"transport_time_{i}", value=day_data.get('transport_time', ''))
                transport_cost = st.number_input("Transport Cost ($)", key=f"transport_cost_{i}", value=day_data.get('transport_cost', 0), min_value=0.0)
                
            with col2:
                st.subheader("🏨 Accommodation")
                accommodation_type = st.selectbox(
                    "Accommodation Type",
                    ["Hostel", "Hotel", "Guesthouse", "Camping", "Bus (sleeping)", "Train (sleeping)", "Airbnb", "Couchsurfing", "Friend's place", "None"],
                    key=f"accommodation_type_{i}",
                    index=["Hostel", "Hotel", "Guesthouse", "Camping", "Bus (sleeping)", "Train (sleeping)", "Airbnb", "Couchsurfing", "Friend's place", "None"].index(day_data.get('accommodation_type', 'Hostel'))
                )
                
                accommodation_name = st.text_input("Accommodation Name", key=f"accommodation_name_{i}", value=day_data.get('accommodation_name', ''))
                accommodation_cost = st.number_input("Accommodation Cost ($)", key=f"accommodation_cost_{i}", value=day_data.get('accommodation_cost', 0), min_value=0.0)
                
                # Show special message for bus/train sleeping
                if accommodation_type in ["Bus (sleeping)", "Train (sleeping)"]:
                    st.info("💡 You'll be sleeping on transport - no separate accommodation needed!")
            
            # General info
            date = st.date_input("Date", key=f"date_{i}")
            location = st.text_input("Location/City", key=f"location_{i}", value=day_data.get('location', ''))
            notes = st.text_area("Notes", key=f"notes_{i}", value=day_data.get('notes', ''))
            
            # Update session state
            st.session_state.trip_data[i].update({
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
            
            # Delete day button
            if st.button(f"🗑️ Delete Day {day_data['day']}", key=f"delete_{i}"):
                st.session_state.trip_data.pop(i)
                # Renumber remaining days
                for j, remaining_day in enumerate(st.session_state.trip_data):
                    remaining_day['day'] = j + 1
                st.rerun()

def budget_calculator():
    st.header("💰 Budget Calculator")
    
    if not st.session_state.trip_data:
        st.warning("Add some days in the Day-by-Day Planning section first!")
        return
    
    # Calculate totals from trip data
    total_transport = sum(day.get('transport_cost', 0) for day in st.session_state.trip_data)
    total_accommodation = sum(day.get('accommodation_cost', 0) for day in st.session_state.trip_data)
    
    # Additional expenses
    st.subheader("Additional Expenses")
    col1, col2 = st.columns(2)
    
    with col1:
        food_budget = st.number_input("Food Budget ($)", min_value=0.0, value=0.0)
        activities_budget = st.number_input("Activities Budget ($)", min_value=0.0, value=0.0)
        
    with col2:
        shopping_budget = st.number_input("Shopping Budget ($)", min_value=0.0, value=0.0)
        emergency_budget = st.number_input("Emergency Fund ($)", min_value=0.0, value=0.0)
    
    # Calculate totals
    total_planned = total_transport + total_accommodation + food_budget + activities_budget + shopping_budget + emergency_budget
    total_budget = st.session_state.budget_data['total_budget']
    remaining = total_budget - total_planned
    
    # Display budget summary
    st.subheader("Budget Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Budget", f"${total_budget:,.2f}")
    with col2:
        st.metric("Planned Expenses", f"${total_planned:,.2f}")
    with col3:
        color = "normal" if remaining >= 0 else "inverse"
        st.metric("Remaining", f"${remaining:,.2f}", delta=None)
    with col4:
        percentage = (total_planned / total_budget * 100) if total_budget > 0 else 0
        st.metric("Budget Used", f"{percentage:.1f}%")
    
    # Budget breakdown chart
    if total_planned > 0:
        budget_breakdown = {
            'Transport': total_transport,
            'Accommodation': total_accommodation,
            'Food': food_budget,
            'Activities': activities_budget,
            'Shopping': shopping_budget,
            'Emergency': emergency_budget
        }
        
        # Remove zero values
        budget_breakdown = {k: v for k, v in budget_breakdown.items() if v > 0}
        
        if budget_breakdown:
            fig = px.pie(
                values=list(budget_breakdown.values()),
                names=list(budget_breakdown.keys()),
                title="Budget Breakdown"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Daily budget tracker
    st.subheader("Daily Expenses Tracker")
    if st.session_state.trip_data:
        df = pd.DataFrame(st.session_state.trip_data)
        df['total_daily_cost'] = df['transport_cost'] + df['accommodation_cost']
        
        fig = px.bar(
            df, 
            x='day', 
            y='total_daily_cost',
            title="Daily Expenses (Transport + Accommodation)",
            labels={'day': 'Day', 'total_daily_cost': 'Cost ($)'}
        )
        st.plotly_chart(fig, use_container_width=True)

def trip_summary():
    st.header("📋 Trip Summary")
    
    if not st.session_state.trip_data:
        st.warning("No trip data available. Start planning in the Day-by-Day section!")
        return
    
    # Trip statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Days", len(st.session_state.trip_data))
    with col2:
        total_transport_cost = sum(day.get('transport_cost', 0) for day in st.session_state.trip_data)
        st.metric("Transport Cost", f"${total_transport_cost:,.2f}")
    with col3:
        total_accommodation_cost = sum(day.get('accommodation_cost', 0) for day in st.session_state.trip_data)
        st.metric("Accommodation Cost", f"${total_accommodation_cost:,.2f}")
    
    # Detailed itinerary
    st.subheader("Detailed Itinerary")
    
    for day in st.session_state.trip_data:
        with st.container():
            st.markdown(f"### Day {day['day']} - {day.get('location', 'TBD')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🚌 Transport:**")
                if day.get('transport_from') and day.get('transport_to'):
                    st.write(f"• {day['transport_type']}: {day['transport_from']} → {day['transport_to']}")
                    if day.get('transport_time'):
                        st.write(f"• Departure: {day['transport_time']}")
                    st.write(f"• Cost: ${day.get('transport_cost', 0):.2f}")
                else:
                    st.write("Transport details to be added")
                    
            with col2:
                st.markdown("**🏨 Accommodation:**")
                if day['accommodation_type'] in ["Bus (sleeping)", "Train (sleeping)"]:
                    st.write(f"• Sleeping on {day['accommodation_type'].lower()}")
                elif day.get('accommodation_name'):
                    st.write(f"• {day['accommodation_type']}: {day['accommodation_name']}")
                    st.write(f"• Cost: ${day.get('accommodation_cost', 0):.2f}")
                else:
                    st.write("Accommodation details to be added")
            
            if day.get('notes'):
                st.markdown(f"**📝 Notes:** {day['notes']}")
            
            st.markdown("---")
    
    # Export functionality
    st.subheader("📤 Export Trip Data")
    if st.button("Download as CSV"):
        df = pd.DataFrame(st.session_state.trip_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📁 Download CSV",
            data=csv,
            file_name="backpacking_trip_plan.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
