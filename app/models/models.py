from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base
import datetime
import enum

class RiskLevel(str, enum.Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class SMSStatus(str, enum.Enum):
    SENT = "SENT"
    FAILED = "FAILED"
    RETRYING = "RETRYING"

class Sector(Base):
    __tablename__ = "sectors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    province = Column(String)
    slope_factor = Column(Float)
    population_estimate = Column(Integer)
    current_risk_level = Column(String, default="LOW")
    current_risk_score = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    environmental_data = relationship("EnvironmentalData", back_populates="sector")
    alerts = relationship("Alert", back_populates="sector")

class EnvironmentalData(Base):
    __tablename__ = "environmental_data"

    id = Column(Integer, primary_key=True, index=True)
    sector_id = Column(Integer, ForeignKey("sectors.id"))
    rainfall_mm = Column(Float)
    soil_moisture_percent = Column(Float)
    displacement_score = Column(Float)
    vegetation_index = Column(Float)
    slope_factor = Column(Float)
    confidence_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    sector = relationship("Sector", back_populates="environmental_data")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    sector_id = Column(Integer, ForeignKey("sectors.id"))
    risk_level = Column(String)
    message_en = Column(String)
    message_rw = Column(String)
    explanation = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="ACTIVE") # ACTIVE, RESOLVED

    sector = relationship("Sector", back_populates="alerts")
    sms_logs = relationship("SMSLog", back_populates="alert")

class SMSLog(Base):
    __tablename__ = "sms_logs"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    recipient = Column(String)
    provider = Column(String) # Africa's Talking, Twilio
    message = Column(String)
    status = Column(String)
    retry_count = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    alert = relationship("Alert", back_populates="sms_logs")

class Recipient(Base):
    __tablename__ = "recipients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_number = Column(String)
    sector_id = Column(Integer, ForeignKey("sectors.id"))

class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String) # INFO, WARNING, ERROR, CRITICAL
    message = Column(String)
    component = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class ThresholdConfiguration(Base):
    __tablename__ = "threshold_configurations"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    value = Column(Float)
    description = Column(String)
