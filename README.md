🏗️ System Architecture

Architecture Overview

The Smart Farm Management System is built using a modern microservices architecture designed for real-time IoT data processing, scalable farm management, and Malaysian agricultural operations. The system consists of three main layers working together to provide comprehensive farm monitoring and control.

System Components Diagram

┌─────────────────────────────────────────────────────────────────┐
│ USER INTERFACE LAYER │
│ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐│
│ │ Dashboard │ │ Plot │ │ Sensor │ │ Farm ││
│ │ Component │ │ Management │ │ Monitoring │ │ Map ││
│ │ 📊 │ │ 🌱 │ │ 📡 │ │ 🗺️ ││
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘│
│ │
│ React.js Frontend (Port 3000) │
└─────────────────────────────────────────────────────────────────┘
│
HTTP/WebSocket API
│
┌─────────────────────────────────────────────────────────────────┐
│ BACKEND SERVICES LAYER │
│ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐│
│ │ FastAPI │ │ WebSocket │ │ Background │ │ Alert ││
│ │ REST APIs │ │ Server │ │ Tasks │ │ System ││
│ │ 🔌 │ │ 📡 │ │ ⚙️ │ │ 🚨 ││
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘│
│ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Farm │ │ Data │ │ Live Data │ │
│ │ Service │ │ Simulator │ │ Service │ │
│ │ 🌾 │ │ 🎲 │ │ 📊 │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ │
│ │
│ Python Backend (Port 8000) │
└─────────────────────────────────────────────────────────────────┘
│
File System I/O
│
┌─────────────────────────────────────────────────────────────────┐
│ DATA STORAGE LAYER │
│ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐│
│ │ Farm │ │ Sensor │ │ Weather │ │ Alerts ││
│ │ Data │ │ Data │ │ Forecast │ │ Data ││
│ │ 📄 │ │ 📄 │ │ 📄 │ │ 📄 ││
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘│
│ │
│ JSON File Storage System │
└─────────────────────────────────────────────────────────────────┘
│
Malaysian Data Simulation
│
┌─────────────────────────────────────────────────────────────────┐
│ SIMULATION ENGINE LAYER │
│ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐│
│ │ Weather │ │ Crop │ │ Sensor │ │Equipment││
│ │ Patterns │ │ Growth │ │ Network │ │Monitor ││
│ │ 🌦️ │ │ 🌱 │ │ 📡 │ │ 🔧 ││
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘│
│ │
│ Malaysian Agricultural Simulation │
└─────────────────────────────────────────────────────────────────┘

Component Interaction Flow

1. Data Flow Pipeline

Data Generation → Processing → Storage → API → Frontend Display
↓ ↓ ↓ ↓ ↓
Simulation → Background → JSON Files → HTTP → React Components
Tasks WebSocket

2. Real-time Communication

Frontend ←─ WebSocket ─→ Backend ←─ Timer ─→ Data Simulator
│ │ │
└── User Actions ──→ REST API ──→ Data Updates ──┘

3. System Interaction Sequence

User Interface
│
├─ Dashboard Request ─→ Farm Service ─→ JSON Data ─→ Response
│
├─ Plot Control ─→ API Endpoint ─→ Data Update ─→ WebSocket Broadcast
│
├─ Live Data ←─ WebSocket ←─ Background Task ←─ Data Simulator
│
└─ Map View ─→ Location API ─→ Plot Coordinates ─→ Leaflet Map

Technical Architecture Details

Frontend Architecture (React.js)

React App (localhost:3000)
├── App.js (Main container)
├── Components/
│ ├── Dashboard.js (Farm overview)
│ ├── PlotManagement.js (Plot controls)
│ ├── SensorMonitoring.js (Live data)
│ └── FarmMap.js (Interactive map)
├── Services/
│ ├── api.js (HTTP client)
│ └── websocket.js (Real-time client)
└── Styles/
└── App.css (Malaysian theme)

Key Features:

State Management: React hooks for component state
API Integration: Axios for HTTP requests
Real-time Updates: WebSocket connections
Interactive Maps: Leaflet integration
Data Visualization: Recharts for analytics

Backend Architecture (FastAPI)

FastAPI Server (localhost:8000)
├── main.py (Application entry)
├── Services/
│ ├── farm_service.py (CRUD operations)
│ ├── data_simulator.py (Malaysian data)
│ └── live_data_service.py (Real-time)
├── Models/
│ ├── farm_models.py (Data structures)
│ └── sensor_models.py (IoT models)
└── Data/
├── farm_data.json (Main data)
├── sensor_data.json (Readings)
└── alerts.json (Notifications)

