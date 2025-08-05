import React, { useState, useEffect } from 'react';
import { farmApi } from '../services/api';

const Dashboard = ({ farmData, onDataUpdate }) => {
  const [liveSensorData, setLiveSensorData] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchLiveSensorData();
    const interval = setInterval(fetchLiveSensorData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchLiveSensorData = async () => {
    try {
      setLoading(true);
      const response = await farmApi.getLiveSensorData();
      setLiveSensorData(response.data);
    } catch (error) {
      console.error('Error fetching live sensor data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPlotStatusSummary = () => {
    const statusCounts = farmData.plots.reduce((acc, plot) => {
      acc[plot.status] = (acc[plot.status] || 0) + 1;
      return acc;
    }, {});
    return statusCounts;
  };

  const getCropSummary = () => {
    const cropCounts = farmData.plots.reduce((acc, plot) => {
      if (plot.crop) {
        acc[plot.crop.type] = (acc[plot.crop.type] || 0) + 1;
      }
      return acc;
    }, {});
    return cropCounts;
  };

  const getAverageWeatherData = () => {
    if (liveSensorData.length === 0) return null;
    
    const totals = liveSensorData.reduce((acc, reading) => {
      acc.temperature += reading.temperature;
      acc.humidity += reading.humidity;
      acc.soil_moisture += reading.soil_moisture;
      acc.rainfall += reading.rainfall;
      return acc;
    }, { temperature: 0, humidity: 0, soil_moisture: 0, rainfall: 0 });

    const count = liveSensorData.length;
    return {
      temperature: (totals.temperature / count).toFixed(1),
      humidity: (totals.humidity / count).toFixed(1),
      soil_moisture: (totals.soil_moisture / count).toFixed(1),
      rainfall: (totals.rainfall / count).toFixed(1)
    };
  };

  const statusSummary = getPlotStatusSummary();
  const cropSummary = getCropSummary();
  const weatherData = getAverageWeatherData();

  return (
    <div>
      <h2>Farm Dashboard Overview</h2>
      <p>Real-time monitoring of your Malaysian agricultural operations</p>

      <div className="dashboard-grid">
        {/* Farm Statistics */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">🏡 Farm Statistics</h3>
          </div>
          <div className="detail-row">
            <span className="detail-label">Total Plots:</span>
            <span>{farmData.plots.length}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Total Area:</span>
            <span>{farmData.total_area.toFixed(2)} hectares</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Established:</span>
            <span>{new Date(farmData.established_date).getFullYear()}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Location:</span>
            <span>{farmData.location}</span>
          </div>
        </div>

        {/* Plot Status Summary */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">📊 Plot Status Summary</h3>
          </div>
          {Object.entries(statusSummary).map(([status, count]) => (
            <div key={status} className="detail-row">
              <span className="detail-label">
                <span className={`plot-status status-${status}`}>
                  {status.charAt(0).toUpperCase() + status.slice(1)}
                </span>
              </span>
              <span>{count} plots</span>
            </div>
          ))}
        </div>

        {/* Crop Distribution */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">🌾 Crop Distribution</h3>
          </div>
          {Object.entries(cropSummary).map(([crop, count]) => (
            <div key={crop} className="detail-row">
              <span className="detail-label">
                {crop.replace('_', ' ').toUpperCase()}:
              </span>
              <span>{count} plots</span>
            </div>
          ))}
        </div>

        {/* Weather Overview */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">🌡️ Current Weather Conditions</h3>
            <button 
              className="btn btn-small btn-primary" 
              onClick={fetchLiveSensorData}
              disabled={loading}
            >
              {loading ? 'Updating...' : 'Refresh'}
            </button>
          </div>
          {weatherData ? (
            <div className="sensor-grid">
              <div className="sensor-card">
                <div>Temperature</div>
                <div className="sensor-value">{weatherData.temperature}</div>
                <div className="sensor-unit">°C</div>
              </div>
              <div className="sensor-card">
                <div>Humidity</div>
                <div className="sensor-value">{weatherData.humidity}</div>
                <div className="sensor-unit">%</div>
              </div>
              <div className="sensor-card">
                <div>Soil Moisture</div>
                <div className="sensor-value">{weatherData.soil_moisture}</div>
                <div className="sensor-unit">%</div>
              </div>
              <div className="sensor-card">
                <div>Rainfall</div>
                <div className="sensor-value">{weatherData.rainfall}</div>
                <div className="sensor-unit">mm</div>
              </div>
            </div>
          ) : (
            <p>No sensor data available</p>
          )}
        </div>
      </div>

      {/* Recent Plot Activities */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">📋 Recent Plot Activities</h3>
        </div>
        <div className="dashboard-grid">
          {farmData.plots.slice(0, 3).map(plot => (
            <div key={plot.id} className="plot-card">
              <h4>{plot.name}</h4>
              <div className="detail-row">
                <span className="detail-label">Status:</span>
                <span className={`plot-status status-${plot.status}`}>
                  {plot.status}
                </span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Area:</span>
                <span>{plot.area} hectares</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Crop:</span>
                <span>{plot.crop ? plot.crop.type.replace('_', ' ') : 'None'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Irrigation:</span>
                <span>{plot.irrigation_status ? '💧 Active' : '🚰 Inactive'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Last Updated:</span>
                <span>{new Date(plot.last_updated).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;