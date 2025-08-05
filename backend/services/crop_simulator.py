from datetime import datetime, timedelta
from typing import Dict, List
import random
import math

class CropGrowthSimulator:
    def __init__(self):
        self.growth_factors = {
            "temperature": {"optimal": (26, 30), "weight": 0.25},
            "humidity": {"optimal": (70, 85), "weight": 0.15},
            "soil_moisture": {"optimal": (70, 90), "weight": 0.30},
            "ph_level": {"optimal": (6.0, 7.0), "weight": 0.15},
            "rainfall": {"optimal": (10, 30), "weight": 0.15}
        }
    
    def calculate_growth_rate(self, sensor_data: List[Dict], crop_type: str) -> float:
        """Calculate crop growth rate based on environmental conditions"""
        if not sensor_data:
            return 1.0  # Default growth rate
        
        # Get recent data (last 7 days)
        recent_data = sensor_data[-168:]  # Assuming hourly data
        
        if not recent_data:
            return 1.0
        
        # Calculate average conditions
        avg_conditions = {
            "temperature": sum(d["temperature"] for d in recent_data) / len(recent_data),
            "humidity": sum(d["humidity"] for d in recent_data) / len(recent_data),
            "soil_moisture": sum(d["soil_moisture"] for d in recent_data) / len(recent_data),
            "ph_level": sum(d["ph_level"] for d in recent_data) / len(recent_data),
            "rainfall": sum(d["rainfall"] for d in recent_data)
        }
        
        # Calculate growth factor for each parameter
        total_factor = 0
        total_weight = 0
        
        for param, config in self.growth_factors.items():
            value = avg_conditions[param]
            optimal_min, optimal_max = config["optimal"]
            weight = config["weight"]
            
            if optimal_min <= value <= optimal_max:
                factor = 1.0  # Optimal conditions
            else:
                # Calculate penalty for deviation from optimal
                if value < optimal_min:
                    deviation = (optimal_min - value) / optimal_min
                else:
                    deviation = (value - optimal_max) / optimal_max
                
                factor = max(0.1, 1.0 - deviation * 0.5)  # Penalty, minimum 0.1
            
            total_factor += factor * weight
            total_weight += weight
        
        growth_rate = total_factor / total_weight if total_weight > 0 else 1.0
        
        # Add crop-specific modifiers
        crop_modifiers = {
            "rice": 1.0,
            "palm_oil": 0.8,  # Slower growth
            "rubber": 0.6,    # Very slow growth
            "durian": 1.2,    # Faster fruit development
            "banana": 1.1,    # Good growth rate
            "coconut": 0.7    # Slow growth
        }
        
        growth_rate *= crop_modifiers.get(crop_type, 1.0)
        
        return max(0.1, min(2.0, growth_rate))  # Clamp between 0.1 and 2.0
    
    def update_crop_progress(self, crop_data: Dict, growth_rate: float) -> Dict:
        """Update crop growth progress"""
        planted_date = datetime.fromisoformat(crop_data["planted_date"])
        days_since_planted = (datetime.now() - planted_date).days
        
        # Apply growth rate to progress
        actual_progress = days_since_planted * growth_rate
        
        # Determine growth stage based on progress
        crop_type = crop_data["type"]
        stage_thresholds = self.get_stage_thresholds(crop_type)
        
        current_stage = "seedling"
        for stage, threshold in stage_thresholds.items():
            if actual_progress >= threshold:
                current_stage = stage
        
        # Update yield estimate based on growth conditions
        base_yield = crop_data["yield_estimate"]
        if growth_rate > 1.2:
            yield_modifier = 1.1  # Bonus for excellent conditions
        elif growth_rate < 0.8:
            yield_modifier = 0.9  # Penalty for poor conditions
        else:
            yield_modifier = 1.0
        
        updated_yield = base_yield * yield_modifier
        
        # Calculate new expected harvest date
        total_cycle_days = self.get_cycle_days(crop_type)
        remaining_days = (total_cycle_days - actual_progress) / growth_rate
        expected_harvest = datetime.now() + timedelta(days=remaining_days)
        
        return {
            **crop_data,
            "growth_stage": current_stage,
            "growth_progress": min(100, (actual_progress / total_cycle_days) * 100),
            "growth_rate": round(growth_rate, 2),
            "yield_estimate": round(updated_yield, 0),
            "expected_harvest": expected_harvest.isoformat(),
            "last_growth_update": datetime.now().isoformat()
        }
    
    def get_stage_thresholds(self, crop_type: str) -> Dict[str, int]:
        """Get growth stage thresholds in days for different crops"""
        thresholds = {
            "rice": {
                "seedling": 0, "tillering": 30, "panicle_initiation": 60,
                "flowering": 90, "grain_filling": 105, "maturity": 120
            },
            "palm_oil": {
                "nursery": 0, "immature": 90, "young_mature": 180,
                "prime_mature": 270, "old_mature": 300
            },
            "rubber": {
                "immature": 0, "young_tapping": 120, "peak_production": 240, "declining": 300
            },
            "durian": {
                "flowering": 0, "fruit_set": 30, "fruit_development": 90,
                "ripening": 120, "harvest": 150
            },
            "banana": {
                "sucker": 0, "vegetative": 60, "flowering": 180,
                "bunch_development": 240, "harvest": 300
            },
            "coconut": {
                "seedling": 0, "juvenile": 90, "flowering": 180,
                "bearing": 270, "mature": 365
            }
        }
        return thresholds.get(crop_type, thresholds["rice"])
    
    def get_cycle_days(self, crop_type: str) -> int:
        """Get total growth cycle days for crop"""
        cycles = {
            "rice": 120, "palm_oil": 365, "rubber": 365,
            "durian": 150, "banana": 300, "coconut": 365
        }
        return cycles.get(crop_type, 120)