from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "RwaSafe Landslide Early Warning System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = "sqlite:///./rwasafe.db"
    
    # Simulation Settings
    SIMULATION_INTERVAL_SECONDS: int = 10
    
    # Risk Thresholds
    THRESHOLD_RAINFALL_HIGH: float = 100.0
    THRESHOLD_MOISTURE_HIGH: float = 80.0
    THRESHOLD_DISPLACEMENT_HIGH: float = 5.0
    
    # SMS Simulation
    SMS_SUCCESS_RATE: float = 0.90
    
    # Rwandan Sectors
    MONITORED_SECTORS: List[str] = ["Rubavu", "Rutsiro", "Nyabihu", "Musanze", "Burera"]

    class Config:
        case_sensitive = True

settings = Settings()
