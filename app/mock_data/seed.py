from sqlalchemy.orm import Session
from app.models.models import Sector, Recipient, ThresholdConfiguration, Base
from app.database.session import engine

def seed_db(db: Session):
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Check if sectors exist
    if db.query(Sector).first():
        return

    # Seed Sectors
    sectors = [
        Sector(name="Rubavu", province="Western", slope_factor=8.5, population_estimate=150000),
        Sector(name="Rutsiro", province="Western", slope_factor=9.2, population_estimate=120000),
        Sector(name="Nyabihu", province="Western", slope_factor=7.8, population_estimate=130000),
        Sector(name="Musanze", province="Northern", slope_factor=8.0, population_estimate=180000),
        Sector(name="Burera", province="Northern", slope_factor=7.5, population_estimate=110000),
    ]
    db.add_all(sectors)
    db.commit()

    # Seed Recipients
    db_sectors = db.query(Sector).all()
    recipients = []
    for sector in db_sectors:
        recipients.append(Recipient(name=f"Admin {sector.name}", phone_number=f"+250780000{sector.id:02d}", sector_id=sector.id))
        recipients.append(Recipient(name=f"Emergency Response {sector.name}", phone_number=f"+250781111{sector.id:02d}", sector_id=sector.id))
    
    db.add_all(recipients)
    
    # Seed Thresholds
    thresholds = [
        ThresholdConfiguration(key="rainfall_high", value=100.0, description="Rainfall threshold for HIGH risk"),
        ThresholdConfiguration(key="soil_moisture_high", value=80.0, description="Soil moisture threshold for HIGH risk"),
        ThresholdConfiguration(key="displacement_high", value=5.0, description="Displacement threshold for HIGH risk"),
    ]
    db.add_all(thresholds)
    
    db.commit()
