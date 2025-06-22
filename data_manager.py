import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class DataManager:
    """Simplified data manager for the trip planner"""
    
    def __init__(self, data_file: str = "trip_data.json"):
        """Initialize data manager with JSON file path"""
        self.data_file = data_file
        
    def save_data(self, trip_data: List[Dict], budget_data: Dict, trip_info: Dict) -> bool:
        """Save all trip data to JSON file with error handling"""
        try:
            # Prepare data structure
            data_to_save = {
                "trip_data": trip_data,
                "budget_data": budget_data,
                "trip_info": self._serialize_trip_info(trip_info),
                "last_saved": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            # Write to JSON file with proper encoding
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False, default=str)
            
            return True
            
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self) -> Optional[Dict[str, Any]]:
        """Load trip data from JSON file with error handling"""
        try:
            if not os.path.exists(self.data_file):
                return None
            
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Deserialize trip_info dates
            if "trip_info" in data:
                data["trip_info"] = self._deserialize_trip_info(data["trip_info"])
            
            return data
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def backup_data(self) -> bool:
        """Create a timestamped backup of current data"""
        try:
            if not os.path.exists(self.data_file):
                return False
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"trip_data_backup_{timestamp}.json"
            
            # Copy current file to backup
            with open(self.data_file, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            
            return True
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def data_exists(self) -> bool:
        """Check if saved data file exists"""
        return os.path.exists(self.data_file)
    
    def get_last_saved(self) -> Optional[str]:
        """Get the last saved timestamp"""
        data = self.load_data()
        if data and "last_saved" in data:
            return data["last_saved"]
        return None
    
    def _serialize_trip_info(self, trip_info: Dict) -> Dict:
        """Convert date objects to strings for JSON serialization"""
        if not trip_info:
            return {}
            
        serialized = trip_info.copy()
        
        # Handle start_date
        if "start_date" in serialized and serialized["start_date"]:
            try:
                if hasattr(serialized["start_date"], 'isoformat'):
                    serialized["start_date"] = serialized["start_date"].isoformat()
                else:
                    serialized["start_date"] = str(serialized["start_date"])
            except Exception:
                serialized["start_date"] = None
        
        # Handle end_date
        if "end_date" in serialized and serialized["end_date"]:
            try:
                if hasattr(serialized["end_date"], 'isoformat'):
                    serialized["end_date"] = serialized["end_date"].isoformat()
                else:
                    serialized["end_date"] = str(serialized["end_date"])
            except Exception:
                serialized["end_date"] = None
        
        return serialized
    
    def _deserialize_trip_info(self, trip_info: Dict) -> Dict:
        """Convert date strings back to date objects"""
        if not trip_info:
            return {}
            
        deserialized = trip_info.copy()
        
        # Handle start_date
        if "start_date" in deserialized and deserialized["start_date"]:
            try:
                deserialized["start_date"] = datetime.fromisoformat(deserialized["start_date"]).date()
            except (ValueError, TypeError, AttributeError):
                deserialized["start_date"] = None
        
        # Handle end_date
        if "end_date" in deserialized and deserialized["end_date"]:
            try:
                deserialized["end_date"] = datetime.fromisoformat(deserialized["end_date"]).date()
            except (ValueError, TypeError, AttributeError):
                deserialized["end_date"] = None
        
        return deserialized

# Convenience functions for direct use
def save_trip_data(trip_data: List[Dict], budget_data: Dict, trip_info: Dict) -> bool:
    """Save trip data using default data manager"""
    dm = DataManager()
    return dm.save_data(trip_data, budget_data, trip_info)

def load_trip_data() -> Optional[Dict[str, Any]]:
    """Load trip data using default data manager"""
    dm = DataManager()
    return dm.load_data()

def auto_save(trip_data: List[Dict], budget_data: Dict, trip_info: Dict) -> None:
    """Auto-save function for Streamlit callbacks with error handling"""
    try:
        save_trip_data(trip_data, budget_data, trip_info)
    except Exception as e:
        print(f"Auto-save failed: {e}")

def initialize_from_saved_data():
    """Initialize session state from saved data if it exists"""
    try:
        saved_data = load_trip_data()
        if saved_data:
            return {
                'trip_data': saved_data.get('trip_data', []),
                'budget_data': saved_data.get('budget_data', {}),
                'trip_info': saved_data.get('trip_info', {}),
                'last_saved': saved_data.get('last_saved')
            }
    except Exception as e:
        print(f"Error initializing from saved data: {e}")
    
    return None

def clear_saved_data() -> bool:
    """Clear saved data file"""
    try:
        if os.path.exists("trip_data.json"):
            os.remove("trip_data.json")
            return True
        return False
    except Exception as e:
        print(f"Error clearing saved data: {e}")
        return False
