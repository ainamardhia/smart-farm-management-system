#!/usr/bin/env python3
"""
Script to generate comprehensive sample data for Smart Farm Management System
Run this to create initial farm data and historical sensor readings
"""

import json
import os
from datetime import datetime
from services.data_simulator import MalaysianFarmSimulator

def generate_complete_dataset():
    """Generate complete dataset for the farm management system"""
    simulator = MalaysianFarmSimulator()
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    
    print("🌾 Generating Malaysian Smart Farm Data...")
    
    # Generate main farm data
    print("📊 Creating farm structure...")
    farm_data = simulator.generate_complete_farm()
    
    # Save main farm data
    with open("data/farm_data.json", "w") as f:
        json.dump(farm_data, f, indent=2)
    
    print(f"✅ Generated farm: {farm_data['name']}")
    print(f"📍 Location: {farm_data['location']}")
    print(f"🌱 Plots: {len(farm_data['plots'])}")
    print(f"📏 Total Area: {farm_data['total_area']} hectares")
    
    # Generate historical sensor data
    print("\n📡 Generating historical sensor data...")
    all_sensor_data = []
    
    for plot in farm_data["plots"]:
        plot_info = {
            "plot_id": plot["id"],
            "crop_type": plot["crop"]["type"],
            "location": plot["location"]
        }
        
        # Generate 30 days of historical data
        historical_data = simulator.generate_historical_sensor_data(
            plot["sensors"], plot_info, days=30
        )
        all_sensor_data.extend(historical_data)
        
        print(f"  📈 Plot {plot['name']}: {len(historical_data)} sensor readings")
    
    # Save sensor data
    with open("data/sensor_data.json", "w") as f:
        json.dump(all_sensor_data, f, indent=2)
    
    print(f"✅ Generated {len(all_sensor_data)} historical sensor readings")
    
    # Generate equipment alerts
    print("\n🚨 Generating equipment alerts...")
    all_equipment = []
    for plot in farm_data["plots"]:
        all_equipment.extend(plot["equipment"])
    
    alerts = simulator.simulate_equipment_alerts(all_equipment)
    
    with open("data/alerts.json", "w") as f:
        json.dump(alerts, f, indent=2)
    
    print(f"✅ Generated {len(alerts)} equipment alerts")
    
    # Generate weather forecast
    print("\n🌤️ Generating weather forecast...")
    forecast = simulator.generate_weather_forecast(farm_data["coordinates"], days=7)
    
    with open("data/weather_forecast.json", "w") as f:
        json.dump(forecast, f, indent=2)
    
    print(f"✅ Generated 7-day weather forecast")
    
    # Generate summary statistics
    print("\n📊 Generating farm statistics...")
    
    # Crop distribution
    crop_counts = {}
    total_yield = 0
    total_equipment = 0
    total_sensors = 0
    
    for plot in farm_data["plots"]:
        crop_type = plot["crop"]["type"]
        crop_counts[crop_type] = crop_counts.get(crop_type, 0) + 1
        total_yield += plot["crop"]["yield_estimate"]
        total_equipment += len(plot["equipment"])
        total_sensors += len(plot["sensors"])
    
    # Equipment status distribution
    equipment_status = {}
    for plot in farm_data["plots"]:
        for equipment in plot["equipment"]:
            status = equipment["status"]
            equipment_status[status] = equipment_status.get(status, 0) + 1
                                 
    statistics = {
        "generated_at": datetime.now().isoformat(),
        "farm_summary": {
            "total_plots": len(farm_data["plots"]),
            "total_area": farm_data["total_area"],
            "total_yield_estimate": total_yield,
            "total_equipment": total_equipment,
            "total_sensors": total_sensors,
            "crop_distribution": crop_counts,
            "equipment_status": equipment_status
        },
        "sensor_data_summary": {
            "total_readings": len(all_sensor_data),
            "date_range": {
                "start": min(reading["timestamp"] for reading in all_sensor_data),
                "end": max(reading["timestamp"] for reading in all_sensor_data)
            },
            "sensors_count": len(set(reading["sensor_id"] for reading in all_sensor_data))
        },
        "alerts_summary": {
            "total_alerts": len(alerts),
            "alert_types": {}
        }
    }
    
    # Alert type distribution
    for alert in alerts:
        alert_type = alert["type"]
        statistics["alerts_summary"]["alert_types"][alert_type] = \
            statistics["alerts_summary"]["alert_types"].get(alert_type, 0) + 1
    
    with open("data/statistics.json", "w") as f:
        json.dump(statistics, f, indent=2)
    
    print(f"✅ Generated farm statistics")
    
    # Print summary
    print("\n" + "="*50)
    print("🎉 DATA GENERATION COMPLETE!")
    print("="*50)
    print(f"📊 Farm Data: data/farm_data.json")
    print(f"📡 Sensor Data: data/sensor_data.json")
    print(f"🚨 Alerts: data/alerts.json")
    print(f"🌤️ Weather Forecast: data/weather_forecast.json")
    print(f"📈 Statistics: data/statistics.json")
    print("\n🚀 Ready to start the Smart Farm Management System!")
    
    return {
        "farm_data": farm_data,
        "sensor_data": all_sensor_data,
        "alerts": alerts,
        "forecast": forecast,
        "statistics": statistics
    }

if __name__ == "__main__":
    generate_complete_dataset()