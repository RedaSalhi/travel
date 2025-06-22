import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class DataManager:
    def __init__(self, data_file: str = "trip_data.json"):
        """Initialize data manager with JSON file path"""
        self.data_file = data_file
        
    def save_data(self, trip_data: List[Dict], budget_data: Dict, trip_info: Dict) -> bool:
        """Save all trip data to JSON file"""
        try:
            # Prepare data structure
            data_to_save = {
                "trip_data": trip_data,
                "budget_data": budget_data,
                "trip_info": self._serialize_trip_info(trip_info),
                "last_saved": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            # Write to JSON file
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self) -> Optional[Dict[str, Any]]:
        """Load trip data from JSON file"""
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
        serialized = trip_info.copy()
        
        # Convert date objects to ISO format strings
        if "start_date" in serialized and serialized["start_date"]:
            if hasattr(serialized["start_date"], 'isoformat'):
                serialized["start_date"] = serialized["start_date"].isoformat()
        
        if "end_date" in serialized and serialized["end_date"]:
            if hasattr(serialized["end_date"], 'isoformat'):
                serialized["end_date"] = serialized["end_date"].isoformat()
        
        return serialized
    
    def _deserialize_trip_info(self, trip_info: Dict) -> Dict:
        """Convert date strings back to date objects"""
        deserialized = trip_info.copy()
        
        # Convert ISO format strings back to date objects
        if "start_date" in deserialized and deserialized["start_date"]:
            try:
                deserialized["start_date"] = datetime.fromisoformat(deserialized["start_date"]).date()
            except (ValueError, TypeError):
                deserialized["start_date"] = None
        
        if "end_date" in deserialized and deserialized["end_date"]:
            try:
                deserialized["end_date"] = datetime.fromisoformat(deserialized["end_date"]).date()
            except (ValueError, TypeError):
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
    """Auto-save function for Streamlit callbacks"""
    try:
        save_trip_data(trip_data, budget_data, trip_info)
    except Exception as e:
        print(f"Auto-save failed: {e}")

def initialize_from_saved_data():
    """Initialize session state from saved data if it exists"""
    saved_data = load_trip_data()
    if saved_data:
        return {
            'trip_data': saved_data.get('trip_data', []),
            'budget_data': saved_data.get('budget_data', {}),
            'trip_info': saved_data.get('trip_info', {}),
            'last_saved': saved_data.get('last_saved')
        }
    return None
