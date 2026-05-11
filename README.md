# RwaSafe: Satellite-Based Landslide Early Warning System

RwaSafe is a high-fidelity backend simulation for a landslide monitoring and alerting platform tailored for Rwanda's high-risk sectors. It leverages mock satellite data (NASA SMAP, Sentinel-1/2, CHIRPS) to predict landslide risks and automate emergency responses.

## 🚀 Key Features

- **Real-time Simulation**: Environmental data is generated every 10 seconds for 5 key Rwanda sectors.
- **Intelligent Risk Engine**: Classifies risk levels (LOW to CRITICAL) based on rainfall, soil moisture, displacement, and slope factors.
- **Automated Bilingual Alerting**: Generates instant alerts in English and Kinyarwanda.
- **Resilient SMS Dispatch**: Simulated SMS gateway with failover logic (Africa's Talking → Twilio).
- **Comprehensive Analytics**: Dashboard APIs for monitoring national safety status.
- **Historical Logging**: Full audit trail of environmental trends and system actions.

---

## 🏗️ Architecture

The system follows a clean architecture pattern:

- **`app/main.py`**: Entry point and scheduler initialization.
- **`app/models/`**: SQLAlchemy ORM models for database persistence.
- **`app/services/`**: Core business logic (Risk Engine, Simulation Engine).
- **`app/routes/`**: FastAPI REST endpoints.
- **`app/scheduler/`**: Background worker management using APScheduler.
- **`app/database/`**: Connection and session management.

---

## 🛠️ Setup Guide

### 1. Prerequisites
- Python 3.9+
- pip

### 2. Installation
```bash
# Clone the repository (or navigate to the folder)
cd rwasafe

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Server
```bash
# Start the backend simulation
python -m uvicorn app.main:app --reload
```

The server will be available at `http://localhost:8000`.
Swagger Documentation: `http://localhost:8000/docs`

---

## 📡 API Usage Examples

### Get Live Sector Risks
**Endpoint**: `GET /api/sectors`
**Response**:
```json
[
  {
    "id": 1,
    "name": "Rutsiro",
    "province": "Western",
    "current_risk_level": "HIGH",
    "current_risk_score": 72.5,
    "last_updated": "2024-05-11T12:00:00Z"
  }
]
```

### Get Active Alerts
**Endpoint**: `GET /api/alerts/active`
**Response**:
```json
[
  {
    "id": 105,
    "sector_id": 1,
    "risk_level": "HIGH",
    "message_en": "[RWASAFE ALERT] HIGH LANDSLIDE RISK – Rutsiro Sector. Heavy rainfall detected...",
    "message_rw": "[RWASAFE] IMPANUKA: Ibyago byinshi mu Rutsiro...",
    "timestamp": "2024-05-11T12:05:00Z"
  }
]
```

---

## 🛰️ Simulation Details

The system simulates four primary satellite/environmental sources:
1. **NASA SMAP**: Soil Moisture (%)
2. **Sentinel-1 SAR**: Ground Displacement Score (0-10)
3. **Sentinel-2**: Vegetation Stress Index (0-1)
4. **CHIRPS**: Rainfall Accumulation (mm)

---

## 🇷🇼 Monitored Sectors
- Rubavu
- Rutsiro
- Nyabihu
- Musanze
- Burera
