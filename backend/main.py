from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import uvicorn
import asyncio
import json
from datetime import datetime
from contextlib import asynccontextmanager
from services.farm_service import FarmService
from services.live_data_service import LiveDataService

# Initialize services
farm_service = FarmService()
live_service = LiveDataService()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"📡 WebSocket client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"📡 WebSocket client disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"❌ Error sending WebSocket message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"❌ Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - start and stop background tasks"""
    print("🌾 Starting Smart Farm Management System...")
    
    # Start live simulation in background
    simulation_task = asyncio.create_task(live_service.start_live_simulation())
    
    # Start WebSocket broadcast task
    broadcast_task = asyncio.create_task(broadcast_live_data())
    
    yield
    
    # Cleanup on shutdown
    print("🛑 Shutting down Smart Farm Management System...")
    live_service.stop_simulation()
    simulation_task.cancel()
    broadcast_task.cancel()
    
    try:
        await simulation_task
        await broadcast_task
    except asyncio.CancelledError:
        pass

async def broadcast_live_data():
    """Broadcast live sensor data to all connected WebSocket clients"""
    while True:
        try:
            if manager.active_connections:
                # Get live sensor data
                live_data = farm_service.generate_live_sensor_data()
                
                # Get recent alerts
                alerts = farm_service.get_alerts()
                recent_alerts = [alert for alert in alerts[-5:]]  # Last 5 alerts
                
                # Prepare broadcast message
                message = json.dumps({
                    "type": "live_update",
                    "timestamp": datetime.now().isoformat(),
                    "sensor_data": live_data,
                    "alerts": recent_alerts,
                    "connection_count": len(manager.active_connections)
                })
                
                await manager.broadcast(message)
                print(f"📡 Broadcasted live data to {len(manager.active_connections)} clients")
            
            await asyncio.sleep(30)  # Broadcast every 30 seconds
            
        except Exception as e:
            print(f"❌ Error in broadcast task: {e}")
            await asyncio.sleep(60)  # Wait longer on error

# Initialize FastAPI app with lifespan management
app = FastAPI(
    title="Smart Farm Management System", 
    version="1.0.0",
    description="IoT-enabled Smart Farm Management for Malaysian Agriculture",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "🌾 Smart Farm Management System API",
        "version": "1.0.0",
        "description": "Malaysian Agricultural IoT Management Platform",
        "endpoints": {
            "farm": "/api/farm",
            "plots": "/api/plots", 
            "sensors": "/api/sensors",
            "alerts": "/api/alerts",
            "weather": "/api/weather",
            "analytics": "/api/analytics",
            "websocket": "/ws"
        }
    }

# Farm endpoints
@app.get("/api/farm")
async def get_farm():
    """Get complete farm information"""
    try:
        return farm_service.get_farm()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching farm data: {str(e)}")

@app.get("/api/farm/summary")
async def get_farm_summary():
    """Get farm summary statistics"""
    try:
        farm_data = farm_service.get_farm()
        plots = farm_data.get("plots", [])
        
        # Calculate summary statistics
        total_plots = len(plots)
        total_area = farm_data.get("total_area", 0)
        active_plots = len([p for p in plots if p["status"] == "active"])
        total_equipment = sum(len(p.get("equipment", [])) for p in plots)
        total_sensors = sum(len(p.get("sensors", [])) for p in plots)
        
        return {
            "farm_name": farm_data.get("name", "Unknown Farm"),
            "location": farm_data.get("location", "Malaysia"),
            "total_plots": total_plots,
            "active_plots": active_plots,
            "total_area": total_area,
            "total_equipment": total_equipment,
            "total_sensors": total_sensors,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Plot endpoints
@app.get("/api/plots")
async def get_plots():
    """Get all farm plots"""
    try:
        return farm_service.get_plots()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plots: {str(e)}")

@app.get("/api/plots/{plot_id}")
async def get_plot(plot_id: str):
    """Get specific plot by ID"""
    try:
        plot = farm_service.get_plot(plot_id)
        if not plot:
            raise HTTPException(status_code=404, detail="Plot not found")
        return plot
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/plots/{plot_id}/status")
async def update_plot_status(plot_id: str, status_data: Dict[str, str]):
    """Update plot status"""
    try:
        status = status_data.get("status")
        if not status:
            raise HTTPException(status_code=400, detail="Status is required")
        
        valid_statuses = ["active", "maintenance", "harvesting", "idle"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        
        success = farm_service.update_plot_status(plot_id, status)
        if not success:
            raise HTTPException(status_code=404, detail="Plot not found")
        
        # Broadcast update to WebSocket clients
        await manager.broadcast(json.dumps({
            "type": "plot_update",
            "plot_id": plot_id,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }))
        
        return {"message": "Plot status updated successfully", "plot_id": plot_id, "new_status": status}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/plots/{plot_id}/irrigation")
async def toggle_irrigation(plot_id: str):
    """Toggle irrigation status for a plot"""
    try:
        success = farm_service.toggle_irrigation(plot_id)
        if not success:
            raise HTTPException(status_code=404, detail="Plot not found")
        
        # Get updated plot info
        plot = farm_service.get_plot(plot_id)
        irrigation_status = plot["irrigation_status"] if plot else False
        
        # Broadcast update to WebSocket clients
        await manager.broadcast(json.dumps({
            "type": "irrigation_update",
            "plot_id": plot_id,
            "irrigation_status": irrigation_status,
            "timestamp": datetime.now().isoformat()
        }))
        
        return {
            "message": "Irrigation status toggled successfully", 
            "plot_id": plot_id, 
            "irrigation_status": irrigation_status
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sensor endpoints
@app.get("/api/sensors/live")
async def get_live_sensor_data():
    """Get live sensor data for all plots"""
    try:
        return farm_service.generate_live_sensor_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating live sensor data: {str(e)}")

@app.get("/api/sensors/{sensor_id}")
async def get_sensor_data(sensor_id: str, limit: int = 100):
    """Get historical data for a specific sensor"""
    try:
        data = farm_service.get_sensor_data(sensor_id, limit)
        if not data:
            raise HTTPException(status_code=404, detail="No data found for this sensor")
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sensors")
async def get_all_sensor_data(limit: int = 100):
    """Get all sensor data"""
    try:
        return farm_service.get_sensor_data(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sensors/summary")
async def get_sensors_summary():
    """Get summary of all sensor readings"""
    try:
        sensor_data = farm_service.get_sensor_data(limit=50)
        if not sensor_data:
            return {"message": "No sensor data available"}
        
        # Calculate averages
        total_readings = len(sensor_data)
        avg_temperature = sum(d["temperature"] for d in sensor_data) / total_readings
        avg_humidity = sum(d["humidity"] for d in sensor_data) / total_readings
        avg_soil_moisture = sum(d["soil_moisture"] for d in sensor_data) / total_readings
        avg_ph = sum(d["ph_level"] for d in sensor_data) / total_readings
        total_rainfall = sum(d["rainfall"] for d in sensor_data)
        
        unique_sensors = len(set(d["sensor_id"] for d in sensor_data))
        
        return {
            "total_readings": total_readings,
            "unique_sensors": unique_sensors,
            "averages": {
                "temperature": round(avg_temperature, 1),
                "humidity": round(avg_humidity, 1),
                "soil_moisture": round(avg_soil_moisture, 1),
                "ph_level": round(avg_ph, 1),
                "total_rainfall": round(total_rainfall, 1)
            },
            "last_reading": sensor_data[-1]["timestamp"] if sensor_data else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Alert endpoints
@app.get("/api/alerts")
async def get_alerts():
    """Get all alerts"""
    try:
        return farm_service.get_alerts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/alerts")
async def create_alert(alert_data: Dict):
    """Create a new alert"""
    try:
        # Add timestamp and ID if not provided
        if "timestamp" not in alert_data:
            alert_data["timestamp"] = datetime.now().isoformat()
        if "id" not in alert_data:
            import uuid
            alert_data["id"] = str(uuid.uuid4())
        
        success = farm_service.add_alert(alert_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create alert")
        
        # Broadcast alert to WebSocket clients
        await manager.broadcast(json.dumps({
            "type": "new_alert",
            "alert": alert_data,
            "timestamp": datetime.now().isoformat()
        }))
        
        return {"message": "Alert created successfully", "alert_id": alert_data["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/alerts/broadcast")
async def broadcast_alert(alert_data: Dict):
    """Broadcast alert to all connected clients"""
    try:
        await manager.broadcast(json.dumps({
            "type": "broadcast_alert",
            "data": alert_data,
            "timestamp": datetime.now().isoformat()
        }))
        return {"message": "Alert broadcasted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Weather endpoints
@app.get("/api/weather/forecast")
async def get_weather_forecast():
    """Get weather forecast"""
    try:
        return farm_service.get_weather_forecast()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/weather/forecast")
async def update_weather_forecast():
    """Update weather forecast"""
    try:
        forecast = farm_service.update_weather_forecast()
        
        # Broadcast weather update
        await manager.broadcast(json.dumps({
            "type": "weather_update",
            "forecast": forecast,
            "timestamp": datetime.now().isoformat()
        }))
        
        return {"message": "Weather forecast updated successfully", "forecast": forecast}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather/current")
async def get_current_weather():
    """Get current weather conditions from latest sensor data"""
    try:
        sensor_data = farm_service.get_sensor_data(limit=20)
        if not sensor_data:
            raise HTTPException(status_code=404, detail="No weather data available")
        
        # Calculate current conditions from recent sensor readings
        recent_data = sensor_data[-10:]  # Last 10 readings
        avg_temp = sum(d["temperature"] for d in recent_data) / len(recent_data)
        avg_humidity = sum(d["humidity"] for d in recent_data) / len(recent_data)
        total_rainfall = sum(d["rainfall"] for d in recent_data)
        avg_light = sum(d["light_intensity"] for d in recent_data) / len(recent_data)
        
        return {
            "temperature": round(avg_temp, 1),
            "humidity": round(avg_humidity, 1),
            "rainfall": round(total_rainfall, 1),
            "light_intensity": round(avg_light, 0),
            "last_updated": recent_data[-1]["timestamp"],
            "conditions": "Real-time sensor data",
            "data_points": len(recent_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analytics endpoints
@app.get("/api/analytics")
async def get_analytics():
    """Get comprehensive analytics report"""
    try:
        return farm_service.generate_analytics_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/performance")
async def get_performance_analytics():
    """Get farm performance analytics"""
    try:
        farm_data = farm_service.get_farm()
        sensor_data = farm_service.get_sensor_data(limit=200)
        
        # Calculate performance metrics
        plots = farm_data.get("plots", [])
        total_yield = sum(plot["crop"]["yield_estimate"] for plot in plots)
        avg_yield_per_hectare = total_yield / farm_data["total_area"] if farm_data["total_area"] > 0 else 0
        
        # Equipment efficiency
        all_equipment = []
        for plot in plots:
            all_equipment.extend(plot.get("equipment", []))
        
        operational_equipment = len([eq for eq in all_equipment if eq["status"] == "operational"])
        equipment_efficiency = (operational_equipment / len(all_equipment)) * 100 if all_equipment else 0
        
        # Irrigation coverage
        irrigated_plots = len([plot for plot in plots if plot["irrigation_status"]])
        irrigation_coverage = (irrigated_plots / len(plots)) * 100 if plots else 0
        
        # Environmental conditions score
        if sensor_data:
            recent_sensors = sensor_data[-50:]  # Last 50 readings
            avg_conditions = {
                "temperature": sum(d["temperature"] for d in recent_sensors) / len(recent_sensors),
                "humidity": sum(d["humidity"] for d in recent_sensors) / len(recent_sensors),
                "soil_moisture": sum(d["soil_moisture"] for d in recent_sensors) / len(recent_sensors)
            }
            
            # Simple scoring system (0-100)
            temp_score = 100 if 26 <= avg_conditions["temperature"] <= 32 else max(0, 100 - abs(avg_conditions["temperature"] - 29) * 10)
            humidity_score = 100 if 70 <= avg_conditions["humidity"] <= 85 else max(0, 100 - abs(avg_conditions["humidity"] - 77.5) * 2)
            moisture_score = 100 if 70 <= avg_conditions["soil_moisture"] <= 90 else max(0, 100 - abs(avg_conditions["soil_moisture"] - 80) * 3)
            
            environmental_score = (temp_score + humidity_score + moisture_score) / 3
        else:
            environmental_score = 0
        
        return {
            "total_yield_estimate": round(total_yield, 0),
            "avg_yield_per_hectare": round(avg_yield_per_hectare, 0),
            "equipment_efficiency": round(equipment_efficiency, 1),
            "irrigation_coverage": round(irrigation_coverage, 1),
            "environmental_score": round(environmental_score, 1),
            "performance_grade": "A" if environmental_score >= 80 else "B" if environmental_score >= 60 else "C",
            "calculated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/statistics")
async def get_statistics():
    """Get farm statistics"""
    try:
        return farm_service.get_statistics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Equipment endpoints
@app.get("/api/equipment")
async def get_all_equipment():
    """Get all equipment across all plots"""
    try:
        farm_data = farm_service.get_farm()
        all_equipment = []
        
        for plot in farm_data.get("plots", []):
            for equipment in plot.get("equipment", []):
                equipment_with_plot = {
                    **equipment,
                    "plot_id": plot["id"],
                    "plot_name": plot["name"]
                }
                all_equipment.append(equipment_with_plot)
        
        return all_equipment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/equipment/status/{status}")
async def get_equipment_by_status(status: str):
    """Get equipment filtered by status"""
    try:
        all_equipment = await get_all_equipment()
        filtered_equipment = [eq for eq in all_equipment if eq["status"] == status]
        return filtered_equipment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# System health endpoints
@app.get("/api/health")
async def health_check():
    """System health check"""
    try:
        farm_data = farm_service.get_farm()
        sensor_data = farm_service.get_sensor_data(limit=10)
        alerts = farm_service.get_alerts()
        
        # Check data freshness
        data_fresh = True
        if sensor_data:
            last_reading = datetime.fromisoformat(sensor_data[-1]["timestamp"])
            if (datetime.now() - last_reading).seconds > 300:  # 5 minutes
                data_fresh = False
        
        # Count active alerts
        active_alerts = len([alert for alert in alerts[-10:] if alert.get("severity") in ["high", "medium"]])
        
        return {
            "status": "healthy" if data_fresh and active_alerts < 5 else "warning",
            "timestamp": datetime.now().isoformat(),
            "data_fresh": data_fresh,
            "active_connections": len(manager.active_connections),
            "active_alerts": active_alerts,
            "total_plots": len(farm_data.get("plots", [])),
            "live_simulation": live_service.is_running,
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await manager.connect(websocket)
    try:
        while True:
            # Wait for messages from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get("type", "unknown")
                
                if message_type == "ping":
                    # Respond to ping with pong
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "pong",
                            "timestamp": datetime.now().isoformat()
                        }),
                        websocket
                    )
                
                elif message_type == "request_live_data":
                    # Send current live data
                    live_data = farm_service.generate_live_sensor_data()
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "live_data_response",
                            "data": live_data,
                            "timestamp": datetime.now().isoformat()
                        }),
                        websocket
                    )
                
                elif message_type == "subscribe":
                    # Handle subscription requests
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "subscription_confirmed",
                            "message": "Subscribed to live updates",
                            "timestamp": datetime.now().isoformat()
                        }),
                        websocket
                    )
                
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "message": "Invalid JSON format",
                        "timestamp": datetime.now().isoformat()
                    }),
                    websocket
                )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        manager.disconnect(websocket)

# Development endpoints (for testing and data management)
@app.post("/api/dev/regenerate-data")
async def regenerate_farm_data():
    """Regenerate all farm data (development only)"""
    try:
        from services.data_simulator import MalaysianFarmSimulator
        
        simulator = MalaysianFarmSimulator()
        new_farm_data = simulator.generate_complete_farm()
        farm_service.save_farm_data(new_farm_data)
        
        # Broadcast update
        await manager.broadcast(json.dumps({
            "type": "farm_regenerated",
            "message": "Farm data has been regenerated",
            "timestamp": datetime.now().isoformat()
        }))
        
        return {
            "message": "Farm data regenerated successfully",
            "farm_name": new_farm_data["name"],
            "total_plots": len(new_farm_data["plots"])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dev/simulate-alert")
async def simulate_alert(alert_type: str = "maintenance"):
    """Simulate an alert (development only)"""
    try:
        import uuid
        
        alert = {
            "id": str(uuid.uuid4()),
            "type": alert_type,
            "severity": "medium",
            "message": f"Simulated {alert_type} alert for testing",
            "timestamp": datetime.now().isoformat(),
            "equipment_id": "test-equipment",
            "action_required": "Test alert - no action needed"
        }
        
        farm_service.add_alert(alert)
        
        # Broadcast alert
        await manager.broadcast(json.dumps({
            "type": "simulated_alert",
            "alert": alert,
            "timestamp": datetime.now().isoformat()
        }))
        
        return {"message": "Alert simulated successfully", "alert": alert}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API documentation
@app.get("/api/docs/endpoints")
async def get_api_documentation():
    """Get API endpoints documentation"""
    return {
        "title": "Smart Farm Management System API",
        "version": "1.0.0",
        "description": "Malaysian Agricultural IoT Management Platform",
        "endpoints": {
            "farm": {
                "GET /api/farm": "Get complete farm information",
                "GET /api/farm/summary": "Get farm summary statistics"
            },
            "plots": {
                "GET /api/plots": "Get all farm plots",
                "GET /api/plots/{plot_id}": "Get specific plot",
                "PUT /api/plots/{plot_id}/status": "Update plot status",
                "PUT /api/plots/{plot_id}/irrigation": "Toggle irrigation"
            },
            "sensors": {
                "GET /api/sensors": "Get all sensor data",
                "GET /api/sensors/live": "Get live sensor data",
                "GET /api/sensors/{sensor_id}": "Get sensor history",
                "GET /api/sensors/summary": "Get sensor summary"
            },
            "alerts": {
                "GET /api/alerts": "Get all alerts",
                "POST /api/alerts": "Create new alert",
                "POST /api/alerts/broadcast": "Broadcast alert"
            },
            "weather": {
                "GET /api/weather/forecast": "Get weather forecast",
                "PUT /api/weather/forecast": "Update weather forecast",
                "GET /api/weather/current": "Get current weather"
            },
            "analytics": {
                "GET /api/analytics": "Get comprehensive analytics",
                "GET /api/analytics/performance": "Get performance analytics",
                "GET /api/statistics": "Get farm statistics"
            },
            "equipment": {
                "GET /api/equipment": "Get all equipment",
                "GET /api/equipment/status/{status}": "Get equipment by status"
            },
            "system": {
                "GET /api/health": "System health check",
                "WebSocket /ws": "Real-time WebSocket connection"
            }
        },
        "websocket_events": {
            "live_update": "Live sensor data and alerts",
            "plot_update": "Plot status changes",
            "irrigation_update": "Irrigation status changes",
            "weather_update": "Weather forecast updates",
            "new_alert": "New alerts",
            "farm_regenerated": "Farm data regeneration"
        }
    }

if __name__ == "__main__":
    print("🌾 Starting Smart Farm Management System API...")
    print("📍 Malaysian Agricultural IoT Platform")
    print("🔗 API Documentation: http://localhost:8000/docs")
    print("📡 WebSocket Endpoint: ws://localhost:8000/ws")
    print("🌐 Health Check: http://localhost:8000/api/health")
    print("=" * 50)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )