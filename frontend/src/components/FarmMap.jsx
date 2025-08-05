import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const FarmMap = ({ farmData }) => {
  const [selectedPlot, setSelectedPlot] = useState(null);
  const [mapView, setMapView] = useState('plots'); // 'plots', 'equipment', 'sensors'

  // Calculate farm center coordinates
  const getFarmCenter = () => {
    if (farmData.plots.length === 0) return [4.2105, 101.9758]; // Default to Malaysia center
    
    const avgLat = farmData.plots.reduce((sum, plot) => sum + plot.location.lat, 0) / farmData.plots.length;
    const avgLng = farmData.plots.reduce((sum, plot) => sum + plot.location.lng, 0) / farmData.plots.length;
    
    return [avgLat, avgLng];
  };

  // Create custom icons for different elements
  const createCustomIcon = (color, symbol) => {
    return L.divIcon({
      className: 'custom-marker',
      html: `<div style="
        background-color: ${color};
        width: 30px;
        height: 30px;
        border-radius: 50%;
        border: 3px solid white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
      ">${symbol}</div>`,
      iconSize: [30, 30],
      iconAnchor: [15, 15]
    });
  };

  const getPlotIcon = (plot) => {
    const statusColors = {
      active: '#28a745',
      maintenance: '#ffc107',
      harvesting: '#17a2b8',
      idle: '#6c757d'
    };
    return createCustomIcon(statusColors[plot.status] || '#6c757d', '🌱');
  };

  const getEquipmentIcon = (equipment) => {
    const typeIcons = {
      irrigation: '💧',
      tractor: '🚜',
      drone: '🚁',
      sensor: '📡',
      harvester: '🌾'
    };
    return createCustomIcon('#dc143c', typeIcons[equipment.type] || '🔧');
  };

  const getStatusColor = (status) => {
    const colors = {
      active: '#28a745',
      maintenance: '#ffc107',
      harvesting: '#17a2b8',
      idle: '#6c757d',
      operational: '#28a745'
    };
    return colors[status] || '#6c757d';
  };

  const farmCenter = getFarmCenter();

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <div>
          <h2>🗺️ Farm Map</h2>
          <p>Geospatial view of {farmData.name} with IoT device locations</p>
        </div>
        
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            className={`btn ${mapView === 'plots' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setMapView('plots')}
          >
            🌱 Plots
          </button>
          <button
            className={`btn ${mapView === 'equipment' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setMapView('equipment')}
          >
            🚜 Equipment
          </button>
          <button
            className={`btn ${mapView === 'sensors' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setMapView('sensors')}
          >
            📡 Sensors
          </button>
        </div>
      </div>

      <div className="card">
        <div className="map-container">
          <MapContainer
            center={farmCenter}
            zoom={15}
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />

            {/* Plot Markers and Areas */}
            {(mapView === 'plots' || mapView === 'sensors') && farmData.plots.map(plot => (
              <React.Fragment key={plot.id}>
                <Marker
                  position={[plot.location.lat, plot.location.lng]}
                  icon={getPlotIcon(plot)}
                  eventHandlers={{
                    click: () => setSelectedPlot(selectedPlot === plot.id ? null : plot.id)
                  }}
                >
                  <Popup>
                    <div style={{ minWidth: '200px' }}>
                      <h4>{plot.name}</h4>
                      <p><strong>Status:</strong> {plot.status}</p>
                      <p><strong>Area:</strong> {plot.area} hectares</p>
                      {plot.crop && (
                        <p><strong>Crop:</strong> {plot.crop.type.replace('_', ' ')}</p>
                      )}
                      <p><strong>Irrigation:</strong> {plot.irrigation_status ? 'Active' : 'Inactive'}</p>
                      <p><strong>Equipment:</strong> {plot.equipment.length} units</p>
                      <p><strong>Sensors:</strong> {plot.sensors.length} active</p>
                    </div>
                  </Popup>
                </Marker>

                {/* Plot area circle */}
                <Circle
                  center={[plot.location.lat, plot.location.lng]}
                  radius={Math.sqrt(plot.area * 10000) / 2} // Convert hectares to approximate radius
                  color={getStatusColor(plot.status)}
                  fillColor={getStatusColor(plot.status)}
                  fillOpacity={0.2}
                  weight={2}
                />

                {/* Sensor markers for selected plot */}
                {mapView === 'sensors' && selectedPlot === plot.id && plot.sensors.map((sensorId, index) => {
                  // Generate approximate positions around the plot
                  const offsetLat = (Math.random() - 0.5) * 0.001;
                  const offsetLng = (Math.random() - 0.5) * 0.001;
                  return (
                    <Marker
                      key={sensorId}
                      position={[plot.location.lat + offsetLat, plot.location.lng + offsetLng]}
                      icon={createCustomIcon('#17a2b8', '📡')}
                    >
                      <Popup>
                        <div>
                          <h5>Sensor {sensorId.substring(0, 8)}...</h5>
                          <p><strong>Plot:</strong> {plot.name}</p>
                          <p><strong>Type:</strong> Environmental Sensor</p>
                          <p><strong>Status:</strong> Active</p>
                        </div>
                      </Popup>
                    </Marker>
                  );
                })}
              </React.Fragment>
            ))}

            {/* Equipment Markers */}
            {mapView === 'equipment' && farmData.plots.map(plot =>
              plot.equipment.map(equipment => (
                <Marker
                  key={equipment.id}
                  position={[equipment.location.lat, equipment.location.lng]}
                  icon={getEquipmentIcon(equipment)}
                >
                  <Popup>
                    <div style={{ minWidth: '200px' }}>
                      <h4>{equipment.name}</h4>
                      <p><strong>Type:</strong> {equipment.type.replace('_', ' ').toUpperCase()}</p>
                      <p><strong>Status:</strong> {equipment.status}</p>
                      <p><strong>Plot:</strong> {plot.name}</p>
                      <p><strong>Operational Hours:</strong> {equipment.operational_hours}h</p>
                      <p><strong>Last Maintenance:</strong> {new Date(equipment.last_maintenance).toLocaleDateString()}</p>
                    </div>
                  </Popup>
                </Marker>
              ))
            )}
          </MapContainer>
        </div>
      </div>

      {/* Map Legend */}
      <div className="card" style={{ marginTop: '1rem' }}>
        <h4>Map Legend</h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          {mapView === 'plots' && (
            <div>
              <h5>Plot Status</h5>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '20px', height: '20px', backgroundColor: '#28a745', borderRadius: '50%' }}></div>
                  <span>Active</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '20px', height: '20px', backgroundColor: '#ffc107', borderRadius: '50%' }}></div>
                  <span>Maintenance</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '20px', height: '20px', backgroundColor: '#17a2b8', borderRadius: '50%' }}></div>
                  <span>Harvesting</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '20px', height: '20px', backgroundColor: '#6c757d', borderRadius: '50%' }}></div>
                  <span>Idle</span>
                </div>
              </div>
            </div>
          )}

          {mapView === 'equipment' && (
            <div>
              <h5>Equipment Types</h5>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '20px' }}>🚜</span>
                  <span>Tractor</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '20px' }}>💧</span>
                  <span>Irrigation</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '20px' }}>🚁</span>
                  <span>Drone</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '20px' }}>🌾</span>
                  <span>Harvester</span>
                </div>
              </div>
            </div>
          )}

          {mapView === 'sensors' && (
            <div>
              <h5>Sensor Network</h5>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '20px' }}>📡</span>
                  <span>Environmental Sensors</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '20px' }}>🌱</span>
                  <span>Plot Center</span>
                </div>
              </div>
              <p style={{ fontSize: '0.9rem', marginTop: '0.5rem', color: '#6c757d' }}>
                Click on a plot to show its sensors
              </p>
            </div>
          )}

          <div>
            <h5>Farm Information</h5>
            <p><strong>Location:</strong> {farmData.location}</p>
            <p><strong>Total Area:</strong> {farmData.total_area.toFixed(2)} hectares</p>
            <p><strong>Total Plots:</strong> {farmData.plots.length}</p>
            <p><strong>Coordinates:</strong> {farmCenter[0].toFixed(4)}, {farmCenter[1].toFixed(4)}</p>
          </div>
        </div>
      </div>

      {/* Selected Plot Details */}
      {selectedPlot && (
        <div className="card" style={{ marginTop: '1rem', borderLeft: '4px solid #dc143c' }}>
          <h4>Selected Plot Details</h4>
          {farmData.plots
            .filter(plot => plot.id === selectedPlot)
            .map(plot => (
              <div key={plot.id}>
                <div className="dashboard-grid">
                  <div>
                    <h5>{plot.name}</h5>
                    <div className="detail-row">
                      <span className="detail-label">Status:</span>
                      <span className={`plot-status status-${plot.status}`}>{plot.status}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Area:</span>
                      <span>{plot.area} hectares</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Coordinates:</span>
                      <span>{plot.location.lat.toFixed(6)}, {plot.location.lng.toFixed(6)}</span>
                    </div>
                  </div>
                  
                  {plot.crop && (
                    <div>
                      <h5>Crop Information</h5>
                      <div className="detail-row">
                        <span className="detail-label">Type:</span>
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
                    </div>
                  )}
                  
                  <div>
                    <h5>IoT Devices</h5>
                    <div className="detail-row">
                      <span className="detail-label">Equipment:</span>
                      <span>{plot.equipment.length} units</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Sensors:</span>
                      <span>{plot.sensors.length} active</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Irrigation:</span>
                      <span>{plot.irrigation_status ? '💧 Active' : '🚰 Inactive'}</span>
                    </div>
                  </div>
                </div>
                
                <button
                  className="btn btn-secondary"
                  onClick={() => setSelectedPlot(null)}
                  style={{ marginTop: '1rem' }}
                >
                  Close Details
                </button>
              </div>
            ))}
        </div>
      )}
    </div>
  );
};

export default FarmMap;