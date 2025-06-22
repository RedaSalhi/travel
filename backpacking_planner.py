import streamlit as st
import pandas as pd
import json
import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Backpacking Trip Planner",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# DATABASE & STORAGE SETUP
# ============================================================================

class TripDatabase:
    def __init__(self, db_path="data/trip_planner.db"):
        self.db_path = db_path
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Trips table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                start_date DATE,
                end_date DATE,
                destinations TEXT,
                travel_style TEXT,
                group_size INTEGER,
                total_budget REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Days table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trip_days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER,
                day_number INTEGER,
                date DATE,
                location TEXT,
                transport_type TEXT,
                transport_from TEXT,
                transport_to TEXT,
                transport_time TEXT,
                transport_cost REAL,
                accommodation_type TEXT,
                accommodation_name TEXT,
                accommodation_cost REAL,
                notes TEXT,
                FOREIGN KEY (trip_id) REFERENCES trips (id)
            )
        ''')
        
        # Budget categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER,
                category_name TEXT,
                budgeted_amount REAL,
                spent_amount REAL DEFAULT 0,
                FOREIGN KEY (trip_id) REFERENCES trips (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password):
        """Create a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        user = cursor.fetchone()
        conn.close()
        return user
    
    def save_trip(self, user_id, trip_data, budget_data, days_data):
        """Save complete trip data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Save or update trip
            if trip_data.get('id'):
                cursor.execute('''
                    UPDATE trips SET name=?, start_date=?, end_date=?, destinations=?, 
                    travel_style=?, group_size=?, total_budget=?, updated_at=CURRENT_TIMESTAMP
                    WHERE id=? AND user_id=?
                ''', (
                    trip_data['name'], trip_data.get('start_date'), trip_data.get('end_date'),
                    trip_data.get('destinations'), trip_data.get('travel_style'),
                    trip_data.get('group_size'), budget_data.get('total_budget'),
                    trip_data['id'], user_id
                ))
                trip_id = trip_data['id']
            else:
                cursor.execute('''
                    INSERT INTO trips (user_id, name, start_date, end_date, destinations, 
                    travel_style, group_size, total_budget) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id, trip_data['name'], trip_data.get('start_date'), 
                    trip_data.get('end_date'), trip_data.get('destinations'),
                    trip_data.get('travel_style'), trip_data.get('group_size'),
                    budget_data.get('total_budget')
                ))
                trip_id = cursor.lastrowid
            
            # Clear existing days and budget categories
            cursor.execute("DELETE FROM trip_days WHERE trip_id = ?", (trip_id,))
            cursor.execute("DELETE FROM budget_categories WHERE trip_id = ?", (trip_id,))
            
            # Save days
            for day in days_data:
                cursor.execute('''
                    INSERT INTO trip_days (trip_id, day_number, date, location, transport_type,
                    transport_from, transport_to, transport_time, transport_cost,
                    accommodation_type, accommodation_name, accommodation_cost, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    trip_id, day['day'], day.get('date'), day.get('location'),
                    day.get('transport_type'), day.get('transport_from'), day.get('transport_to'),
                    day.get('transport_time'), day.get('transport_cost'),
                    day.get('accommodation_type'), day.get('accommodation_name'),
                    day.get('accommodation_cost'), day.get('notes')
                ))
            
            # Save budget categories
            for category, amount in budget_data.items():
                if category != 'total_budget' and amount > 0:
                    cursor.execute('''
                        INSERT INTO budget_categories (trip_id, category_name, budgeted_amount)
                        VALUES (?, ?, ?)
                    ''', (trip_id, category, amount))
            
            conn.commit()
            return trip_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_user_trips(self, user_id):
        """Get all trips for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, start_date, end_date, destinations, total_budget, 
                   created_at, updated_at
            FROM trips WHERE user_id = ? ORDER BY updated_at DESC
        ''', (user_id,))
        trips = cursor.fetchall()
        conn.close()
        return trips
    
    def load_trip(self, trip_id, user_id):
        """Load complete trip data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Load trip info
        cursor.execute('''
            SELECT * FROM trips WHERE id = ? AND user_id = ?
        ''', (trip_id, user_id))
        trip = cursor.fetchone()
        
        if not trip:
            conn.close()
            return None, None, None
        
        # Load days
        cursor.execute('''
            SELECT * FROM trip_days WHERE trip_id = ? ORDER BY day_number
        ''', (trip_id,))
        days = cursor.fetchall()
        
        # Load budget categories
        cursor.execute('''
            SELECT category_name, budgeted_amount FROM budget_categories WHERE trip_id = ?
        ''', (trip_id,))
        budget_categories = cursor.fetchall()
        
        conn.close()
        
        # Convert to format expected by app
        trip_info = {
            'id': trip[0],
            'name': trip[2],
            'start_date': pd.to_datetime(trip[3]).date() if trip[3] else None,
            'end_date': pd.to_datetime(trip[4]).date() if trip[4] else None,
            'destinations': trip[5] or '',
            'travel_style': trip[6] or '🎒 Budget Backpacker (£25-40/day)',
            'group_size': trip[7] or 1
        }
        
        budget_data = {'total_budget': trip[8] or 1000.0}
        for category, amount in budget_categories:
            budget_data[category] = amount
        
        days_data = []
        for day in days:
            days_data.append({
                'day': day[2],
                'date': day[3] or '',
                'location': day[4] or '',
                'transport_type': day[5] or 'Bus',
                'transport_from': day[6] or '',
                'transport_to': day[7] or '',
                'transport_time': day[8] or '',
                'transport_cost': day[9] or 0.0,
                'accommodation_type': day[10] or 'Hostel',
                'accommodation_name': day[11] or '',
                'accommodation_cost': day[12] or 0.0,
                'notes': day[13] or ''
            })
        
        return trip_info, budget_data, days_data
    
    def delete_trip(self, trip_id, user_id):
        """Delete a trip and all associated data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verify ownership
        cursor.execute("SELECT id FROM trips WHERE id = ? AND user_id = ?", (trip_id, user_id))
        if not cursor.fetchone():
            conn.close()
            return False
        
        # Delete related data
        cursor.execute("DELETE FROM trip_days WHERE trip_id = ?", (trip_id,))
        cursor.execute("DELETE FROM budget_categories WHERE trip_id = ?", (trip_id,))
        cursor.execute("DELETE FROM trips WHERE id = ?", (trip_id,))
        
        conn.commit()
        conn.close()
        return True

