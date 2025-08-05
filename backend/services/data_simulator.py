import random
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import math

class MalaysianFarmSimulator:
    def __init__(self):
        # Malaysian weather patterns by season
        self.weather_patterns = {
            "dry_season": {
                "months": [6, 7, 8, 9],  # June-September
                "temp_range": (26, 35),
                "humidity_range": (60, 80),
                "rainfall_range": (0, 15),
                "soil_moisture_modifier": -10
            },
            "wet_season": {
                "months": [10, 11, 12, 1, 2, 3],  # October-March
                "temp_range": (24, 32),
                "humidity_range": (70, 95),
                "rainfall_range": (10, 80),
                "soil_moisture_modifier": +15
            },
            "transition": {
                "months": [4, 5],  # April-May
                "temp_range": (25, 33),
                "humidity_range": (65, 85),
                "rainfall_range": (5, 40),
                "soil_moisture_modifier": 0
            }
        }
        
        # Malaysian crop data
        self.crop_data = {
            "rice": {
                "varieties": ["MR220", "MR219", "MR297", "Bario", "Fragrant Rice"],
                "growth_stages": ["seedling", "tillering", "panicle_initiation", "flowering", "grain_filling", "maturity"],
                "growth_cycle_days": 120,
                "yield_range": (3000, 7000),  # kg/hectare
                "optimal_ph": (5.5, 7.0),
                "optimal_moisture": (80, 95),
                "optimal_temp": (26, 32)
            },
            "palm_oil": {
                "varieties": ["Dura", "Pisifera", "Tenera", "MPOB Yangambi", "FELDA"],
                "growth_stages": ["nursery", "immature", "young_mature", "prime_mature", "old_mature"],
                "growth_cycle_days": 365,
                "yield_range": (15000, 25000),  # kg/hectare/year
                "optimal_ph": (4.5, 6.5),
                "optimal_moisture": (60, 80),
                "optimal_temp": (24, 28)
            },
            "rubber": {
                "varieties": ["RRIM 600", "RRIM 2020", "RRIM 3001", "PB 260", "GT 1"],
                "growth_stages": ["immature", "young_tapping", "peak_production", "declining"],
                "growth_cycle_days": 365,
                "yield_range": (1200, 2500),  # kg/hectare/year
                "optimal_ph": (4.5, 6.0),
                "optimal_moisture": (70, 85),
                "optimal_temp": (24, 30)
            },
            "durian": {
                "varieties": ["Musang King", "D24", "Red Prawn", "IOI", "Tekka"],
                "growth_stages": ["flowering", "fruit_set", "fruit_development", "ripening", "harvest"],
                "growth_cycle_days": 150,
                "yield_range": (8000, 15000),  # kg/hectare
                "optimal_ph": (6.0, 7.5),
                "optimal_moisture": (70, 90),
                "optimal_temp": (26, 32)
            },
            "banana": {
                "varieties": ["Cavendish", "Pisang Mas", "Pisang Raja", "Berangan", "Rastali"],
                "growth_stages": ["sucker", "vegetative", "flowering", "bunch_development", "harvest"],
                "growth_cycle_days": 300,
                "yield_range": (20000, 40000),  # kg/hectare
                "optimal_ph": (5.5, 7.0),
                "optimal_moisture": (75, 85),
                "optimal_temp": (26, 30)
            },
            "coconut": {
                "varieties": ["Malayan Dwarf", "Malayan Tall", "MATAG", "MAWA", "Hybrid"],
                "growth_stages": ["seedling", "juvenile", "flowering", "bearing", "mature"],
                "growth_cycle_days": 365,
                "yield_range": (6000, 12000),  # kg/hectare/year
                "optimal_ph": (5.2, 8.0),
                "optimal_moisture": (60, 80),
                "optimal_temp": (27, 32)
            }
        }
        
        # Malaysian states with coordinates
        self.farm_locations = [
            {"state": "Kedah", "name": "Kedah Rice Bowl", "lat": 6.1254, "lng": 100.3673, "primary_crop": "rice"},
            {"state": "Johor", "name": "Johor Palm Estate", "lat": 1.4927, "lng": 103.7414, "primary_crop": "palm_oil"},
            {"state": "Perak", "name": "Perak Rubber Plantation", "lat": 4.5921, "lng": 101.0901, "primary_crop": "rubber"},
            {"state": "Pahang", "name": "Pahang Durian Orchard", "lat": 3.8126, "lng": 103.3256, "primary_crop": "durian"},
            {"state": "Negeri Sembilan", "name": "NS Mixed Farm", "lat": 2.7297, "lng": 101.9381, "primary_crop": "banana"},
            {"state": "Terengganu", "name": "Terengganu Coconut Farm", "lat": 5.3117, "lng": 103.1324, "primary_crop": "coconut"},
            {"state": "Selangor", "name": "Selangor Agro Park", "lat": 3.0738, "lng": 101.5183, "primary_crop": "rice"},
            {"state": "Melaka", "name": "Melaka Heritage Farm", "lat": 2.1896, "lng": 102.2501, "primary_crop": "durian"}
        ]
        
        # Equipment types with Malaysian focus
        self.equipment_types = {
            "irrigation": ["Drip System", "Sprinkler System", "Flood Irrigation", "Smart Irrigation"],
            "tractor": ["Kubota M7040", "John Deere 5E", "Massey Ferguson 385", "New Holland TD5"],
            "harvester": ["Rice Harvester", "Palm Oil Harvester", "Multi-crop Harvester"],
            "drone": ["DJI Agras", "Yamaha RMAX", "AgEagle RX60", "PrecisionHawk Lancaster"],
            "sensor": ["Weather Station", "Soil Sensor", "Crop Monitor", "Water Level Sensor"]
        }
    
    def get_current_season(self) -> str:
        """Determine current season based on Malaysian weather patterns"""
        month = datetime.now().month
        for season, data in self.weather_patterns.items():
            if month in data["months"]:
                return season
        return "transition"
    
    def generate_weather_data(self, base_location: Dict, time_offset_hours: int = 0) -> Dict:
        """Generate realistic weather data for Malaysian conditions"""
        season = self.get_current_season()
        weather = self.weather_patterns[season]
        
        # Add time-based variations
        current_time = datetime.now() + timedelta(hours=time_offset_hours)
        hour = current_time.hour
        
        # Diurnal temperature variation
        temp_base = random.uniform(*weather["temp_range"])
        if 6 <= hour <= 18:  # Daytime
            temp_modifier = math.sin(math.pi * (hour - 6) / 12) * 3
        else:  # Nighttime
            temp_modifier = -random.uniform(2, 5)
        
        temperature = round(temp_base + temp_modifier, 1)
        
        # Humidity inverse relationship with temperature
        humidity_base = random.uniform(*weather["humidity_range"])
        humidity = round(max(50, humidity_base - (temperature - 27) * 2), 1)
        
        # Rainfall with seasonal patterns
        rainfall_chance = 0.3 if season == "dry_season" else 0.7
        if random.random() < rainfall_chance:
            rainfall = round(random.uniform(*weather["rainfall_range"]), 1)
        else:
            rainfall = 0.0
        
        # Light intensity based on time and weather
        if 6 <= hour <= 18:
            base_light = 50000 + (hour - 12) ** 2 * (-2000)  # Peak at noon
            if rainfall > 10:
                base_light *= 0.3  # Cloudy/rainy conditions
        else:
            base_light = random.uniform(0, 100)  # Night/artificial lighting
        
        return {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
            "light_intensity": round(max(0, base_light), 0),
            "season": season,
            "time": current_time.isoformat()
        }
    
    def generate_soil_data(self, crop_type: str, weather_data: Dict) -> Dict:
        """Generate soil data based on crop requirements and weather"""
        crop_info = self.crop_data.get(crop_type, self.crop_data["rice"])
        
        # Base soil moisture affected by rainfall and season
        moisture_base = random.uniform(*crop_info["optimal_moisture"])
        if weather_data["rainfall"] > 20:
            moisture_modifier = random.uniform(5, 15)
        elif weather_data["rainfall"] == 0:
            moisture_modifier = random.uniform(-10, -5)
        else:
            moisture_modifier = random.uniform(-2, 5)
        
        # Add seasonal modifier
        season_modifier = self.weather_patterns[weather_data["season"]]["soil_moisture_modifier"]
        soil_moisture = round(max(20, min(100, moisture_base + moisture_modifier + season_modifier)), 1)
        
        # pH level with some variation
        ph_range = crop_info["optimal_ph"]
        ph_level = round(random.uniform(ph_range[0] - 0.5, ph_range[1] + 0.5), 1)
        
        # Nutrient levels (NPK)
        nitrogen = round(random.uniform(20, 80), 1)  # mg/kg
        phosphorus = round(random.uniform(10, 50), 1)  # mg/kg
        potassium = round(random.uniform(100, 300), 1)  # mg/kg
        
        return {
            "soil_moisture": soil_moisture,
            "ph_level": ph_level,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "organic_matter": round(random.uniform(2.0, 8.0), 1)  # percentage
        }
    
    def generate_sensor_reading(self, sensor_id: str, plot_info: Dict, time_offset_hours: int = 0) -> Dict:
        """Generate complete sensor reading"""
        crop_type = plot_info.get("crop_type", "rice")
        location = plot_info.get("location", {"lat": 4.2105, "lng": 101.9758})
        
        weather_data = self.generate_weather_data(location, time_offset_hours)
        soil_data = self.generate_soil_data(crop_type, weather_data)
        
        return {
            "sensor_id": sensor_id,
            "timestamp": weather_data["time"],
            "plot_id": plot_info.get("plot_id", "unknown"),
            "location": location,
            
            # Weather data
            "temperature": weather_data["temperature"],
            "humidity": weather_data["humidity"],
            "rainfall": weather_data["rainfall"],
            "light_intensity": weather_data["light_intensity"],
            
            # Soil data
            "soil_moisture": soil_data["soil_moisture"],
            "ph_level": soil_data["ph_level"],
            "nitrogen": soil_data["nitrogen"],
            "phosphorus": soil_data["phosphorus"],
            "potassium": soil_data["potassium"],
            "organic_matter": soil_data["organic_matter"],
            
            # Additional sensors
            "wind_speed": round(random.uniform(0, 15), 1),  # km/h
            "wind_direction": random.randint(0, 360),  # degrees
            "uv_index": random.randint(6, 12),  # High UV in Malaysia
            "co2_level": random.randint(380, 420),  # ppm
            
            # Metadata
            "season": weather_data["season"],
            "data_quality": random.choice(["excellent", "good", "fair"]),
            "battery_level": random.randint(60, 100)  # sensor battery %
        }
    
    def generate_equipment_data(self, equipment_type: str, plot_location: Dict) -> Dict:
        """Generate equipment data"""
        equipment_names = self.equipment_types.get(equipment_type, ["Generic Equipment"])
        
        # Generate location near plot
        lat_offset = random.uniform(-0.002, 0.002)
        lng_offset = random.uniform(-0.002, 0.002)
        
        # Status based on type and random factors
        status_weights = {
            "operational": 0.7,
            "maintenance": 0.15,
            "idle": 0.1,
            "repair": 0.05
        }
        
        status = random.choices(
            list(status_weights.keys()),
            weights=list(status_weights.values())
        )[0]
        
        # Operational hours based on equipment age
        base_hours = random.uniform(100, 3000)
        if status == "repair":
            base_hours += random.uniform(500, 1000)  # Older equipment more likely to need repair
        
        return {
            "id": str(uuid.uuid4()),
            "name": random.choice(equipment_names),
            "type": equipment_type,
            "model": f"{random.choice(['2020', '2021', '2022', '2023'])}-{random.randint(100, 999)}",
            "status": status,
            "location": {
                "lat": plot_location["lat"] + lat_offset,
                "lng": plot_location["lng"] + lng_offset
            },
            "operational_hours": round(base_hours, 1),
            "last_maintenance": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
            "next_maintenance": (datetime.now() + timedelta(days=random.randint(30, 180))).isoformat(),
            "fuel_level": random.randint(20, 100) if equipment_type in ["tractor", "harvester"] else None,
            "efficiency": round(random.uniform(75, 98), 1),  # percentage
            "cost_per_hour": round(random.uniform(50, 200), 2)  # MYR
        }
    
    def generate_crop_data(self, crop_type: str, plot_area: float) -> Dict:
        """Generate detailed crop data"""
        crop_info = self.crop_data[crop_type]
        
        # Random variety
        variety = random.choice(crop_info["varieties"])
        
        # Growth stage progression
        days_since_planted = random.randint(10, crop_info["growth_cycle_days"] - 30)
        total_stages = len(crop_info["growth_stages"])
        stage_duration = crop_info["growth_cycle_days"] / total_stages
        current_stage_index = min(int(days_since_planted / stage_duration), total_stages - 1)
        growth_stage = crop_info["growth_stages"][current_stage_index]
        
        # Yield calculation based on growth progress
        progress_percentage = (days_since_planted / crop_info["growth_cycle_days"]) * 100
        base_yield = random.uniform(*crop_info["yield_range"])
        
        # Yield modifiers based on conditions
        if growth_stage in ["maturity", "harvest", "ripening"]:
            yield_modifier = random.uniform(0.9, 1.1)
        else:
            yield_modifier = random.uniform(0.3, 0.8)
        
        estimated_yield = round(base_yield * yield_modifier * plot_area, 0)
        
        # Dates
        planted_date = datetime.now() - timedelta(days=days_since_planted)
        expected_harvest = planted_date + timedelta(days=crop_info["growth_cycle_days"])
        
        return {
            "id": str(uuid.uuid4()),
            "type": crop_type,
            "variety": variety,
            "planted_date": planted_date.isoformat(),
            "expected_harvest": expected_harvest.isoformat(),
            "growth_stage": growth_stage,
            "growth_progress": round(progress_percentage, 1),
            "yield_estimate": estimated_yield,
            "yield_per_hectare": round(estimated_yield / plot_area, 0),
            "health_status": random.choice(["excellent", "good", "fair", "poor"]),
            "disease_risk": random.choice(["low", "medium", "high"]),
            "pest_pressure": random.choice(["minimal", "moderate", "high"]),
            "irrigation_needs": random.choice(["low", "medium", "high"]),
            "fertilizer_last_applied": (datetime.now() - timedelta(days=random.randint(7, 60))).isoformat(),
            "pesticide_last_applied": (datetime.now() - timedelta(days=random.randint(14, 90))).isoformat()
        }
    
    def generate_complete_farm(self, farm_location: Dict = None) -> Dict:
        """Generate a complete farm with all components"""
        if not farm_location:
            farm_location = random.choice(self.farm_locations)
        
        farm_id = str(uuid.uuid4())
        
        # Generate plots (3-8 plots per farm)
        num_plots = random.randint(3, 8)
        plots = []
        total_area = 0
        
        for i in range(num_plots):
            plot_area = round(random.uniform(0.5, 5.0), 2)  # hectares
            total_area += plot_area
            
            # Choose crop type (favor primary crop of the region)
            if random.random() < 0.6:  # 60% chance of primary crop
                crop_type = farm_location["primary_crop"]
            else:
                crop_type = random.choice(list(self.crop_data.keys()))
            
            # Generate plot location near farm center
            plot_lat = farm_location["lat"] + random.uniform(-0.01, 0.01)
            plot_lng = farm_location["lng"] + random.uniform(-0.01, 0.01)
            plot_location = {"lat": plot_lat, "lng": plot_lng}
            
            # Generate sensors (2-5 per plot)
            num_sensors = random.randint(2, 5)
            sensors = [str(uuid.uuid4()) for _ in range(num_sensors)]
            
            # Generate equipment (1-4 per plot)
            num_equipment = random.randint(1, 4)
            equipment = []
            for _ in range(num_equipment):
                eq_type = random.choice(list(self.equipment_types.keys()))
                equipment.append(self.generate_equipment_data(eq_type, plot_location))
            
            # Generate crop data
            crop_data = self.generate_crop_data(crop_type, plot_area)
            
            # Plot status based on crop and equipment status
            equipment_statuses = [eq["status"] for eq in equipment]
            if "repair" in equipment_statuses:
                plot_status = "maintenance"
            elif crop_data["growth_stage"] in ["harvest", "maturity", "ripening"]:
                plot_status = "harvesting"
            elif random.random() < 0.8:
                plot_status = "active"
            else:
                plot_status = "idle"
            
            plot = {
                "id": str(uuid.uuid4()),
                "name": f"Plot {i+1} - {crop_type.title().replace('_', ' ')}",
                "location": plot_location,
                "area": plot_area,
                "status": plot_status,
                "crop": crop_data,
                "equipment": equipment,
                "sensors": sensors,
                "irrigation_status": random.choice([True, False]),
                "soil_type": random.choice(["clay", "loam", "sandy", "peat", "alluvial"]),
                "drainage": random.choice(["excellent", "good", "moderate", "poor"]),
                "slope": round(random.uniform(0, 15), 1),  # degrees
                "elevation": random.randint(5, 200),  # meters above sea level
                "last_updated": datetime.now().isoformat(),
                "created_date": (datetime.now() - timedelta(days=random.randint(30, 1000))).isoformat()
            }
            plots.append(plot)
        
        # Farm metadata
        established_years_ago = random.randint(3, 25)
        established_date = datetime.now() - timedelta(days=established_years_ago * 365)
        
        farm_data = {
            "id": farm_id,
            "name": farm_location["name"],
            "location": f"{farm_location['state']}, Malaysia",
            "coordinates": {"lat": farm_location["lat"], "lng": farm_location["lng"]},
            "owner": random.choice([
                "Malaysian Agricultural Cooperative",
                "Federal Land Development Authority (FELDA)",
                "Sime Darby Plantation",
                "IOI Corporation",
                "Private Smallholder Cooperative"
            ]),
            "total_area": round(total_area, 2),
            "plots": plots,
            "established_date": established_date.isoformat(),
            "farm_type": random.choice(["commercial", "smallholder", "cooperative", "estate"]),
            "certification": random.choice(["RSPO", "MyGAP", "Organic", "None"]),
            "labor_force": random.randint(5, 50),
            "annual_revenue": round(random.uniform(100000, 2000000), 2),  # MYR
            "contact": {
                "phone": f"+60{random.randint(10000000, 99999999)}",
                "email": f"info@{farm_location['name'].lower().replace(' ', '')}.com.my"
            }
        }
        
        return farm_data
    
    def generate_historical_sensor_data(self, sensor_ids: List[str], plot_info: Dict, days: int = 30) -> List[Dict]:
        """Generate historical sensor data for the past N days"""
        historical_data = []
        
        for day in range(days):
            for hour in range(0, 24, 6):  # Every 6 hours
                time_offset = -(days - day) * 24 + hour
                
                for sensor_id in sensor_ids:
                    reading = self.generate_sensor_reading(sensor_id, plot_info, time_offset)
                    historical_data.append(reading)
        
        return historical_data
    
    def simulate_equipment_alerts(self, equipment_list: List[Dict]) -> List[Dict]:
        """Generate equipment alerts and notifications"""
        alerts = []
        
        for equipment in equipment_list:
            # Maintenance alerts
            last_maintenance = datetime.fromisoformat(equipment["last_maintenance"])
            days_since_maintenance = (datetime.now() - last_maintenance).days
            
            if days_since_maintenance > 60:
                alerts.append({
                    "id": str(uuid.uuid4()),
                    "type": "maintenance",
                    "severity": "high" if days_since_maintenance > 90 else "medium",
                    "equipment_id": equipment["id"],
                    "equipment_name": equipment["name"],
                    "message": f"Maintenance overdue by {days_since_maintenance - 60} days",
                    "timestamp": datetime.now().isoformat(),
                    "action_required": "Schedule maintenance"
                })
            
            # Fuel alerts
            if equipment.get("fuel_level") and equipment["fuel_level"] < 25:
                alerts.append({
                    "id": str(uuid.uuid4()),
                    "type": "fuel",
                    "severity": "medium" if equipment["fuel_level"] > 15 else "high",
                    "equipment_id": equipment["id"],
                    "equipment_name": equipment["name"],
                    "message": f"Low fuel level: {equipment['fuel_level']}%",
                    "timestamp": datetime.now().isoformat(),
                    "action_required": "Refuel equipment"
                })
            
            # Efficiency alerts
            if equipment["efficiency"] < 80:
                alerts.append({
                    "id": str(uuid.uuid4()),
                    "type": "efficiency",
                    "severity": "medium",
                    "equipment_id": equipment["id"],
                    "equipment_name": equipment["name"],
                    "message": f"Low efficiency: {equipment['efficiency']}%",
                    "timestamp": datetime.now().isoformat(),
                    "action_required": "Check equipment performance"
                })
        
        return alerts
    
    def generate_weather_forecast(self, location: Dict, days: int = 7) -> List[Dict]:
        """Generate weather forecast for next N days"""
        forecast = []
        
        for day in range(1, days + 1):
            future_date = datetime.now() + timedelta(days=day)
            weather_data = self.generate_weather_data(location, day * 24)
            
            forecast.append({
                "date": future_date.strftime("%Y-%m-%d"),
                "day_name": future_date.strftime("%A"),
                "temperature_min": round(weather_data["temperature"] - random.uniform(3, 8), 1),
                "temperature_max": round(weather_data["temperature"] + random.uniform(2, 6), 1),
                "humidity": weather_data["humidity"],
                "rainfall_probability": random.randint(20, 80),
                "rainfall_amount": weather_data["rainfall"],
                "wind_speed": round(random.uniform(5, 20), 1),
                "uv_index": random.randint(6, 12),
                "conditions": random.choice([
                    "Sunny", "Partly Cloudy", "Cloudy", "Light Rain", 
                    "Heavy Rain", "Thunderstorms", "Hazy"
                ])
            })
        
        return forecast
