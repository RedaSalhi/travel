"""
Helper functions for the Backpacking Trip Planner
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


def calculate_suggested_budget(travel_style: str, days: int) -> float:
    """
    Calculate suggested budget based on travel style and duration
    
    Args:
        travel_style: The travel style selected by user
        days: Number of days for the trip
        
    Returns:
        Suggested budget amount
    """
    daily_rates = {
        "Budget Backpacker": (25, 40),
        "Mid-range Explorer": (40, 70),
        "Comfort Traveller": (70, 120)
    }
    
    # Extract style key from full string
    style_key = travel_style.split('(')[0].strip()
    
    if style_key in daily_rates:
        low, high = daily_rates[style_key]
        return (low + high) / 2 * days
    
    return 50 * days  # Default fallback


def calculate_day_completion(day_data: Dict[str, Any]) -> float:
    """
    Calculate completion percentage for a day's planning
    
    Args:
        day_data: Dictionary containing day information
        
    Returns:
        Completion percentage (0.0 to 1.0)
    """
    required_fields = ['location', 'transport_from', 'transport_to', 'accommodation_type']
    optional_fields = ['date', 'transport_time', 'accommodation_name', 'notes']
    
    # Required fields (70% weight)
    required_completed = sum(1 for field in required_fields if day_data.get(field))
    required_score = (required_completed / len(required_fields)) * 0.7
    
    # Optional fields (30% weight)  
    optional_completed = sum(1 for field in optional_fields if day_data.get(field))
    optional_score = (optional_completed / len(optional_fields)) * 0.3
    
    return required_score + optional_score


def get_transport_emoji(transport_type: str) -> str:
    """Get emoji for transport type"""
    emoji_map = {
        'Bus': '🚌',
        'Bus (overnight)': '🚌',
        'Train': '🚂',
        'Train (overnight)': '🚂',
        'Plane': '✈️',
        'Ferry': '⛴️',
        'Car/Taxi': '🚗',
        'Walking': '🚶',
        'Local Transport': '🚊',
        'Cycling': '🚴'
    }
    return emoji_map.get(transport_type, '🚌')


def get_accommodation_emoji(accommodation_type: str) -> str:
    """Get emoji for accommodation type"""
    emoji_map = {
        'Hostel': '🏠',
        'Hotel': '🏨',
        'Guesthouse': '🏡',
        'Camping': '⛺',
        'Bus (sleeping)': '🚌',
        'Train (sleeping)': '🚂',
        'Airbnb': '🏠',
        'Couchsurfing': '🛋️',
        "Friend's place": '👥',
        'None (transit day)': '🚶'
    }
    return emoji_map.get(accommodation_type, '🏠')


def format_currency(amount: float, currency: str = 'GBP') -> str:
    """
    Format currency amount
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    symbols = {
        'GBP': '£',
        'USD': '$',
        'EUR': '€'
    }
    
    symbol = symbols.get(currency, '£')
    return f"{symbol}{amount:.2f}"


