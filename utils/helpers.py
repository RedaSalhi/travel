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


def generate_trip_insights(trip_data: List[Dict[
