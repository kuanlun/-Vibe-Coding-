# Stock Portfolio Manager

Multi-market stock portfolio monitoring platform supporting A-shares, Taiwan stocks, and US stocks.

## Tech Stack

- **Backend**: Python FastAPI
- **Frontend**: Vue 3 + Vite
- **Database**: SQLite
- **Data Sources**: AKShare / Yahoo Finance

## Project Structure

```
stock-portfolio-manager/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── database.py       # Database configuration
│   │   ├── models/           # SQLAlchemy models
│   │   ├── routers/          # API routes
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utilities
│   ├── tests/                # pytest tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/            # Page components
│   │   ├── components/      # Reusable components
│   │   ├── router/          # Router configuration
│   │   └── main.js          # Vue entry point
│   └── package.json
└── doc/
    ├── proposal.md          # Requirements document
    ├── design.md            # Design document
    └── tasks/               # Task lists
```

## Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Features

- User authentication (JWT)
- Portfolio management (CRUD)
- Multi-market support (A-shares, Taiwan, US)
- Price alerts
- Data export (CSV/Excel)

## API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `GET /api/portfolios` - Get portfolios
- `POST /api/portfolios` - Create portfolio
- `PUT /api/portfolios/{id}` - Update portfolio
- `DELETE /api/portfolios/{id}` - Delete portfolio
- `GET /api/stocks/quote/{symbol}` - Get stock quote
- `GET /api/alerts` - Get alerts
- `POST /api/alerts` - Create alert
- `GET /api/export/csv` - Export CSV
- `GET /api/export/excel` - Export Excel