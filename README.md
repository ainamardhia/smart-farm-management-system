# Smart Farm Management System 🌾

> A comprehensive IoT-enabled farm management system designed specifically for Malaysian agricultural operations using European metrics and real-time data simulation.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Node.js](https://img.shields.io/badge/node-16+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)

## 🇲🇾 Malaysian Agricultural Focus

Tailored for Malaysian farming conditions with support for:

- **Local Crops**: Rice (Padi), Palm Oil, Rubber, Durian, Banana, Coconut
- **Tropical Climate**: Monsoon patterns, high humidity, temperature variations  
- **Regional Varieties**: MR220 Rice, Musang King Durian, RRIM Rubber
- **European Metrics**: Hectares, Celsius, Millimeters, Kilograms

## ✨ Features

### 🏡 Farm Management
- Real-time dashboard with farm overview
- Individual plot monitoring and control
- Crop lifecycle tracking with Malaysian varieties
- Equipment status and maintenance alerts
- Irrigation system control

### 📡 IoT Sensor Network
- Live environmental monitoring
- Historical data analysis with 30+ days of data
- Weather pattern recognition (dry/wet seasons)
- Soil condition tracking (pH, moisture, nutrients)
- Automated alert system

### 🗺️ Interactive Mapping
- Geospatial plot visualization
- Equipment location tracking
- Sensor network overlay
- Malaysian coordinates integration

### 📊 Analytics & Reports
- Yield estimation and projections
- Performance analytics
- Environmental scoring
- Equipment efficiency tracking
- Weather-based insights

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI + Python | REST API & WebSocket server |
| **Frontend** | React.js | Modern UI framework |
| **Database** | JSON Files | Lightweight data storage |
| **Mapping** | Leaflet | Interactive maps |
| **Charts** | Recharts | Data visualization |
| **Real-time** | WebSocket | Live data streaming |

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-farm-management
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   # macOS/Linux  
   source venv/bin/activate
   
   pip install -r requirements.txt
   python generate_sample_data.py
   python main.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the Application**
   - Main App: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/health

## 📂 Project Structure

```
smart-farming-app/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── requirements.txt           # Python dependencies
│   ├── generate_sample_data.py    # Data generation script
│   ├── services/                  # Core services
│   │   ├── farm_service.py
│   │   ├── data_simulator.py
│   │   └── live_data_service.py
│   └── data/                      # JSON data storage
│       ├── farm_data.json
│       ├── sensor_data.json
│       ├── alerts.json
│       └── weather_forecast.json
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js                 # Main React component
│   │   ├── App.css               # Styling
│   │   ├── services/
│   │   │   └── api.js            # API client
│   │   └── components/           # React components
│   │       ├── Dashboard.js
│   │       ├── PlotManagement.js
│   │       ├── SensorMonitoring.js
│   │       └── FarmMap.js
│   └── package.json
└── README.md
```

## 🔌 API Endpoints

### Farm Operations
- `GET /api/farm` - Complete farm information
- `GET /api/farm/summary` - Farm statistics summary

### Plot Management
- `GET /api/plots` - All farm plots
- `GET /api/plots/{id}` - Specific plot details
- `PUT /api/plots/{id}/status` - Update plot status
- `PUT /api/plots/{id}/irrigation` - Toggle irrigation

### Sensor Data
- `GET /api/sensors` - All sensor data
- `GET /api/sensors/live` - Live sensor readings
- `GET /api/sensors/{id}` - Specific sensor history

### System Health
- `GET /api/health` - System status
- `WebSocket /ws` - Real-time connection

## 🌱 Supported Crops

| Crop | Varieties | Growth Cycle | Yield (kg/ha) |
|------|-----------|--------------|---------------|
| **Rice** | MR220, MR219, MR297, Bario | 120 days | 3,000-7,000 |
| **Palm Oil** | Dura, Tenera, MPOB | 365 days | 15,000-25,000 |
| **Rubber** | RRIM 600, RRIM 2020, PB 260 | 365 days | 1,200-2,500 |
| **Durian** | Musang King, D24, Red Prawn | 150 days | 8,000-15,000 |
| **Banana** | Cavendish, Pisang Mas, Raja | 300 days | 20,000-40,000 |
| **Coconut** | Malayan Dwarf, Malayan Tall | 365 days | 6,000-12,000 |

## 🌤️ Malaysian Weather Simulation

The system simulates realistic Malaysian weather patterns:

- **Dry Season** (Jun-Sep): Lower rainfall, higher temperatures
- **Wet Season** (Oct-Mar): Higher rainfall, moderate temperatures  
- **Transition** (Apr-May): Variable conditions

Environmental factors include temperature (24-35°C), humidity (60-95%), rainfall (0-80mm), and soil conditions varying by crop type.

## 📊 Real-time Features

### Live Data Simulation
- Sensor readings every 30 seconds
- Weather updates every hour
- Equipment status monitoring
- Automatic alert generation

### WebSocket Integration
```javascript
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
```

## 🧪 Development & Testing

### Generate New Data
```bash
cd backend
python generate_sample_data.py
```

### API Testing
```bash
curl http://localhost:8000/api/health
curl http://localhost:8000/api/farm/summary
curl http://localhost:8000/api/sensors/live
```

## 🌍 Production Deployment

For production deployment, consider:

- **Database Migration**: Replace JSON with PostgreSQL
- **Cloud Infrastructure**: AWS/Azure deployment with load balancers
- **IoT Integration**: Real sensor connectivity via MQTT/LoRaWAN
- **Security**: JWT authentication and HTTPS
- **Monitoring**: Application and infrastructure monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Standards
- **Python**: Follow PEP 8
- **JavaScript**: Use ESLint configuration
- **Documentation**: Update README for new features
- **Testing**: Add unit tests for new functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Malaysian Agricultural Research and Development Institute (MARDI)
- Federal Land Development Authority (FELDA)
- Malaysian Palm Oil Board (MPOB)
- Department of Agriculture Malaysia

## 📞 Support

- **Documentation**: Check API docs at `/docs`
- **Health Check**: Monitor at `/api/health`
- **Issues**: Report bugs via GitHub issues
- **Features**: Request features via GitHub discussions

## 🚀 Future Enhancements

- [ ] Machine learning crop predictions
- [ ] Drone integration for aerial monitoring
- [ ] Mobile app for field operations
- [ ] Blockchain for supply chain tracking
- [ ] AI-powered pest detection
- [ ] Weather station integration
- [ ] Automated irrigation scheduling
- [ ] Market price integration

---

**System Requirements**: Python 3.8+, Node.js 16+, 2GB RAM, 10GB storage, stable internet for real-time features.
