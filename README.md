# Item Management API

A FastAPI-based REST API for managing items with SQLite database and a web interface.

## Features

- **RESTful API** with CRUD operations for items
- **SQLite database** for persistent storage
- **Web interface** for easy item management
- **Filtering and sorting** support for item queries

## Tech Stack

- **Backend**: FastAPI
- **Database**: SQLite
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **Server**: Uvicorn
- **Version Control**: Git

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the server:
```bash
uvicorn main:app --reload
```

The application will be available at:
- Web UI: http://localhost:8000/
- API: http://localhost:8000/api/

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve web interface |
| GET | `/api/items` | List all items (supports `in_stock`, `min_price`, `sort` query params) |
| GET | `/api/items/{item_id}` | Get specific item |
| POST | `/api/items/{item_id}` | Create or update an item |
| DELETE | `/api/items/{item_id}` | Delete an item |

### Query Parameters for GET /api/items

- `in_stock`: Filter by stock status (true/false)
- `min_price`: Filter by minimum price
- `sort`: Sort results (`price_asc` or `price_desc`)

### Example API Requests

```bash
# Get all items
curl http://localhost:8000/api/items

# Get in-stock items only
curl "http://localhost:8000/api/items?in_stock=true"

# Get items sorted by price (ascending)
curl "http://localhost:8000/api/items?sort=price_asc"

# Create/Update an item
curl -X POST http://localhost:8000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Apple", "price": 1.99, "in_stock": true}'

# Delete an item
curl -X DELETE http://localhost:8000/api/items/1
```

## Version Control

This project uses Git for version control. The repository is hosted on [GitHub](https://github.com/mea03kkw/fast-API-exercise).

## Project Structure

```
fastapi-lab/
├── .gitignore          # Git ignore rules
├── README.md           # Project documentation
├── main.py             # FastAPI application and endpoints
├── requirements.txt    # Python dependencies
└── static/
    ├── index.html      # Web interface
    ├── app.js          # Frontend JavaScript
    └── style.css       # Frontend styles