import asyncio
import json
from datetime import datetime
from typing import Dict, List
from .data_simulator import MalaysianFarmSimulator
from .farm_service import FarmService

class LiveDataService:
    def __init__(self):
        self.simulator = MalaysianFarmSimulator()
        self.farm_service = FarmService()
        self.is_running = False
        
    async def start_live_simulation(self):
        """Start continuous data simulation"""
        self.is_running = True
        print("🔄 Starting live data simulation...")
        
        while self.is_running:
            try:
                # Generate new sensor readings every 30 seconds
                await self.update_sensor_data()
                
                # Update weather forecast every hour
                if datetime.now().minute == 0:
                    await self.update_weather_data()
                
                # Check for new alerts every 5 minutes
                if datetime.now().minute % 5 == 0:
                    await self.check_alerts()
                
                await asyncio.sleep(30)  # Wait 30 seconds
                
            except Exception as e:
                print(f"❌ Error in live simulation: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def update_sensor_data(self):
        """Generate new sensor readings"""
        try:
            live_data = self.farm_service.generate_live_sensor_data()
            print(f"📡 Generated {len(live_data)} sensor readings at {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"❌ Error updating sensor data: {e}")
    
    async def update_weather_data(self):
        """Update weather forecast"""
        try:
            forecast = self.farm_service.update_weather_forecast()
            print(f"🌤️ Updated weather forecast at {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"❌ Error updating weather: {e}")
    
    async def check_alerts(self):
        """Check for new alerts"""
        try:
            farm_data = self.farm_service.get_farm()
            all_equipment = []
            
            for plot in farm_data["plots"]:
                all_equipment.extend(plot["equipment"])
            
            new_alerts = self.simulator.simulate_equipment_alerts(all_equipment)
            
            for alert in new_alerts:
                self.farm_service.add_alert(alert)
            
            if new_alerts:
                print(f"🚨 Generated {len(new_alerts)} alerts at {datetime.now().strftime('%H:%M:%S')}")
                
        except Exception as e:
            print(f"❌ Error checking alerts: {e}")
    
    def stop_simulation(self):
        """Stop live simulation"""
        self.is_running = False
        print("⏹️ Stopped live data simulation")