Key Features:

REST API: CRUD operations for all entities
WebSocket Server: Real-time data streaming
Background Tasks: Automated data generation
Data Validation: Pydantic models
Error Handling: Comprehensive exception management

Data Simulation Engine

Malaysian Agriculture Simulator
├── Weather Simulation
│ ├── Dry Season (Jun-Sep)
│ ├── Wet Season (Oct-Mar)
│ └── Transition (Apr-May)
├── Crop Management
│ ├── Rice (MR220, MR219)
│ ├── Palm Oil (Tenera, Dura)
│ ├── Rubber (RRIM varieties)
│ └── Tropical Fruits
├── IoT Sensor Network
│ ├── Environmental sensors
│ ├── Soil monitoring
│ └── Equipment tracking
└── Alert System
├── Maintenance alerts
├── Weather warnings
└── Equipment failures

Data Architecture

Information Flow

Real-World Data Simulation
↓
JSON File Storage
↓
Service Layer Processing
↓
API Response Generation
↓
Frontend State Update
↓
User Interface Display

Database Schema (JSON-based)

{
"farm": {
"plots": ["plot_1", "plot_2"],
"equipment": ["equipment_1"],
"sensors": ["sensor_1", "sensor_2"]
},
"sensor_readings": {
"timestamp": "2024-01-01T00:00:00",
"sensor_id": "sensor_1",
"temperature": 28.5,
"humidity": 75.2,
"soil_moisture": 82.1
}
}

Communication Protocols

REST API Endpoints

GET /api/farm → Farm information
GET /api/plots → All farm plots
PUT /api/plots/{id}/status → Update plot status
GET /api/sensors/live → Live sensor data
POST /api/alerts → Create alerts

WebSocket Events

live_update → Real-time sensor data
plot_update → Plot status changes  
irrigation_update → Irrigation toggles
weather_update → Weather forecasts
new_alert → System alerts

Scalability Design

Current Architecture (Development)

Single Instance: One backend server
File Storage: JSON-based persistence
In-Memory: WebSocket connections
Local Simulation: Background data generation

Production Ready Architecture

Load Balancer
│
┌────┴────┐
│ Frontend │ (React.js)
│ Servers │
└─────────┘
│
┌────┴────┐
│ API │ (FastAPI)
│ Gateway │
└─────────┘
│
┌────┴────┐ ┌─────────┐ ┌─────────┐
│Backend │────│Database │────│Message │
│Services │ │Cluster │ │Queue │
└─────────┘ └─────────┘ └─────────┘
│
┌────┴────┐
│ IoT │
│ Gateway │ (Real Sensors)
└─────────┘

Deployment Architecture

Development Environment

Local Machine
├── Backend: python main.py (Port 8000)
├── Frontend: npm start (Port 3000)
└── Data: JSON files in /backend/data/

Production Environment

Cloud Infrastructure
├── Application Load Balancer
├── Container Services (Docker)
├── Managed Database (PostgreSQL)
├── Message Queue (Redis)
├── IoT Hub (Device management)
└── CDN (Static assets)

This architecture provides a robust foundation for Malaysian agricultural management while maintaining simplicity for development and flexibility for future IoT integration and scaling. 🌾🏗️

Smart Farm Management System 🌾

A comprehensive IoT-enabled farm management system designed specifically for Malaysian agricultural operations using European metrics and real-time data simulation.

🇲🇾 Malaysian Agricultural Focus

This system is tailored for Malaysian farming conditions with support for:

Local Crops: Rice (Padi), Palm Oil, Rubber, Durian, Banana, Coconut
Tropical Climate: Monsoon patterns, high humidity, temperature variations
Regional Varieties: MR220 Rice, Musang King Durian, RRIM Rubber, etc.
European Metrics: Hectares, Celsius, Millimeters, Kilograms

✨ Features

🏡 Farm Management

Real-time dashboard with farm overview
Individual plot monitoring and control
Crop lifecycle tracking with Malaysian varieties
Equipment status and maintenance alerts
Irrigation system control

📡 IoT Sensor Network

Live environmental monitoring
Historical data analysis with 30+ days of data
Weather pattern recognition (dry/wet seasons)
Soil condition tracking (pH, moisture, nutrients)
Automated alert system

🗺️ Interactive Mapping

Geospatial plot visualization
Equipment location tracking
Sensor network overlay
Malaysian coordinates integration

📊 Analytics & Reports

Yield estimation and projections
Performance analytics
Environmental scoring
Equipment efficiency tracking
Weather-based insights

