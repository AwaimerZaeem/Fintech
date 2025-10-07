# FinTech DataGen 💰📊

An end-to-end financial data demo that ties together a React interface, a Flask API, MongoDB persistence, and light-weight machine learning utilities.

---

## 🏗️ Technology Overview

### 🖥️ Frontend
- React.js UI
- React Router DOM for navigation
- Axios for HTTP requests
- Plain CSS styling

### ⚙️ Backend
- Flask (Python) service
- Flask-CORS for cross-origin access
- Environment management via python-dotenv

### 🧠 Machine Learning
- Python ecosystem: scikit-learn, pandas, numpy
- Baseline model: RandomForestRegressor

### 🗄️ Data Layer
- MongoDB database
- PyMongo client
- Works with MongoDB Atlas

---

## 📁 Repository Layout

```
FinTech-DataGen/
├── frontend/                 # React client
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js
│   │   │   ├── DataGenerator.js
│   │   │   └── Analytics.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
├── backend/                  # Flask API server
│   ├── database/
│   │   ├── __init__.py
│   │   └── mongodb.py
│   ├── ml_models/
│   │   ├── __init__.py
│   │   ├── predictor.py
│   │   └── forecasting.py
│   ├── app.py
│   ├── fintech_data_curator.py
│   └── requirements.txt
├── output/                   # Generated sample files
└── README.md
```

Note: Some filenames may differ slightly as the project evolves; the structure above reflects the current layout.

---

## 🚀 Quickstart

### Prerequisites
- Node.js v14+
- Python 3.8+
- Optional: MongoDB Atlas account

### 1️⃣ Configure environment

Create a `.env` file in `backend/` with your database configuration:
```bash
# backend/.env
MONGOURI=your_mongodb_connection_string
PORT=5000
FLASK_ENV=development
FLASK_DEBUG=True
```

### 2️⃣ Start the backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API will run at `http://localhost:5000`.

### 3️⃣ Start the frontend

```bash
cd frontend
npm install
npm start
```

The React app will be served from `http://localhost:3000`.

---

## 🔧 HTTP API (high level)

### Health
- `GET /api/health` — service and database status

### Data generation
- `POST /api/generate` — create a synthetic/curated financial dataset
- `GET /api/datasets` — list datasets
- `GET /api/datasets/<id>` — fetch one dataset

### Analytics & prediction
- `GET /api/analytics` — recent datasets/predictions and model snapshot
- `POST /api/predict` — make a simple next-step prediction

---

## 🧪 Local testing flow

1. Run the backend: `cd backend && python app.py`
2. Run the frontend: `cd frontend && npm start`
3. Open `http://localhost:3000`
4. Try the following:
   - Inspect system health in the Dashboard
   - Generate a small dataset
   - Review analytics and predictions

---

## 📊 Feature Snapshot

### ✅ Available now
- React SPA with basic routing
- Flask REST API endpoints
- MongoDB persistence (optional but supported)
- Simplified ML utilities and baseline model
- Integrated data curation pipeline
- Health/status checks
- Starter analytics view

### 🔄 Future ideas
- Deeper training workflows
- Real-time visualizations
- Authentication and roles
- Export enhancements
- Performance tuning

---

## 🛠️ Notes for developers

This repository is intended as a compact reference implementation of a full-stack FinTech workflow:

- Frontend: `Dashboard`, `DataGenerator`, and `Analytics` components
- Backend: Flask API wired to MongoDB
- ML: basic structures for prediction/forecast demos
- Data: curator integrates market data with simple sentiment signals

The `fintech_data_curator.py` lives under `backend/` and is used by the API for data creation.

---

## 📚 What to try next

1. Boot both services and confirm health
2. Validate DB connectivity from the health endpoint
3. Generate a small dataset from the UI
4. Extend features as needed

---

## 📄 License

MIT License — use and adapt with attribution.

---

## ✨ Attribution

Author: Abdullah Daoud  
Institution: FAST NUCES, BS Software Engineering

🚀 Build something insightful with your data.