import React, { useState, useEffect } from 'react';
import { farmApi } from './services/api';
import Dashboard from './components/Dashboard';
import PlotManagement from './components/PlotManagement';
import SensorMonitoring from './components/SensorMonitoring';
import FarmMap from './components/FarmMap';
import './App.css'; // Changed from './styles/App.css'

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [farmData, setFarmData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadFarmData();
  }, []);

  const loadFarmData = async () => {
    try {
      setLoading(true);
      const response = await farmApi.getFarm();
      setFarmData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load farm data');
      console.error('Error loading farm data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDataUpdate = () => {
    loadFarmData();
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <h2>Loading Smart Farm Management System...</h2>
          <p>Fetching data from Malaysian farm operations</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">
          <h2>Error</h2>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={loadFarmData}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>🌾 Smart Farm Management System</h1>
          <div className="header-info">
            <div>
              <span className="flag-icon"></span>
              {farmData?.name} - {farmData?.location}
            </div>
            <div>Owner: {farmData?.owner}</div>
            <div>Total Area: {farmData?.total_area?.toFixed(2)} hectares</div>
          </div>
        </div>
      </header>

      <nav className="nav">
        <div className="nav-content">
          <button
            className={`nav-button ${currentView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentView('dashboard')}
          >
            📊 Dashboard
          </button>
          <button
            className={`nav-button ${currentView === 'plots' ? 'active' : ''}`}
            onClick={() => setCurrentView('plots')}
          >
            🌱 Plot Management
          </button>
          <button
            className={`nav-button ${currentView === 'sensors' ? 'active' : ''}`}
            onClick={() => setCurrentView('sensors')}
          >
            📡 Sensor Monitoring
          </button>
          <button
            className={`nav-button ${currentView === 'map' ? 'active' : ''}`}
            onClick={() => setCurrentView('map')}
          >
            🗺️ Farm Map
          </button>
        </div>
      </nav>

      <main className="main-content">
        {currentView === 'dashboard' && (
          <Dashboard farmData={farmData} onDataUpdate={handleDataUpdate} />
        )}
        {currentView === 'plots' && (
          <PlotManagement farmData={farmData} onDataUpdate={handleDataUpdate} />
        )}
        {currentView === 'sensors' && (
          <SensorMonitoring farmData={farmData} />
        )}
        {currentView === 'map' && (
          <FarmMap farmData={farmData} />
        )}
      </main>
    </div>
  );
}

export default App;