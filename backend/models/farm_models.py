from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class CropType(str, Enum):
    RICE = "rice"
    PALM_OIL = "palm_oil"
    RUBBER = "rubber"
    DURIAN = "durian"
    BANANA = "banana"
    COCONUT = "coconut"

class EquipmentType(str, Enum):
    IRRIGATION = "irrigation"
    HARVESTER = "harvester"
    TRACTOR = "tractor"
    DRONE = "drone"
    SENSOR = "sensor"

class PlotStatus(str, Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    HARVESTING = "harvesting"
    IDLE = "idle"

class SensorReading(BaseModel):
    sensor_id: str
    timestamp: datetime
    temperature: float  # Celsius
    humidity: float     # Percentage
    soil_moisture: float  # Percentage
    ph_level: float
    light_intensity: float  # Lux
    rainfall: float     # mm

class Equipment(BaseModel):
    id: str
    name: str
    type: EquipmentType
    status: str
    location: Dict[str, float]  # lat, lng
    last_maintenance: datetime
    operational_hours: float

class Crop(BaseModel):
    id: str
    type: CropType
    variety: str
    planted_date: datetime
    expected_harvest: datetime
    growth_stage: str
    yield_estimate: float  # kg per hectare

class FarmPlot(BaseModel):
    id: str
    name: str
    location: Dict[str, float]  # lat, lng
    area: float  # hectares
    status: PlotStatus
    crop: Optional[Crop]
    equipment: List[Equipment]
    sensors: List[str]  # sensor IDs
    irrigation_status: bool
    last_updated: datetime

class Farm(BaseModel):
    id: str
    name: str
    location: str
    owner: str
    total_area: float  # hectares
    plots: List[FarmPlot]
    established_date: datetime