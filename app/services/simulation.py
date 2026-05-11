import random
import datetime
from sqlalchemy.orm import Session
from app.models.models import Sector, EnvironmentalData, Alert, SMSLog, Recipient, RiskLevel, SystemLog
from app.services.risk_engine import RiskEngine
from app.config.settings import settings

class SimulationService:
    def __init__(self, db: Session):
        self.db = db

    def generate_environmental_data(self):
        sectors = self.db.query(Sector).all()
        for sector in sectors:
            # Simulate realistic fluctuations
            # Get last reading to make it gradual
            last_data = self.db.query(EnvironmentalData)\
                .filter(EnvironmentalData.sector_id == sector.id)\
                .order_by(EnvironmentalData.timestamp.desc())\
                .first()

            if last_data:
                # Rainfall varies by +/- 10mm, min 0, max 250
                rainfall = max(0, min(250, last_data.rainfall_mm + random.uniform(-10, 15)))
                # Moisture follows rainfall but slower
                moisture = max(0, min(100, last_data.soil_moisture_percent + (rainfall * 0.05) - 2))
                # Displacement increases if moisture > 70%
                disp_delta = 0.5 if moisture > 70 else -0.2
                displacement = max(0, min(10, last_data.displacement_score + disp_delta + random.uniform(-0.1, 0.1)))
                veg_index = max(0.1, min(1.0, last_data.vegetation_index + random.uniform(-0.01, 0.01)))
            else:
                # Initial values
                rainfall = random.uniform(0, 50)
                moisture = random.uniform(20, 60)
                displacement = random.uniform(0, 2)
                veg_index = random.uniform(0.6, 0.9)

            new_data = EnvironmentalData(
                sector_id=sector.id,
                rainfall_mm=round(rainfall, 2),
                soil_moisture_percent=round(moisture, 2),
                displacement_score=round(displacement, 2),
                vegetation_index=round(veg_index, 2),
                slope_factor=sector.slope_factor,
                confidence_score=round(random.uniform(0.85, 0.99), 2),
                timestamp=datetime.datetime.utcnow()
            )
            self.db.add(new_data)
            self.db.flush()

            # Process Risk
            risk_level, risk_score, explanation = RiskEngine.calculate_risk(
                new_data.rainfall_mm,
                new_data.soil_moisture_percent,
                new_data.displacement_score,
                new_data.slope_factor
            )

            # Update Sector
            old_level = sector.current_risk_level
            sector.current_risk_level = risk_level
            sector.current_risk_score = round(risk_score, 2)
            sector.last_updated = datetime.datetime.utcnow()

            # Trigger Alert if level changed to HIGH or CRITICAL or if it's already critical and we want to refresh
            if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL] and risk_level != old_level:
                self.trigger_alert(sector, risk_level, explanation)

        self.db.commit()

    def trigger_alert(self, sector: Sector, level: str, explanation: str):
        # Create Alert
        msg_en = f"[RWASAFE ALERT] {level} LANDSLIDE RISK – {sector.name} Sector. {explanation} Avoid steep slopes."
        
        # Simple Kinyarwanda translation mock
        rw_level = "IBYAGO BYINSHI" if level == RiskLevel.HIGH else "IBYAGO BYIHUTIRWA"
        msg_rw = f"[RWASAFE] IMPANUKA: {rw_level} byo gusunikwa kw'ubutaka mu {sector.name}. {explanation} Irinde ahantu hateganye."

        new_alert = Alert(
            sector_id=sector.id,
            risk_level=level,
            message_en=msg_en,
            message_rw=msg_rw,
            explanation=explanation,
            timestamp=datetime.datetime.utcnow(),
            status="ACTIVE"
        )
        self.db.add(new_alert)
        self.db.flush()

        # Simulate SMS Dispatch
        self.dispatch_sms(new_alert)

    def dispatch_sms(self, alert: Alert):
        # Get recipients for this sector
        recipients = self.db.query(Recipient).filter(Recipient.sector_id == alert.sector_id).all()
        
        for recipient in recipients:
            # Primary provider: Africa's Talking
            success = random.random() < settings.SMS_SUCCESS_RATE
            provider = "Africa's Talking"
            status = "SENT" if success else "FAILED"
            
            sms_log = SMSLog(
                alert_id=alert.id,
                recipient=recipient.phone_number,
                provider=provider,
                message=alert.message_en,
                status=status,
                timestamp=datetime.datetime.utcnow()
            )
            self.db.add(sms_log)
            self.db.flush()

            if status == "FAILED":
                # Failover to Twilio
                retry_success = random.random() < 0.95 # Higher success on failover
                retry_log = SMSLog(
                    alert_id=alert.id,
                    recipient=recipient.phone_number,
                    provider="Twilio (Failover)",
                    message=alert.message_en,
                    status="SENT" if retry_success else "FAILED",
                    retry_count=1,
                    timestamp=datetime.datetime.utcnow()
                )
                self.db.add(retry_log)
                
        # Log system event
        sys_log = SystemLog(
            level="INFO",
            message=f"Alert generated for {alert.sector_id}: {alert.risk_level}",
            component="AlertService",
            timestamp=datetime.datetime.utcnow()
        )
        self.db.add(sys_log)
