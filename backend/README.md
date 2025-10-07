# FinTech DataGen Backend

The Flask service that powers FinTech DataGen. It orchestrates dataset creation via the integrated curator, persists results to MongoDB, and exposes REST endpoints for downloads, analytics, and lightweight ML predictions.

## Highlights

- **Curated data pipeline**: `fintech_data_curator.py` composes market data with basic sentiment features
- **MongoDB storage**: datasets, price history, predictions, and metadata
- **RESTful API**: generation, retrieval, analytics, and file exports
- **ML utilities**: baseline prediction/forecast helpers
- **Resilient behavior**: handles missing database gracefully

## Setup

### Prerequisites

- Python 3.8+
- MongoDB (optional — the app still runs without it)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Environment (optional) — create `backend/.env`:
```bash
MONGOURI=mongodb://localhost:27017/fintech
PORT=5000
```

### Run the server

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

## API Map

- `GET /api/health` — service and DB status
- `POST /api/generate` — build a new dataset
- `GET /api/datasets` — list datasets
- `GET /api/datasets/<id>/csv` — download CSV
- `GET /api/datasets/<id>/json` — download JSON
- `GET /api/analytics` — recent datasets/predictions
- `POST /api/predict` — next-step prediction

## Testing

Example invocation (if present):
```bash
python tests/run_tests.py
```

## Files

```
backend/
├── app.py                    # Flask entrypoint
├── fintech_data_curator.py   # Curator module
├── database/
│   ├── mongodb.py            # MongoDB access helpers
│   └── __init__.py
├── ml_models/
│   ├── predictor.py          # Tabular predictor
│   ├── forecasting.py        # Forecast utilities
│   └── __init__.py
├── requirements.txt
└── README.md
```

## Behavior without MongoDB

The service strives to remain usable even when no database is configured:
- Dataset generation still works
- Endpoints that require DB return clear errors or empty lists
- Core curation and preview actions remain available

## Integration Notes

`fintech_data_curator.py` is embedded in the backend:
- Logs are written within the backend directory
- Dependencies are specified in `requirements.txt`
- Can be used directly or through the API
