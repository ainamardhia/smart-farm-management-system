import json
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from .data_simulator import MalaysianFarmSimulator

class FarmService:
    def __init__(self):
        self.data_file = "data/farm_data.json"
        self.sensor_data_file = "data/sensor_data.json"
        self.alerts_file = "data/alerts.json"
        self.forecast_file = "data/weather_forecast.json"
        self.statistics_file = "data/statistics.json"
        self.simulator = MalaysianFarmSimulator()
        self.ensure_data_files()
    
    def ensure_data_files(self):
        """Ensure data files exist and contain initial data"""
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(self.data_file):
            print("🌾 Generating initial farm data...")
            initial_farm = self.simulator.generate_complete_farm()
            self.save_farm_data(initial_farm)
        
        if not os.path.exists(self.sensor_data_file):
            with open(self.sensor_data_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.alerts_file):
            with open(self.alerts_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.forecast_file):
            with open(self.forecast_file, 'w') as f:
                json.dump([], f)
    
    def load_farm_data(self) -> Dict:
        """Load farm data from JSON file"""
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def save_farm_data(self, data: Dict):
        """Save farm data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_farm(self) -> Dict:
        """Get complete farm data"""
        return self.load_farm_data()
    
    def get_plots(self) -> List[Dict]:
        """Get all plots"""
        farm_data = self.load_farm_data()
        return farm_data.get("plots", [])
    
    def get_plot(self, plot_id: str) -> Optional[Dict]:
        """Get specific plot by ID"""
        plots = self.get_plots()
        return next((plot for plot in plots if plot["id"] == plot_id), None)
    
    def update_plot_status(self, plot_id: str, status: str) -> bool:
        """Update plot status"""
        farm_data = self.load_farm_data()
        for plot in farm_data["plots"]:
            if plot["id"] == plot_id:
                plot["status"] = status
                plot["last_updated"] = datetime.now().isoformat()
                self.save_farm_data(farm_data)
                return True
        return False
    
    def toggle_irrigation(self, plot_id: str) -> bool:
        """Toggle irrigation status for a plot"""
        farm_data = self.load_farm_data()
        for plot in farm_data["plots"]:
            if plot["id"] == plot_id:
                plot["irrigation_status"] = not plot["irrigation_status"]
                plot["last_updated"] = datetime.now().isoformat()
                self.save_farm_data(farm_data)
                return True
        return False
    
    def get_sensor_data(self, sensor_id: str = None, limit: int = 100) -> List[Dict]:
        """Get sensor data, optionally filtered by sensor ID"""
        try:
            with open(self.sensor_data_file, 'r') as f:
                all_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        if sensor_id:
            filtered_data = [data for data in all_data if data["sensor_id"] == sensor_id]
            return filtered_data[-limit:]  # Return latest readings
        
        return all_data[-limit:]  # Return latest readings
    
    def generate_live_sensor_data(self) -> List[Dict]:
        """Generate and return live sensor data for all plots"""
        farm_data = self.load_farm_data()
        live_data = []
        
        for plot in farm_data["plots"]:
            plot_info = {
                "plot_id": plot["id"],
                "crop_type": plot["crop"]["type"],
                "location": plot["location"]
            }
            
            for sensor_id in plot["sensors"]:
                sensor_reading = self.simulator.generate_sensor_reading(sensor_id, plot_info)
                live_data.append(sensor_reading)
        
        # Save to file (keep last 1000 readings)
        existing_data = self.get_sensor_data(limit=1000)
        all_data = existing_data + live_data
        if len(all_data) > 1000:
            all_data = all_data[-1000:]
        
        with open(self.sensor_data_file, 'w') as f:
            json.dump(all_data, f, indent=2)
        
        return live_data
    
    def get_alerts(self) -> List[Dict]:
        """Get all alerts"""
        try:
            with open(self.alerts_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def add_alert(self, alert: Dict) -> bool:
        """Add new alert"""
        alerts = self.get_alerts()
        alerts.append(alert)
        
        # Keep only last 100 alerts
        if len(alerts) > 100:
            alerts = alerts[-100:]
        
        with open(self.alerts_file, 'w') as f:
            json.dump(alerts, f, indent=2)
        return True
    
    def get_weather_forecast(self) -> List[Dict]:
        """Get weather forecast"""
        try:
            with open(self.forecast_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def update_weather_forecast(self) -> List[Dict]:
        """Generate and save new weather forecast"""
        farm_data = self.load_farm_data()
        forecast = self.simulator.generate_weather_forecast(farm_data["coordinates"])
        
        with open(self.forecast_file, 'w') as f:
            json.dump(forecast, f, indent=2)
        
        return forecast
    
    def get_statistics(self) -> Dict:
        """Get farm statistics"""
        try:
            with open(self.statistics_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def generate_analytics_report(self) -> Dict:
        """Generate comprehensive analytics report"""
        farm_data = self.load_farm_data()
        sensor_data = self.get_sensor_data(limit=500)
        alerts = self.get_alerts()
        
        # Calculate averages from recent sensor data
        if sensor_data:
            recent_data = [d for d in sensor_data if 
                          (datetime.now() - datetime.fromisoformat(d["timestamp"])).days <= 7]
            
            if recent_data:
                avg_temp = sum(d["temperature"] for d in recent_data) / len(recent_data)
                avg_humidity = sum(d["humidity"] for d in recent_data) / len(recent_data)
                avg_soil_moisture = sum(d["soil_moisture"] for d in recent_data) / len(recent_data)
                total_rainfall = sum(d["rainfall"] for d in recent_data)
            else:
                avg_temp = avg_humidity = avg_soil_moisture = total_rainfall = 0
        else:
            avg_temp = avg_humidity = avg_soil_moisture = total_rainfall = 0
        
        # Equipment status summary
        equipment_summary = {"operational": 0, "maintenance": 0, "idle": 0, "repair": 0}
        total_equipment = 0
        
        for plot in farm_data["plots"]:
            for equipment in plot["equipment"]:
                total_equipment += 1
                status = equipment["status"]
                equipment_summary[status] = equipment_summary.get(status, 0) + 1
        
        # Plot status summary
        plot_summary = {"active": 0, "maintenance": 0, "harvesting": 0, "idle": 0}
        for plot in farm_data["plots"]:
            status = plot["status"]
            plot_summary[status] = plot_summary.get(status, 0) + 1
        
        # Alert severity summary
        alert_summary = {"high": 0, "medium": 0, "low": 0}
        for alert in alerts[-30:]:  # Last 30 alerts
            severity = alert.get("severity", "medium")
            alert_summary[severity] = alert_summary.get(severity, 0) + 1
        
        return {
            "generated_at": datetime.now().isoformat(),
            "farm_overview": {
                "name": farm_data["name"],
                "location": farm_data["location"],
                "total_area": farm_data["total_area"],
                "total_plots": len(farm_data["plots"]),
                "established": farm_data["established_date"]
            },
            "weather_summary": {
                "avg_temperature": round(avg_temp, 1),
                "avg_humidity": round(avg_humidity, 1),
                "avg_soil_moisture": round(avg_soil_moisture, 1),
                "total_rainfall_7days": round(total_rainfall, 1)
            },
            "equipment_status": equipment_summary,
            "plot_status": plot_summary,
            "alert_summary": alert_summary,
            "productivity_metrics": {
                "total_estimated_yield": sum(plot["crop"]["yield_estimate"] for plot in farm_data["plots"]),
                "avg_yield_per_hectare": round(
                    sum(plot["crop"]["yield_per_hectare"] for plot in farm_data["plots"]) / len(farm_data["plots"]), 0
                ),
                "irrigation_coverage": round(
                    sum(1 for plot in farm_data["plots"] if plot["irrigation_status"]) / len(farm_data["plots"]) * 100, 1
                )
            }
        }