# Initialize database
@st.cache_resource
def get_database():
    return TripDatabase()

db = get_database()

# ============================================================================
# AUTHENTICATION SYSTEM
# ============================================================================

def show_login_page():
    """Display login/register page"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 4rem 2rem; border-radius: 16px; 
                text-align: center; margin-bottom: 2rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">
        <h1 style="margin: 0; font-size: 3.5rem;">🎒 Adventure Planner</h1>
        <p style="margin: 1rem 0 0 0; font-size: 1.3rem;">Your personal backpacking companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Welcome Back!")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if login_button:
                if username and password:
                    user = db.authenticate_user(username, password)
                    if user:
                        st.session_state.user = {
                            'id': user[0],
                            'username': user[1],
                            'email': user[2]
                        }
                        st.success(f"Welcome back, {user[1]}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.subheader("Join the Adventure!")
        with st.form("register_form"):
            new_username = st.text_input("Choose Username")
            new_email = st.text_input("Email Address")
            new_password = st.text_input("Create Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            register_button = st.form_submit_button("Create Account", type="primary", use_container_width=True)
            
            if register_button:
                if new_username and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords don't match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        user_id = db.create_user(new_username, new_email, new_password)
                        if user_id:
                            st.success("Account created successfully! Please login.")
                        else:
                            st.error("Username or email already exists")
                else:
                    st.error("Please fill in all fields")

def show_user_menu():
    """Display user menu in sidebar"""
    if 'user' in st.session_state:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"👤 **{st.session_state.user['username']}**")
        
        if st.sidebar.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def show_trip_manager():
    """Display trip management interface"""
    st.markdown('<h2 style="text-align: center; color: #667eea;">📁 My Trips</h2>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    trips = db.get_user_trips(user_id)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Your Adventures")
    
    with col2:
        if st.button("➕ New Trip", type="primary"):
            # Reset session state for new trip
            st.session_state.trip_data = []
            st.session_state.budget_data = {
                'total_budget': 1000.0,
                'food_budget': 0.0,
                'activities_budget': 0.0,
                'shopping_budget': 0.0,
                'misc_costs': 0.0,
                'emergency_budget': 0.0,
                'insurance_cost': 0.0
            }
            st.session_state.trip_info = {
                'name': '',
                'start_date': None,
                'end_date': None,
                'destinations': '',
                'travel_style': '🎒 Budget Backpacker (£25-40/day)',
                'group_size': 1
            }
            st.session_state.current_view = 'planning'
            st.rerun()
    
    if trips:
        for trip in trips:
            with st.expander(f"🎒 {trip[1]} - {trip[2] or 'No dates'} to {trip[3] or ''}", expanded=False):
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(f"📍 **Destinations:** {trip[4] or 'Not specified'}")
                    st.write(f"💰 **Budget:** £{trip[5] or 0:.0f}")
                
                with col2:
                    st.write(f"📅 **Created:** {trip[6][:10] if trip[6] else 'Unknown'}")
                    st.write(f"🔄 **Updated:** {trip[7][:10] if trip[7] else 'Unknown'}")
                
                with col3:
                    if st.button("📝 Edit", key=f"edit_{trip[0]}"):
                        # Load trip data
                        trip_info, budget_data, days_data = db.load_trip(trip[0], user_id)
                        if trip_info:
                            st.session_state.trip_info = trip_info
                            st.session_state.budget_data = budget_data
                            st.session_state.trip_data = days_data
                            st.session_state.current_view = 'planning'
                            st.rerun()
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{trip[0]}", type="secondary"):
                        if st.session_state.get(f"confirm_delete_{trip[0]}", False):
                            if db.delete_trip(trip[0], user_id):
                                st.success("Trip deleted!")
                                st.rerun()
                        else:
                            st.session_state[f"confirm_delete_{trip[0]}"] = True
                            st.warning("Click again to confirm deletion")
    else:
        st.info("No trips yet. Create your first adventure!")

# ============================================================================
# ENHANCED HELPER FUNCTIONS
# ============================================================================

def calculate_suggested_budget(travel_style: str, days: int) -> float:
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

def calculate_day_completion(day_data: dict) -> float:
    """Calculate completion percentage for a day's planning"""
    required_fields = ['location', 'transport_from', 'transport_to', 'accommodation_type']
    optional_fields = ['date', 'transport_time', 'accommodation_name', 'notes']
    
    required_completed = sum(1 for field in required_fields if day_data.get(field))
    required_score = (required_completed / len(required_fields)) * 0.7
    
    optional_completed = sum(1 for field in optional_fields if day_data.get(field))
    optional_score = (optional_completed / len(optional_fields)) * 0.3
    
    return required_score + optional_score

