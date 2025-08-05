import React, { useState } from 'react';
import { farmApi } from '../services/api';

const PlotManagement = ({ farmData, onDataUpdate }) => {
  const [selectedPlot, setSelectedPlot] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleStatusUpdate = async (plotId, newStatus) => {
    try {
      setLoading(true);
      await farmApi.updatePlotStatus(plotId, newStatus);
      onDataUpdate();
      alert('Plot status updated successfully!');
    } catch (error) {
      console.error('Error updating plot status:', error);
      alert('Failed to update plot status');
    } finally {
      setLoading(false);
    }
  };

  const handleIrrigationToggle = async (plotId) => {
    try {
      setLoading(true);
      await farmApi.toggleIrrigation(plotId);
      onDataUpdate();
      alert('Irrigation status toggled successfully!');
    } catch (error) {
      console.error('Error toggling irrigation:', error);
      alert('Failed to toggle irrigation');
    } finally {
      setLoading(false);
    }
  };

  const getStatusOptions = () => ['active', 'maintenance', 'harvesting', 'idle'];

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-MY', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const calculateDaysToHarvest = (harvestDate) => {
    const today = new Date();
    const harvest = new Date(harvestDate);
    const diffTime = harvest - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  return (
    <div>
      <h2>Plot Management</h2>
      <p>Monitor and control individual farm plots with IoT-enabled management</p>

      <div className="dashboard-grid">
        {farmData.plots.map(plot => (
          <div key={plot.id} className="card plot-card">
            <div className="card-header">
              <h3 className="card-title">{plot.name}</h3>
              <span className={`plot-status status-${plot.status}`}>
                {plot.status}
              </span>
            </div>

            <div className="plot-details">
              <div className="detail-row">
                <span className="detail-label">Area:</span>
                <span>{plot.area} hectares</span>
              </div>
              
              <div className="detail-row">
                <span className="detail-label">Location:</span>
                <span>{plot.location.lat.toFixed(4)}, {plot.location.lng.toFixed(4)}</span>
              </div>

              {plot.crop && (
                <>
                  <div className="detail-row">
                    <span className="detail-label">Crop Type:</span>
                    <span>{plot.crop.type.replace('_', ' ').toUpperCase()}</span>
                  </div>
                  
                  <div className="detail-row">
                    <span className="detail-label">Variety:</span>
                    <span>{plot.crop.variety}</span>
                  </div>
                  
                  <div className="detail-row">
                    <span className="detail-label">Growth Stage:</span>
                    <span>{plot.crop.growth_stage}</span>
                  </div>
                  
                  <div className="detail-row">
                    <span className="detail-label">Planted:</span>
                    <span>{formatDate(plot.crop.planted_date)}</span>
                  </div>
                  
                  <div className="detail-row">
                    <span className="detail-label">Expected Harvest:</span>
                    <span>
                      {formatDate(plot.crop.expected_harvest)}
                      <br />
                      <small>({calculateDaysToHarvest(plot.crop.expected_harvest)} days)</small>
                    </span>
                  </div>
                  
                  <div className="detail-row">
                    <span className="detail-label">Yield Estimate:</span>
                    <span>{plot.crop.yield_estimate.toLocaleString()} kg/hectare</span>
                  </div>
                </>
              )}

              <div className="detail-row">
                <span className="detail-label">Irrigation:</span>
                <span>
                  {plot.irrigation_status ? '💧 Active' : '🚰 Inactive'}
                </span>
              </div>

              <div className="detail-row">
                <span className="detail-label">Sensors:</span>
                <span>{plot.sensors.length} active</span>
              </div>

              <div className="detail-row">
                <span className="detail-label">Equipment:</span>
                <span>{plot.equipment.length} units</span>
              </div>
            </div>

            {/* Equipment List */}
            <div className="equipment-list">
              <h4>Equipment</h4>
              {plot.equipment.map(equipment => (
                <div key={equipment.id} className="equipment-item">
                  <div>
                    <strong>{equipment.name}</strong>
                    <br />
                    <small>{equipment.type.replace('_', ' ').toUpperCase()}</small>
                  </div>
                  <span className={`equipment-status equipment-${equipment.status}`}>
                    {equipment.status}
                  </span>
                </div>
              ))}
            </div>

            {/* Control Panel */}
            <div className="control-panel">
              <select
                onChange={(e) => handleStatusUpdate(plot.id, e.target.value)}
                value={plot.status}
                disabled={loading}
                className="btn btn-secondary"
              >
                {getStatusOptions().map(status => (
                  <option key={status} value={status}>
                    {status.charAt(0).toUpperCase() + status.slice(1)}
                  </option>
                ))}
              </select>

              <button
                className={`btn ${plot.irrigation_status ? 'btn-warning' : 'btn-primary'}`}
                onClick={() => handleIrrigationToggle(plot.id)}
                disabled={loading}
              >
                {plot.irrigation_status ? '🚰 Stop Irrigation' : '💧 Start Irrigation'}
              </button>

              <button
                className="btn btn-secondary"
                onClick={() => setSelectedPlot(selectedPlot === plot.id ? null : plot.id)}
              >
                {selectedPlot === plot.id ? 'Hide Details' : 'View Details'}
              </button>
            </div>

            {/* Expanded Details */}
            {selectedPlot === plot.id && (
              <div className="card" style={{ marginTop: '1rem', backgroundColor: '#f8f9fa' }}>
                <h4>Detailed Information</h4>
                
                <div className="detail-row">
                  <span className="detail-label">Plot ID:</span>
                  <span>{plot.id}</span>
                </div>
                
                <div className="detail-row">
                  <span className="detail-label">Last Updated:</span>
                  <span>{new Date(plot.last_updated).toLocaleString()}</span>
                </div>

                {plot.crop && (
                  <>
                    <div className="detail-row">
                      <span className="detail-label">Crop ID:</span>
                      <span>{plot.crop.id}</span>
                    </div>
                    
                    <div className="detail-row">
                      <span className="detail-label">Days Since Planted:</span>
                      <span>
                        {Math.floor((new Date() - new Date(plot.crop.planted_date)) / (1000 * 60 * 60 * 24))} days
                      </span>
                    </div>
                  </>
                )}

                <h5>Equipment Details</h5>
                {plot.equipment.map(equipment => (
                  <div key={equipment.id} className="equipment-item">
                    <div>
                      <strong>{equipment.name}</strong> ({equipment.type})
                      <br />
                      <small>ID: {equipment.id}</small>
                      <br />
                      <small>Operational Hours: {equipment.operational_hours}h</small>
                      <br />
                      <small>Last Maintenance: {formatDate(equipment.last_maintenance)}</small>
                    </div>
                    <span className={`equipment-status equipment-${equipment.status}`}>
                      {equipment.status}
                    </span>
                  </div>
                ))}

                <h5>Sensor IDs</h5>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {plot.sensors.map(sensorId => (
                    <span key={sensorId} className="btn btn-small btn-secondary">
                      {sensorId.substring(0, 8)}...
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default PlotManagement;