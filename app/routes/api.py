from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.models import Sector, EnvironmentalData, Alert, SMSLog, ThresholdConfiguration, SystemLog, RiskLevel
from app.schemas.schemas import SectorSchema, EnvironmentalDataSchema, AlertSchema, DashboardStats, ThresholdUpdate
import datetime

router = APIRouter()

@router.get("/sectors", response_model=List[SectorSchema])
def get_sectors(db: Session = Depends(get_db)):
    return db.query(Sector).all()

@router.get("/sectors/{sector_id}", response_model=SectorSchema)
def get_sector(sector_id: int, db: Session = Depends(get_db)):
    sector = db.query(Sector).filter(Sector.id == sector_id).first()
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")
    return sector

@router.get("/environment/latest", response_model=List[EnvironmentalDataSchema])
def get_latest_environment(db: Session = Depends(get_db)):
    # Get latest reading for each sector
    sectors = db.query(Sector).all()
    latest_readings = []
    for sector in sectors:
        reading = db.query(EnvironmentalData)\
            .filter(EnvironmentalData.sector_id == sector.id)\
            .order_by(EnvironmentalData.timestamp.desc())\
            .first()
        if reading:
            latest_readings.append(reading)
    return latest_readings

@router.get("/alerts", response_model=List[AlertSchema])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(Alert.timestamp.desc()).all()

@router.get("/alerts/active", response_model=List[AlertSchema])
def get_active_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).filter(Alert.risk_level.in_([RiskLevel.HIGH, RiskLevel.CRITICAL])).all()

@router.get("/history/{sector_id}", response_model=List[EnvironmentalDataSchema])
def get_sector_history(sector_id: int, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(EnvironmentalData)\
        .filter(EnvironmentalData.sector_id == sector_id)\
        .order_by(EnvironmentalData.timestamp.desc())\
        .limit(limit)\
        .all()

@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_sectors = db.query(Sector).count()
    active_alerts = db.query(Alert).filter(Alert.status == "ACTIVE").count()
    critical_sectors = db.query(Sector).filter(Sector.current_risk_level == RiskLevel.CRITICAL).count()
    sms_sent = db.query(SMSLog).filter(SMSLog.status == "SENT").count()
    
    # Simple average rainfall in last hour
    hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    avg_rainfall = db.query(EnvironmentalData).filter(EnvironmentalData.timestamp >= hour_ago).all()
    avg_rainfall_val = sum(d.rainfall_mm for d in avg_rainfall) / len(avg_rainfall) if avg_rainfall else 0.0
    
    avg_risk_score = db.query(Sector).all()
    avg_risk_val = sum(s.current_risk_score for s in avg_risk_score) / total_sectors if total_sectors else 0.0

    return {
        "total_sectors": total_sectors,
        "active_alerts": active_alerts,
        "critical_sectors": critical_sectors,
        "sms_sent": sms_sent,
        "system_uptime_seconds": 3600, # Mocked
        "average_rainfall": round(avg_rainfall_val, 2),
        "average_risk_score": round(avg_risk_val, 2)
    }

@router.post("/admin/thresholds")
def update_threshold(update: ThresholdUpdate, db: Session = Depends(get_db)):
    threshold = db.query(ThresholdConfiguration).filter(ThresholdConfiguration.key == update.key).first()
    if not threshold:
        raise HTTPException(status_code=404, detail="Threshold not found")
    threshold.value = update.value
    db.commit()
    return {"message": "Threshold updated successfully"}

@router.get("/system/health")
def system_health(db: Session = Depends(get_db)):
    # Check DB
    try:
        db.execute("SELECT 1")
        db_status = "HEALTHY"
    except Exception:
        db_status = "UNHEALTHY"
        
    return {
        "status": "OPERATIONAL",
        "database": db_status,
        "simulation_engine": "ACTIVE",
        "alert_system": "ONLINE",
        "timestamp": datetime.datetime.utcnow()
    }
