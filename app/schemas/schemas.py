from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.models import RiskLevel, SMSStatus

class SectorBase(BaseModel):
    name: str
    province: str
    slope_factor: float
    population_estimate: int

class SectorCreate(SectorBase):
    pass

class SectorSchema(SectorBase):
    id: int
    current_risk_level: str
    current_risk_score: float
    last_updated: datetime

    class Config:
        from_attributes = True

class EnvironmentalDataBase(BaseModel):
    sector_id: int
    rainfall_mm: float
    soil_moisture_percent: float
    displacement_score: float
    vegetation_index: float
    slope_factor: float
    confidence_score: float

class EnvironmentalDataCreate(EnvironmentalDataBase):
    pass

class EnvironmentalDataSchema(EnvironmentalDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    sector_id: int
    risk_level: str
    message_en: str
    message_rw: str
    explanation: str
    status: str

class AlertSchema(AlertBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class SMSLogSchema(BaseModel):
    id: int
    alert_id: int
    recipient: str
    provider: str
    message: str
    status: str
    retry_count: int
    timestamp: datetime

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_sectors: int
    active_alerts: int
    critical_sectors: int
    sms_sent: int
    system_uptime_seconds: int
    average_rainfall: float
    average_risk_score: float

class ThresholdUpdate(BaseModel):
    key: str
    value: float