def save_current_trip():
    """Save current trip to database"""
    if 'user' not in st.session_state:
        return False
    
    user_id = st.session_state.user['id']
    trip_info = st.session_state.trip_info
    budget_data = st.session_state.budget_data
    days_data = st.session_state.trip_data
    
    if not trip_info.get('name'):
        st.error("Please provide a trip name before saving")
        return False
    
    try:
        trip_id = db.save_trip(user_id, trip_info, budget_data, days_data)
        st.session_state.trip_info['id'] = trip_id
        st.success("Trip saved successfully!")
        return True
    except Exception as e:
        st.error(f"Error saving trip: {str(e)}")
        return False

# ============================================================================
# ENHANCED UI COMPONENTS
# ============================================================================

def load_css():
    """Load enhanced CSS with app-like styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        
        --primary: #667eea;
        --secondary: #f5576c;
        --background: #ffffff;
        --surface: #f8fafc;
        --surface-elevated: #ffffff;
        --border: #e2e8f0;
        --text-primary: #1a202c;
        --text-secondary: #4a5568;
        
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        
        --radius-lg: 12px;
        --radius-xl: 16px;
        
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .main .block-container {
        padding: 1rem;
        max-width: 1400px;
        background: var(--background);
    }
    
    .card {
        background: var(--surface-elevated);
        border-radius: var(--radius-lg);
        padding: 2rem;
        border: 1px solid var(--border);
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
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-xl);
    }
    
    .save-indicator {
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--success-gradient);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        box-shadow: var(--shadow-lg);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .trip-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .trip-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION COMPONENTS (Enhanced with auto-save)
# ============================================================================

def init_session_state():
    """Initialize session state with proper structure"""
    if 'trip_data' not in st.session_state:
        st.session_state.trip_data = []
    
    if 'budget_data' not in st.session_state:
        st.session_state.budget_data = {
            'total_budget': 1000.0,
            'food_budget': 0.0,
            'activities_budget': 0.0,
            'shopping_budget': 0.0,
            'misc_costs': 0.0,
            'emergency_budget': 0.0,
            'insurance_cost': 0.0
        }
    
    if 'trip_info' not in st.session_state:
        st.session_state.trip_info = {
            'name': '',
            'start_date': None,
            'end_date': None,
            'destinations': '',
            'travel_style': '🎒 Budget Backpacker (£25-40/day)',
            'group_size': 1
        }
    
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'trips'

def show_auto_save_indicator():
    """Show auto-save status"""
    if st.session_state.get('auto_save_enabled', True):
        if st.session_state.get('last_saved'):
            st.sidebar.success(f"💾 Auto-saved at {st.session_state.last_saved}")
        else:
            st.sidebar.info("💾 Auto-save enabled")

def trip_overview():
    """Enhanced trip overview with auto-save"""
    st.markdown('<h2 style="text-align: center; color: #667eea;">🌍 Trip Overview</h2>', unsafe_allow_html=True)
    
    # Auto-save toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        auto_save = st.checkbox("Auto-save", value=st.session_state.get('auto_save_enabled', True))
        st.session_state.auto_save_enabled = auto_save
    
    # Trip basic information
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
    
    # Save functionality with auto-save
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("💾 Save Trip Overview", type="primary", use_container_width=True, key="save_overview"):
            # Update session state
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
            
            # Save to database
            if save_current_trip():
                st.session_state.last_saved = datetime.now().strftime("%H:%M:%S")
            
            # Auto-suggest days and budget
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
    
    # Auto-save functionality
    if st.session_state.get('auto_save_enabled', True) and trip_name:
        # Auto-save when user stops typing (triggered by any other interaction)
        if trip_name != st.session_state.trip_info.get('name', ''):
            st.session_state.trip_info.update({
                'name': trip_name,
                'start_date': start_date,
                'end_date': end_date,
                'destinations': destinations,
                'travel_style': travel_style,
                'group_size': group_size
            })
            st.session_state.budget_data['total_budget'] = total_budget

def day_by_day_planning():
    """Enhanced day-by-day planning with auto-save"""
    st.markdown('<h2 style="text-align: center; color: #667eea;">📅 Day-by-Day Planning</h2>', unsafe_allow_html=True)
    
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
            if st.session_state.get('auto_save_enabled', True):
                save_current_trip()
            st.rerun()
    
    with col4:
        if st.session_state.trip_data and st.button("🗑️ Clear All", type="secondary"):
            if st.checkbox("Confirm clear all days"):
                st.session_state.trip_data = []
                if st.session_state.get('auto_save_enabled', True):
                    save_current_trip()
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
    
    # Display days with enhanced UI and auto-save
    for i, day_data in enumerate(st.session_state.trip_data):
        day_cost = day_data.get('transport_cost', 0.0) + day_data.get('accommodation_cost', 0.0)
        completion = calculate_day_completion(day_data)
        progress_indicator = "🟢" if completion >= 0.8 else "🟡" if completion >= 0.4 else "🔴"
        
        with st.expander(f"{progress_indicator} Day {day_data['day']} - {day_data.get('location', 'Location TBD')} | £{day_cost:.2f}", 
                        expanded=i == len(st.session_state.trip_data) - 1):
            
            # Enhanced date and location section
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("📅 Date", key=f"date_{i}", 
                                   value=pd.to_datetime(day_data.get('date')).date() if day_data.get('date') else None)
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
                st.markdown('<div style="background: linear-gradient(135deg, #e6f3ff 0%, #cce7ff 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">', unsafe_allow_html=True)
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
                st.markdown('<div style="background: linear-gradient(135deg, #fff0f5 0%, #ffe4e8 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">', unsafe_allow_html=True)
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
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
            with col1:
                if st.button(f"🗑️ Delete", key=f"delete_{i}", type="secondary"):
                    delete_day(i)
            with col2:
                if st.button(f"📋 Copy", key=f"copy_{i}"):
                    copy_day(i)
            with col3:
                if i > 0 and st.button(f"⬆️ Up", key=f"move_up_{i}"):
                    move_day_up(i)
            with col4:
                if st.button(f"💾 Save", key=f"save_day_{i}"):
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
                    if st.session_state.get('auto_save_enabled', True):
                        save_current_trip()
                        st.success("Day saved!")
            with col5:
                completion_percentage = calculate_day_completion(day_data)
                st.progress(completion_percentage, text=f"Completion: {completion_percentage:.0%}")
            
            # Auto-update session state
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
    """Enhanced budget calculator with auto-save"""
    st.markdown('<h2 style="text-align: center; color: #667eea;">💰 Budget Calculator</h2>', unsafe_allow_html=True)
    
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
    
    # Enhanced budget categories with auto-save
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💳 Additional Budget Categories")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🍽️ Daily Expenses**")
        food_budget = st.number_input("Food & Drink (£)", min_value=0.0, 
                                    value=st.session_state.budget_data.get('food_budget', 0.0), step=5.0,
                                    key="food_budget")
        activities_budget = st.number_input("Activities & Attractions (£)", min_value=0.0, 
                                          value=st.session_state.budget_data.get('activities_budget', 0.0), step=5.0,
                                          key="activities_budget")
        
    with col2:
        st.markdown("**🛍️ Shopping & Extras**")
        shopping_budget = st.number_input("Shopping & Souvenirs (£)", min_value=0.0, 
                                        value=st.session_state.budget_data.get('shopping_budget', 0.0), step=5.0,
                                        key="shopping_budget")
        misc_costs = st.number_input("Miscellaneous (£)", min_value=0.0, 
                                   value=st.session_state.budget_data.get('misc_costs', 0.0), step=5.0,
                                   key="misc_costs")
    
    with col3:
        st.markdown("**🛡️ Safety & Security**")
        emergency_budget = st.number_input("Emergency Fund (£)", min_value=0.0, 
                                         value=st.session_state.budget_data.get('emergency_budget', 0.0), step=10.0,
                                         key="emergency_budget")
        insurance_cost = st.number_input("Travel Insurance (£)", min_value=0.0, 
                                       value=st.session_state.budget_data.get('insurance_cost', 0.0), step=5.0,
                                       key="insurance_cost")
    
    # Auto-save budget changes
    if st.button("💾 Save Budget", type="primary"):
        st.session_state.budget_data.update({
            'food_budget': food_budget,
            'activities_budget': activities_budget,
            'shopping_budget': shopping_budget,
            'misc_costs': misc_costs,
            'emergency_budget': emergency_budget,
            'insurance_cost': insurance_cost
        })
        if save_current_trip():
            st.session_state.last_saved = datetime.now().strftime("%H:%M:%S")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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

# ============================================================================
# UTILITY FUNCTIONS (Enhanced)
# ============================================================================

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
    # Auto-save if enabled
    if st.session_state.get('auto_save_enabled', True):
        save_current_trip()
    st.rerun()

def delete_day(index):
    """Delete a day and renumber with auto-save"""
    st.session_state.trip_data.pop(index)
    for j, remaining_day in enumerate(st.session_state.trip_data):
        remaining_day['day'] = j + 1
    # Auto-save if enabled
    if st.session_state.get('auto_save_enabled', True):
        save_current_trip()
    st.rerun()

def copy_day(index):
    """Copy a day with incremented day number and auto-save"""
    original_day = st.session_state.trip_data[index].copy()
    original_day['day'] = len(st.session_state.trip_data) + 1
    original_day['date'] = ''
    st.session_state.trip_data.append(original_day)
    # Auto-save if enabled
    if st.session_state.get('auto_save_enabled', True):
        save_current_trip()
    st.rerun()

def move_day_up(index):
    """Move day up in the list with auto-save"""
    if index > 0:
        st.session_state.trip_data[index], st.session_state.trip_data[index-1] = \
            st.session_state.trip_data[index-1], st.session_state.trip_data[index]
        # Renumber days
        for j, day in enumerate(st.session_state.trip_data):
            day['day'] = j + 1
        # Auto-save if enabled
        if st.session_state.get('auto_save_enabled', True):
            save_current_trip()
        st.rerun()

def update_day_data(index, data):
    """Update day data in session state"""
    if index < len(st.session_state.trip_data):
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

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Enhanced main application with authentication and storage"""
    # Initialize session state
    init_session_state()
    
    # Load CSS
    load_css()
    
    # Check authentication
    if 'user' not in st.session_state:
        show_login_page()
        return
    
    # Show user menu
    show_user_menu()
    show_auto_save_indicator()
    
    # Enhanced header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 3rem 2rem; border-radius: 16px; 
                text-align: center; margin-bottom: 2rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">
        <h1 style="margin: 0; font-size: 3rem;">🎒 Adventure Planner</h1>
        <p style="margin: 1rem 0 0 0; font-size: 1.2rem;">Welcome back, {st.session_state.user['username']}!</p>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">Plan your perfect backpacking journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    if st.session_state.current_view == 'trips':
        show_trip_manager()
    elif st.session_state.current_view == 'planning':
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Back to Trips"):
                st.session_state.current_view = 'trips'
                st.rerun()
        with col3:
            if st.button("💾 Save & Back"):
                if save_current_trip():
                    st.session_state.current_view = 'trips'
                    st.rerun()
        
        # Main planning interface
        tab1, tab2, tab3, tab4 = st.tabs([
            "🌍 Trip Overview", 
            "📅 Day Planning", 
            "💰 Budget Calculator", 
            "📊 Analytics"
        ])
        
        with tab1:
            trip_overview()
        
        with tab2:
            day_by_day_planning()
        
        with tab3:
            budget_calculator()
        
        with tab4:
            if st.session_state.trip_data:
                st.markdown('<h2 style="text-align: center; color: #667eea;">📊 Trip Analytics</h2>', unsafe_allow_html=True)
                
                # Quick analytics
                total_days = len(st.session_state.trip_data)
                total_cost = sum(day.get('transport_cost', 0) + day.get('accommodation_cost', 0) for day in st.session_state.trip_data)
                completed_days = sum(1 for day in st.session_state.trip_data if calculate_day_completion(day) >= 0.8)
                completion_rate = completed_days / total_days if total_days > 0 else 0
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📅 Total Days", total_days)
                with col2:
                    st.metric("💰 Total Cost", f"£{total_cost:.0f}")
                with col3:
                    st.metric("✅ Completed", f"{completed_days}/{total_days}")
                with col4:
                    st.metric("📈 Progress", f"{completion_rate:.1%}")
                
                # Progress bar
                st.progress(completion_rate, text=f"Trip Planning Progress: {completion_rate:.1%}")
                
                # Transport analysis
                if st.session_state.trip_data:
                    transport_stats = {}
                    for day in st.session_state.trip_data:
                        transport = day.get('transport_type', 'Unknown')
                        transport_stats[transport] = transport_stats.get(transport, 0) + 1
                    
                    if transport_stats:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            fig = px.bar(
                                x=list(transport_stats.keys()),
                                y=list(transport_stats.values()),
                                title="🚌 Transport Usage",
                                labels={'x': 'Transport Type', 'y': 'Days'},
                                color=list(transport_stats.values()),
                                color_continuous_scale='Blues'
                            )
                            fig.update_layout(showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            # Cost breakdown
                            daily_costs = [day.get('transport_cost', 0) + day.get('accommodation_cost', 0) 
                                         for day in st.session_state.trip_data]
                            
                            fig = px.line(
                                x=list(range(1, len(daily_costs) + 1)),
                                y=daily_costs,
                                title="💰 Daily Cost Trend",
                                labels={'x': 'Day', 'y': 'Cost (£)'},
                                markers=True
                            )
                            fig.update_traces(line_color='#f5576c', line_width=3)
                            st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Add some days to your trip to see analytics!")
    
    # Enhanced footer
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; text-align: center; padding: 2rem; 
                border-radius: 16px; margin-top: 3rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
        <p style="margin: 0; font-size: 1.1rem;">🎒 Your adventures are safely stored and ready anytime!</p>
        <p style="opacity: 0.8; font-size: 0.9rem; margin-top: 0.5rem;">
            Plan • Save • Explore • Adventure
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