def calculate_trip_statistics(trip_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate comprehensive trip statistics
    
    Args:
        trip_data: List of day data dictionaries
        
    Returns:
        Dictionary with trip statistics
    """
    if not trip_data:
        return {}
    
    # Basic stats
    total_days = len(trip_data)
    total_transport_cost = sum(day.get('transport_cost', 0.0) for day in trip_data)
    total_accommodation_cost = sum(day.get('accommodation_cost', 0.0) for day in trip_data)
    total_cost = total_transport_cost + total_accommodation_cost
    
    # Transport analysis
    transport_counts = {}
    transport_costs = {}
    for day in trip_data:
        transport = day.get('transport_type', 'Unknown')
        transport_counts[transport] = transport_counts.get(transport, 0) + 1
        transport_costs[transport] = transport_costs.get(transport, 0) + day.get('transport_cost', 0)
    
    # Accommodation analysis
    accommodation_counts = {}
    accommodation_costs = {}
    for day in trip_data:
        accommodation = day.get('accommodation_type', 'Unknown')
        accommodation_counts[accommodation] = accommodation_counts.get(accommodation, 0) + 1
        accommodation_costs[accommodation] = accommodation_costs.get(accommodation, 0) + day.get('accommodation_cost', 0)
    
    # Completion analysis
    completed_days = sum(1 for day in trip_data if calculate_day_completion(day) >= 0.8)
    completion_rate = completed_days / total_days
    
    return {
        'total_days': total_days,
        'total_cost': total_cost,
        'total_transport_cost': total_transport_cost,
        'total_accommodation_cost': total_accommodation_cost,
        'average_daily_cost': total_cost / total_days,
        'transport_counts': transport_counts,
        'transport_costs': transport_costs,
        'accommodation_counts': accommodation_counts,
        'accommodation_costs': accommodation_costs,
        'completed_days': completed_days,
        'completion_rate': completion_rate,
        'missing_locations': sum(1 for day in trip_data if not day.get('location')),
        'missing_transport': sum(1 for day in trip_data if not day.get('transport_from'))
    }


def validate_day_data(day_data: Dict[str, Any]) -> List[str]:
    """
    Validate day data and return list of issues
    
    Args:
        day_data: Day data dictionary
        
    Returns:
        List of validation error messages
    """
    issues = []
    
    if not day_data.get('location'):
        issues.append("Location is missing")
    
    if not day_data.get('transport_from') and not day_data.get('transport_to'):
        issues.append("Transport route is incomplete")
    
    if day_data.get('transport_cost', 0) < 0:
        issues.append("Transport cost cannot be negative")
    
    if day_data.get('accommodation_cost', 0) < 0:
        issues.append("Accommodation cost cannot be negative")
    
    # Date validation
    if day_data.get('date'):
        try:
            pd.to_datetime(day_data['date'])
        except:
            issues.append("Invalid date format")
    
    return issues


def generate_trip_insights(trip_data: List[Dict[str, Any]], budget_data: Dict[str, Any]) -> List[str]:
    """
    Generate insights and recommendations for the trip
    
    Args:
        trip_data: List of day data dictionaries
        budget_data: Budget information dictionary
        
    Returns:
        List of insight strings
    """
    insights = []
    
    if not trip_data:
        return ["Start planning your trip to get personalized insights!"]
    
    stats = calculate_trip_statistics(trip_data)
    
    # Budget insights
    total_budget = budget_data.get('total_budget', 0)
    if total_budget > 0:
        budget_usage = (stats['total_cost'] / total_budget) * 100
        
        if budget_usage > 100:
            insights.append(f"⚠️ You're {budget_usage-100:.1f}% over budget. Consider reducing costs.")
        elif budget_usage > 80:
            insights.append(f"🔶 You're using {budget_usage:.1f}% of your budget. Budget carefully for remaining items.")
        else:
            insights.append(f"✅ Great! You're using {budget_usage:.1f}% of your budget with room for extras.")
    
    # Transport insights
    if stats['transport_counts']:
        most_used_transport = max(stats['transport_counts'], key=stats['transport_counts'].get)
        insights.append(f"🚌 You're mainly using {most_used_transport} for transport ({stats['transport_counts'][most_used_transport]} times).")
        
        if 'Bus (overnight)' in stats['transport_counts'] or 'Train (overnight)' in stats['transport_counts']:
            overnight_count = stats['transport_counts'].get('Bus (overnight)', 0) + stats['transport_counts'].get('Train (overnight)', 0)
            savings = overnight_count * 25  # Estimated accommodation savings
            insights.append(f"💡 Smart choice! Overnight transport saves you approximately £{savings} on accommodation.")
    
    # Accommodation insights
    if stats['accommodation_counts']:
        if stats['accommodation_counts'].get('Hostel', 0) > stats['total_days'] * 0.7:
            insights.append("🏠 You're staying mostly in hostels - great for meeting other travelers!")
        
        camping_nights = stats['accommodation_counts'].get('Camping', 0)
        if camping_nights > 0:
            savings = camping_nights * 30  # Estimated savings vs hotels
            insights.append(f"⛺ Camping {camping_nights} nights could save you around £{savings}!")
    
    # Cost insights
    if stats['average_daily_cost'] > 0:
        if stats['average_daily_cost'] < 30:
            insights.append(f"💰 Your daily average of £{stats['average_daily_cost']:.0f} is very budget-friendly!")
        elif stats['average_daily_cost'] < 50:
            insights.append(f"💰 Your daily average of £{stats['average_daily_cost']:.0f} is reasonable for backpacking.")
        else:
            insights.append(f"💰 Your daily average of £{stats['average_daily_cost']:.0f} is on the higher side - consider budget alternatives.")
    
    # Completion insights
    if stats['completion_rate'] < 0.5:
        insights.append(f"📝 Your trip is {stats['completion_rate']:.1%} complete. Keep adding details for better planning!")
    elif stats['completion_rate'] < 0.8:
        insights.append(f"📝 Your trip is {stats['completion_rate']:.1%} complete. You're making good progress!")
    else:
        insights.append(f"📝 Your trip is {stats['completion_rate']:.1%} complete. Almost ready for adventure!")
    
    # Duration insights
    if stats['total_days'] > 0:
        if stats['total_days'] < 7:
            insights.append("⏰ A short but sweet adventure! Perfect for a quick getaway.")
        elif stats['total_days'] < 14:
            insights.append("⏰ Two weeks of adventure - ideal for exploring a region thoroughly!")
        elif stats['total_days'] < 30:
            insights.append("⏰ A month-long journey - plenty of time for deep exploration!")
        else:
            insights.append("⏰ An epic long-term adventure! Don't forget to pace yourself.")
    
    return insights


def export_to_dataframe(trip_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Convert trip data to pandas DataFrame for analysis
    
    Args:
        trip_data: List of day data dictionaries
        
    Returns:
        Pandas DataFrame with trip data
    """
    if not trip_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(trip_data)
    
    # Ensure numeric columns
    df['transport_cost'] = pd.to_numeric(df['transport_cost'], errors='coerce').fillna(0)
    df['accommodation_cost'] = pd.to_numeric(df['accommodation_cost'], errors='coerce').fillna(0)
    
    # Add calculated columns
    df['total_daily_cost'] = df['transport_cost'] + df['accommodation_cost']
    df['cumulative_cost'] = df['total_daily_cost'].cumsum()
    
    # Add completion percentage
    df['completion_percentage'] = df.apply(lambda row: calculate_day_completion(row.to_dict()), axis=1)
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    return df


def get_budget_recommendations(trip_data: List[Dict[str, Any]], budget_data: Dict[str, Any]) -> List[str]:
    """
    Generate budget recommendations based on current planning
    
    Args:
        trip_data: List of day data dictionaries
        budget_data: Budget information dictionary
        
    Returns:
        List of budget recommendation strings
    """
    recommendations = []
    
    if not trip_data:
        return ["Plan your itinerary first to get budget recommendations!"]
    
    stats = calculate_trip_statistics(trip_data)
    total_budget = budget_data.get('total_budget', 0)
    
    if total_budget <= 0:
        recommendations.append("💰 Set a total budget to get personalized recommendations!")
        return recommendations
    
    current_spending = stats['total_cost']
    remaining_budget = total_budget - current_spending
    
    # Basic budget status
    if remaining_budget < 0:
        recommendations.append(f"⚠️ Over budget by £{abs(remaining_budget):.2f}. Consider these cost-cutting measures:")
        recommendations.append("• Switch to overnight transport to save on accommodation")
        recommendations.append("• Choose hostels over hotels")
        recommendations.append("• Look for free walking tours and activities")
        recommendations.append("• Cook your own meals when possible")
    
    # Category-specific recommendations
    if stats['total_transport_cost'] > total_budget * 0.4:
        recommendations.append("🚌 Transport costs are high (>40% of budget). Consider:")
        recommendations.append("• Booking buses instead of flights")
        recommendations.append("• Using rail passes for multiple train journeys")
        recommendations.append("• Choosing overnight journeys")
    
    if stats['total_accommodation_cost'] > total_budget * 0.4:
        recommendations.append("🏨 Accommodation costs are high (>40% of budget). Consider:")
        recommendations.append("• Staying in hostels with shared rooms")
        recommendations.append("• Trying Couchsurfing or house-sitting")
        recommendations.append("• Camping where possible")
        recommendations.append("• Looking for work exchanges")
    
    # Emergency fund recommendations
    if not budget_data.get('emergency_budget', 0):
        emergency_amount = total_budget * 0.1
        recommendations.append(f"🛡️ Consider setting aside £{emergency_amount:.2f} (10% of budget) for emergencies")
    
    # Daily spending recommendations
    remaining_days = len([day for day in trip_data if not day.get('accommodation_cost')])
    if remaining_days > 0 and remaining_budget > 0:
        suggested_daily = remaining_budget / remaining_days
        recommendations.append(f"📅 For remaining {remaining_days} days, budget approximately £{suggested_daily:.2f} per day")
    
    return recommendations


def save_trip_info(trip_info: Dict[str, Any]) -> bool:
    """
    Save trip information (placeholder for future database integration)
    
    Args:
        trip_info: Trip information dictionary
        
    Returns:
        Success status
    """
    # This would integrate with a database in a full application
    # For now, it's just stored in session state
    return True


def load_trip_info() -> Dict[str, Any]:
    """
    Load trip information (placeholder for future database integration)
    
    Returns:
        Trip information dictionary
    """
    # This would load from a database in a full application
    # For now, return empty dict
    return {}


def validate_trip_dates(start_date: str, end_date: str) -> List[str]:
    """
    Validate trip dates
    
    Args:
        start_date: Start date string
        end_date: End date string
        
    Returns:
        List of validation errors
    """
    errors = []
    
    try:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        if start >= end:
            errors.append("End date must be after start date")
        
        if start < pd.Timestamp.now().date():
            errors.append("Start date should not be in the past")
        
        trip_length = (end - start).days
        if trip_length > 365:
            errors.append("Trip length cannot exceed 365 days")
        
    except Exception as e:
        errors.append("Invalid date format")
    
    return errors