🔄 Real-time Updates

WebSocket live data streaming
Automatic sensor data generation
Live weather simulation
Instant alert notifications

🛠️ Technology Stack

Backend

FastAPI: Modern Python web framework
WebSocket: Real-time communication
JSON: File-based data storage
Asyncio: Background task management
Data Simulation: Realistic Malaysian agricultural data

Frontend

React.js: Modern UI framework
Leaflet: Interactive mapping
Recharts: Data visualization
Custom CSS: Malaysian-themed styling
WebSocket Client: Real-time updates

Data

JSON Storage: Lightweight data persistence
Live Simulation: Continuous data generation
Historical Data: 30+ days of sensor readings
Malaysian Weather: Seasonal pattern simulation

🚀 Quick Start

Prerequisites

Node.js 16+ and npm
Python 3.8+
Git

1. Clone Repository

git clone <repository-url>
cd smart-farm-management

2. Backend Setup

cd backend

# Create virtual environment

python -m venv venv

# Activate virtual environment

# Windows:

venv\Scripts\activate

# macOS/Linux:

source venv/bin/activate

# Install dependencies

pip install -r requirements.txt

# Generate initial data

python generate_sample_data.py

# Start backend server

python main.py

The backend will be available at http://localhost:8000

3. Frontend Setup

cd frontend

# Install dependencies

npm install

# Start development server

npm start

The frontend will be available at http://localhost:3000

4. Access the Application

Main App: http://localhost:3000
API Documentation: http://localhost:8000/docs
Health Check: http://localhost:8000/api/health

📂 Project Structure

smart-farming-app/
├── backend/
│ ├── main.py # FastAPI application
│ ├── requirements.txt # Python dependencies
│ ├── generate_sample_data.py # Data generation script
│ ├── services/
│ │ ├── farm_service.py # Core farm operations
│ │ ├── data_simulator.py # Malaysian data simulation
│ │ └── live_data_service.py # Real-time data service
│ └── data/
│ ├── farm_data.json # Main farm data
│ ├── sensor_data.json # Historical sensor readings
│ ├── alerts.json # System alerts
│ └── weather_forecast.json # Weather predictions
├── frontend/
│ ├── public/
│ │ └── index.html # Main HTML template
│ ├── src/
│ │ ├── App.js # Main React component
│ │ ├── App.css # Malaysian-themed styles
│ │ ├── services/
│ │ │ └── api.js # API communication
│ │ └── components/
│ │ ├── Dashboard.js # Farm overview
│ │ ├── PlotManagement.js # Plot operations
│ │ ├── SensorMonitoring.js # Real-time monitoring
│ │ └── FarmMap.js # Interactive mapping
│ └── package.json # Node.js dependencies
└── README.md # This file

🔌 API Endpoints

Farm Operations

GET /api/farm # Complete farm information
GET /api/farm/summary # Farm statistics summary

Plot Management

GET /api/plots # All farm plots
GET /api/plots/{id} # Specific plot details
PUT /api/plots/{id}/status # Update plot status
PUT /api/plots/{id}/irrigation # Toggle irrigation

Sensor Data

GET /api/sensors # All sensor data
GET /api/sensors/live # Live sensor readings
GET /api/sensors/{id} # Specific sensor history
GET /api/sensors/summary # Sensor statistics

Alerts & Monitoring

GET /api/alerts # All system alerts
POST /api/alerts # Create new alert
POST /api/alerts/broadcast # Broadcast alert

Weather & Analytics

GET /api/weather/current # Current conditions
GET /api/weather/forecast # 7-day forecast
GET /api/analytics # Comprehensive analytics
GET /api/analytics/performance # Performance metrics

System Health

GET /api/health # System status
WebSocket /ws # Real-time connection

🌤️ Malaysian Weather Simulation

The system simulates realistic Malaysian weather patterns:

Seasonal Patterns

Dry Season (Jun-Sep): Lower rainfall, higher temperatures
Wet Season (Oct-Mar): Higher rainfall, moderate temperatures  
Transition (Apr-May): Variable conditions

Environmental Factors

Temperature: 24-35°C with diurnal variations
Humidity: 60-95% based on season and rainfall
Rainfall: 0-80mm with monsoon patterns
Soil Conditions: pH, moisture, nutrients by crop type

🌱 Supported Crops

