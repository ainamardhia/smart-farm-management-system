import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const farmApi = {
  // Farm operations
  getFarm: () => api.get('/farm'),
  
  // Plot operations
  getPlots: () => api.get('/plots'),
  getPlot: (plotId) => api.get(`/plots/${plotId}`),
  updatePlotStatus: (plotId, status) => api.put(`/plots/${plotId}/status`, { status }),
  toggleIrrigation: (plotId) => api.put(`/plots/${plotId}/irrigation`),
  
  // Sensor operations
  getLiveSensorData: () => api.get('/sensors/live'),
  getSensorData: (sensorId) => api.get(`/sensors/${sensorId}`),
  getAllSensorData: () => api.get('/sensors'),
};

export default api;