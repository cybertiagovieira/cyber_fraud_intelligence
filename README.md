# Cyber Fraud Intelligence Architecture

Phase 1 Local Deployment of an automated Cyber Threat Intelligence (CTI) pipeline designed to extract, translate, parse, and disseminate OSINT and cyber fraud telemetry. 

## Architecture Subsystems

1. **Ingestion & Parsing (`ingestion/`)**
   * **`telegram_scraper.py`**: Extracts raw text from targeted public Telegram channels via unauthenticated web previews.
   * **`translator.py`**: Executes offline translation (Russian/Portuguese to English) utilizing `argostranslate`.
   * **`parser.py`**: Heuristically maps unstructured OSINT text to a rigid database schema (Fraud Category, MITRE ATT&CK vectors, Victimology, Financial Impact).
   * **`backfill.py`**: Executes paginated historical extraction via Silobreaker API.

2. **Threat Enrichment (`ingestion/tip_enrichment.py`)**
   * Executes cryptographic HMAC-SHA512 authenticated requests to the Silobreaker API (v2).
   * **Entity Pivot**: Correlates raw IOCs to Threat Actors and Malware families.
   * **Document Extraction**: Retrieves recent 30-day contextual intelligence.

3. **Database (`database/`)**
   * SQLite relational database (`fraud_events.db`).
   * **`init_db.py`**: Constructs core threat telemetry and actionable intelligence tables.
   * **`seed_data.py`**: Injects synthetic baseline telemetry for architectural verification.

4. **Presentation Layer (`app.py`, `pages/`)**
   * Streamlit multi-page deployment.
   * **Executive Pulse**: High-level KPI aggregations, category distribution, and raw telemetry access.
   * **Trend Lines**: Visualized TTP commoditization timelines, sector targeting distribution, and source reliability scoring.
   * **Threat Enrichment**: Direct UI integration for external Silobreaker structural pivots.

5. **Dissemination API (`api/main.py`)**
   * FastAPI ASGI server for machine-to-machine intelligence distribution to external SOC/SOAR environments.
   * Endpoints: `/api/v1/events/recent`, `/api/v1/events/vector/{vector}`.

6. **Orchestration (`run_pipeline.py`, `ingestion/orchestrator.py`)**
   * Daemonized continuous execution loop utilizing `schedule`.
   * Triggers ingestion and database staging at 4-hour intervals.

## Deployment Instructions

### 1. Dependency Installation
Execute in a Python virtual environment:
```powershell
pip install -r requirements.txt

2. Environment Configuration
Create a .env file in the root directory. Insert Silobreaker API credentials:

Plaintext
SILOBREAKER_API_KEY=your_api_key_here
SILOBREAKER_SHARED_KEY=your_shared_key_here
3. Database Initialization
Construct the schema:

PowerShell
python database/init_db.py
(Optional) Inject baseline synthetic data:

PowerShell
python database/seed_data.py
(Optional) Execute historical data backfill via Silobreaker:

PowerShell
python ingestion/backfill.py
4. Operational Execution
The system requires three parallel processes. Execute each in a separate terminal window:

Terminal 1: Continuous Ingestion Daemon

PowerShell
python run_pipeline.py
Terminal 2: Presentation Layer

PowerShell
python -m streamlit run app.py
Access UI at http://localhost:8501.

Terminal 3: Dissemination API

PowerShell
python -m uvicorn api.main:app --port 8000
Access API documentation at http://localhost:8000/docs.