Crop Varieties Growth Cycle Yield (kg/ha)
Rice MR220, MR219, MR297, Bario 120 days 3,000-7,000
Palm Oil Dura, Tenera, MPOB 365 days 15,000-25,000
Rubber RRIM 600, RRIM 2020, PB 260 365 days 1,200-2,500
Durian Musang King, D24, Red Prawn 150 days 8,000-15,000
Banana Cavendish, Pisang Mas, Raja 300 days 20,000-40,000
Coconut Malayan Dwarf, Malayan Tall 365 days 6,000-12,000

📊 Real-time Features

Live Data Simulation

Sensor readings every 30 seconds
Weather updates every hour
Equipment status monitoring
Automatic alert generation

WebSocket Events

// Example WebSocket usage
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
const data = JSON.parse(event.data);

switch(data.type) {
case 'live_update':
// Handle sensor data updates
break;
case 'plot_update':
// Handle plot status changes
break;
case 'new_alert':
// Handle new alerts
break;
}
};

🧪 Development & Testing

Generate New Data

# Regenerate all sample data

cd backend
python generate_sample_data.py

# Or use the quick script

python run_data_generator.py

API Testing

# Test API endpoints

curl http://localhost:8000/api/health
curl http://localhost:8000/api/farm/summary
curl http://localhost:8000/api/sensors/live

Development Endpoints

# Regenerate farm data (dev only)

POST /api/dev/regenerate-data

# Simulate alerts (dev only)

POST /api/dev/simulate-alert?alert_type=maintenance

🌍 Real-World Deployment

Production Architecture

Internet → Load Balancer → API Gateway
↓
FastAPI Backend
↓
PostgreSQL Database
↓
IoT Device Gateway
↓
Field Sensors & Equipment

Scaling Considerations

Database Migration

# Replace JSON with PostgreSQL

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Models for production

class Farm(Base):
**tablename** = "farms"
id = Column(String, primary_key=True)
name = Column(String)
location = Column(String) # ... additional fields

Cloud Deployment

# docker-compose.yml for production

version: '3.8'
services:
backend:
build: ./backend
ports: - "8000:8000"
environment: - DATABASE_URL=postgresql://user:pass@db:5432/farmdb

frontend:
build: ./frontend
ports: - "80:80"

db:
image: postgres:13
environment:
POSTGRES_DB: farmdb
POSTGRES_USER: user
POSTGRES_PASSWORD: pass

IoT Integration

# Example LoRaWAN integration

import paho.mqtt.client as mqtt

class IoTIntegration:
def **init**(self):
self.client = mqtt.Client()
self.client.on_message = self.on_sensor_data

    def on_sensor_data(self, client, userdata, message):
        # Process real sensor data
        sensor_data = json.loads(message.payload)
        self.farm_service.save_sensor_reading(sensor_data)

Security Implementation

# Add authentication

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.middleware("http")
async def authenticate(request: Request, call_next): # Add JWT authentication
pass

📱 Mobile App Integration

React Native Extension

// Example mobile API usage
import { farmApi } from './services/api';

const MobileFarmDashboard = () => {
const [farmData, setFarmData] = useState(null);

useEffect(() => {
farmApi.getFarm().then(setFarmData);
}, []);

return (
<ScrollView>
<FarmSummary data={farmData} />
<LiveSensorData />
<AlertsList />
</ScrollView>
);
};

🤝 Contributing

Development Setup

Fork the repository
Create a feature branch
Make your changes
Add tests
Submit a pull request

Code Standards

Python: Follow PEP 8
JavaScript: Use ESLint configuration
Documentation: Update README for new features
Testing: Add unit tests for new functionality

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

Malaysian Agricultural Research and Development Institute (MARDI)
Federal Land Development Authority (FELDA)
Malaysian Palm Oil Board (MPOB)
Department of Agriculture Malaysia

📞 Support

Getting Help

Documentation: Check API docs at /docs
Health Check: Monitor at /api/health
Issues: Report bugs via GitHub issues
Features: Request features via GitHub discussions

System Requirements

Backend: Python 3.8+, 2GB RAM, 10GB storage
Frontend: Node.js 16+, Modern browser
Network: Stable internet for real-time features

🚀 Future Enhancements

Planned Features

Machine learning crop predictions
Drone integration for aerial monitoring
Mobile app for field operations
Blockchain for supply chain tracking
AI-powered pest detection
Weather station integration
Automated irrigation scheduling
Market price integration

Integration Roadmap

Phase 1: Database migration (PostgreSQL)
Phase 2: Real IoT device integration
Phase 3: Cloud deployment (AWS/Azure)
Phase 4: Mobile app development
Phase 5: AI/ML implementation
Phase 6: Blockchain integration
