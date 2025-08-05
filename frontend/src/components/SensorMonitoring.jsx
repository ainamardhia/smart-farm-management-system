import React, { useState, useEffect } from 'react';
import { farmApi } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';

const SensorMonitoring = ({ farmData }) => {
  const [liveSensorData, setLiveSensorData] = useState([]);
  const [historicalData, setHistoricalData] = useState([]);
  const [selectedSensor, setSelectedSensor] = useState('');
  const [loading, setLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Get all unique sensor IDs from all plots
  const getAllSensorIds = () => {
    return farmData.plots.reduce((acc, plot) => {
      return [...acc, ...plot.sensors];
    }, []);
  };

  useEffect(() => {
    fetchLiveSensorData();
    fetchAllHistoricalData();
    
    let interval;
    if (autoRefresh) {
      interval = setInterval(fetchLiveSensorData, 15000); // Update every 15 seconds
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  useEffect(() => {
    if (selectedSensor) {
      fetchSensorHistory(selectedSensor);
    }
  }, [selectedSensor]);

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

  const fetchAllHistoricalData = async () => {
    try {
      const response = await farmApi.getAllSensorData();
      setHistoricalData(response.data);
    } catch (error) {
      console.error('Error fetching historical data:', error);
    }
  };

  const fetchSensorHistory = async (sensorId) => {
    try {
      const response = await farmApi.getSensorData(sensorId);
      setHistoricalData(response.data);
    } catch (error) {
      console.error('Error fetching sensor history:', error);
    }
  };

  const getSensorDataBySensor = () => {
    const sensorGroups = {};
    liveSensorData.forEach(reading => {
      if (!sensorGroups[reading.sensor_id]) {
        sensorGroups[reading.sensor_id] = [];
      }
      sensorGroups[reading.sensor_id].push(reading);
    });
    return sensorGroups;
  };

  const getAverageConditions = () => {
    if (liveSensorData.length === 0) return null;
    
    const totals = liveSensorData.reduce((acc, reading) => {
      acc.temperature += reading.temperature;
      acc.humidity += reading.humidity;
      acc.soil_moisture += reading.soil_moisture;
      acc.ph_level += reading.ph_level;
      acc.light_intensity += reading.light_intensity;
      acc.rainfall += reading.rainfall;
      return acc;
    }, {
      temperature: 0,
      humidity: 0,
      soil_moisture: 0,
      ph_level: 0,
      light_intensity: 0,
      rainfall: 0
    });

    const count = liveSensorData.length;
    return {
      temperature: (totals.temperature / count).toFixed(1),
      humidity: (totals.humidity / count).toFixed(1),
      soil_moisture: (totals.soil_moisture / count).toFixed(1),
      ph_level: (totals.ph_level / count).toFixed(1),
      light_intensity: Math.round(totals.light_intensity / count),
      rainfall: (totals.rainfall / count).toFixed(1)
    };
  };

  const getAlerts = () => {
    const alerts = [];
    liveSensorData.forEach(reading => {
      // Malaysian climate-specific thresholds
      if (reading.temperature > 38) {
        alerts.push({
          type: 'warning',
          sensor: reading.sensor_id,
          message: `High temperature: ${reading.temperature}°C`
        });
      }
      if (reading.humidity < 50) {
        alerts.push({
          type: 'warning',
          sensor: reading.sensor_id,
          message: `Low humidity: ${reading.humidity}%`
        });
      }
      if (reading.soil_moisture < 40) {
        alerts.push({
          type: 'danger',
          sensor: reading.sensor_id,
          message: `Low soil moisture: ${reading.soil_moisture}%`
        });
      }
      if (reading.ph_level < 5.0 || reading.ph_level > 8.0) {
        alerts.push({
          type: 'warning',
          sensor: reading.sensor_id,
          message: `pH level out of range: ${reading.ph_level}`
        });
      }
    });
    return alerts;
  };

  const prepareChartData = () => {
    return historicalData.slice(-24).map((reading, index) => ({
      time: new Date(reading.timestamp).toLocaleTimeString(),
      temperature: reading.temperature,
      humidity: reading.humidity,
      soil_moisture: reading.soil_moisture,
      ph_level: reading.ph_level,
      rainfall: reading.rainfall
    }));
  };

  const sensorGroups = getSensorDataBySensor();
  const averageConditions = getAverageConditions();
  const alerts = getAlerts();
  const chartData = prepareChartData();
  const allSensorIds = getAllSensorIds();

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h2>Sensor Monitoring</h2>
          <p>Real-time IoT sensor data from Malaysian farm conditions</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <label>
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            Auto-refresh
          </label>
          <button
            className="btn btn-primary"
            onClick={fetchLiveSensorData}
            disabled={loading}
          >
            {loading ? 'Updating...' : 'Refresh Data'}
          </button>
        </div>
      </div>

      {/* Average Conditions Overview */}
      {averageConditions && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <div className="card-header">
            <h3 className="card-title">🌡️ Current Farm Conditions (Average)</h3>
            <span>Last updated: {new Date().toLocaleTimeString()}</span>
          </div>
          <div className="sensor-grid">
            <div className="sensor-card">
              <div>Temperature</div>
              <div className="sensor-value" style={{ color: parseFloat(averageConditions.temperature) > 35 ? '#dc3545' : '#28a745' }}>
                {averageConditions.temperature}
              </div>
              <div className="sensor-unit">°C</div>
            </div>
            <div className="sensor-card">
              <div>Humidity</div>
              <div className="sensor-value" style={{ color: parseFloat(averageConditions.humidity) < 60 ? '#ffc107' : '#28a745' }}>
                {averageConditions.humidity}
              </div>
              <div className="sensor-unit">%</div>
            </div>
            <div className="sensor-card">
              <div>Soil Moisture</div>
              <div className="sensor-value" style={{ color: parseFloat(averageConditions.soil_moisture) < 50 ? '#dc3545' : '#28a745' }}>
                {averageConditions.soil_moisture}
              </div>
              <div className="sensor-unit">%</div>
            </div>
            <div className="sensor-card">
              <div>pH Level</div>
              <div className="sensor-value" style={{ color: parseFloat(averageConditions.ph_level) < 5.5 || parseFloat(averageConditions.ph_level) > 7.5 ? '#ffc107' : '#28a745' }}>
                {averageConditions.ph_level}
              </div>
              <div className="sensor-unit">pH</div>
            </div>
            <div className="sensor-card">
              <div>Light Intensity</div>
              <div className="sensor-value">
                {averageConditions.light_intensity.toLocaleString()}
              </div>
              <div className="sensor-unit">Lux</div>
            </div>
            <div className="sensor-card">
              <div>Rainfall</div>
              <div className="sensor-value" style={{ color: parseFloat(averageConditions.rainfall) > 20 ? '#17a2b8' : '#6c757d' }}>
                {averageConditions.rainfall}
              </div>
              <div className="sensor-unit">mm</div>
            </div>
          </div>
        </div>
      )}

      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="card" style={{ marginBottom: '2rem', borderLeft: '4px solid #dc3545' }}>
          <div className="card-header">
            <h3 className="card-title">⚠️ Active Alerts</h3>
          </div>
          {alerts.map((alert, index) => (
            <div key={index} className={`alert alert-${alert.type}`} style={{ 
              padding: '0.75rem', 
              margin: '0.5rem 0', 
              backgroundColor: alert.type === 'danger' ? '#f8d7da' : '#fff3cd',
              border: `1px solid ${alert.type === 'danger' ? '#f5c6cb' : '#ffeaa7'}`,
              borderRadius: '4px'
            }}>
              <strong>Sensor {alert.sensor.substring(0, 8)}:</strong> {alert.message}
            </div>
          ))}
        </div>
      )}

      {/* Historical Data Charts */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h3 className="card-title">📈 Historical Data Trends</h3>
          <select
            value={selectedSensor}
            onChange={(e) => setSelectedSensor(e.target.value)}
            className="btn btn-secondary"
          >
            <option value="">All Sensors</option>
            {allSensorIds.map(sensorId => (
              <option key={sensorId} value={sensorId}>
                Sensor {sensorId.substring(0, 8)}...
              </option>
            ))}
          </select>
        </div>
        
        {chartData.length > 0 ? (
          <div>
            {/* Temperature and Humidity Chart */}
            <div className="chart-container">
              <h4>Temperature & Humidity</h4>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="temperature" stroke="#dc143c" name="Temperature (°C)" />
                  <Line type="monotone" dataKey="humidity" stroke="#17a2b8" name="Humidity (%)" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Soil Conditions Chart */}
            <div className="chart-container">
              <h4>Soil Conditions</h4>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="soil_moisture" stroke="#28a745" name="Soil Moisture (%)" />
                  <Line type="monotone" dataKey="ph_level" stroke="#ffc107" name="pH Level" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Rainfall Chart */}
            <div className="chart-container">
              <h4>Rainfall</h4>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="rainfall" fill="#007bff" name="Rainfall (mm)" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        ) : (
          <p>No historical data available</p>
        )}
      </div>

      {/* Individual Sensor Readings */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">📡 Individual Sensor Readings</h3>
          <span>{Object.keys(sensorGroups).length} sensors active</span>
        </div>
        
        <div className="dashboard-grid">
          {Object.entries(sensorGroups).map(([sensorId, readings]) => {
            const latestReading = readings[readings.length - 1];
            return (
              <div key={sensorId} className="card" style={{ backgroundColor: '#f8f9fa' }}>
                <div className="card-header">
                  <h4 className="card-title">Sensor {sensorId.substring(0, 8)}...</h4>
                  <span className="btn btn-small btn-success">Online</span>
                </div>
                
                <div className="sensor-grid">
                  <div className="sensor-card">
                    <div>Temp</div>
                    <div className="sensor-value">{latestReading.temperature}</div>
                    <div className="sensor-unit">°C</div>
                  </div>
                  <div className="sensor-card">
                    <div>Humidity</div>
                    <div className="sensor-value">{latestReading.humidity}</div>
                    <div className="sensor-unit">%</div>
                  </div>
                  <div className="sensor-card">
                    <div>Soil</div>
                    <div className="sensor-value">{latestReading.soil_moisture}</div>
                    <div className="sensor-unit">%</div>
                  </div>
                  <div className="sensor-card">
                    <div>pH</div>
                    <div className="sensor-value">{latestReading.ph_level}</div>
                    <div className="sensor-unit">pH</div>
                  </div>
                </div>
                
                <div className="detail-row">
                  <span className="detail-label">Last Reading:</span>
                  <span>{new Date(latestReading.timestamp).toLocaleTimeString()}</span>
                </div>
                
                <button
                  className="btn btn-small btn-primary"
                  onClick={() => setSelectedSensor(sensorId)}
                  style={{ marginTop: '0.5rem' }}
                >
                  View History
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default SensorMonitoring;