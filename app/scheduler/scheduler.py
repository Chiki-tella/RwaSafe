from apscheduler.schedulers.background import BackgroundScheduler
from app.services.simulation import SimulationService
from app.database.session import SessionLocal

def run_simulation_step():
    db = SessionLocal()
    try:
        sim = SimulationService(db)
        sim.generate_environmental_data()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run every 10 seconds as requested
    scheduler.add_job(run_simulation_step, 'interval', seconds=10)
    scheduler.start()
    return scheduler
