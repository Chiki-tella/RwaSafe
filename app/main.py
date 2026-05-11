from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api import router as api_router
from app.config.settings import settings
from app.database.session import SessionLocal, engine
from app.models.models import Base
from app.mock_data.seed import seed_db
from app.scheduler.scheduler import start_scheduler
import logging

# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend simulation for Rwanda's Landslide Early Warning System."
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables and seed DB
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        seed_db(db)
        logger.info("Database seeded successfully.")
    finally:
        db.close()
    
    # Start the background simulation
    start_scheduler()
    logger.info("Background simulation scheduler started.")

# Include Routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "status": "Running",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
