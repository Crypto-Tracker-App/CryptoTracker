# CryptoTracker

A comprehensive cryptocurrency tracking and monitoring API with built-in **Swagger/OpenAPI** documentation.

## Features

- 🚀 **RESTful API** - Clean and intuitive API design
- 📊 **Cryptocurrency Data** - Track real-time cryptocurrency prices and market data
- 💼 **Portfolio Management** - Manage your crypto holdings
- 🔔 **Price Alerts** - Set up notifications for price changes
- 📈 **Market Statistics** - Access overall market trends
- 📝 **OpenAPI/Swagger Documentation** - Interactive API documentation
- ✅ **Data Validation** - Pydantic models for request/response validation

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Crypto-Tracker-App/CryptoTracker.git
cd CryptoTracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the API

Start the server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## Accessing Swagger/OpenAPI Documentation

Once the API is running, you can access the interactive documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Swagger UI Features

The Swagger UI provides:
- Interactive API testing - Try out endpoints directly in the browser
- Complete request/response schemas
- Example requests and responses
- Authentication testing
- Parameter descriptions
- Response codes and error messages

## API Endpoints

### Cryptocurrency Endpoints

- `GET /api/v1/cryptocurrencies` - List all cryptocurrencies
- `GET /api/v1/cryptocurrencies/{symbol}` - Get cryptocurrency by symbol
- `GET /api/v1/cryptocurrencies/{symbol}/history` - Get price history

### Portfolio Endpoints

- `GET /api/v1/portfolio` - Get all portfolio holdings
- `POST /api/v1/portfolio` - Add a new holding
- `DELETE /api/v1/portfolio/{holding_id}` - Delete a holding

### Alert Endpoints

- `GET /api/v1/alerts` - Get all price alerts
- `POST /api/v1/alerts` - Create a new alert
- `DELETE /api/v1/alerts/{alert_id}` - Delete an alert

### Market Endpoints

- `GET /api/v1/market/stats` - Get overall market statistics

## Example Usage

### Get Bitcoin Information

```bash
curl http://localhost:8000/api/v1/cryptocurrencies/BTC
```

Response:
```json
{
  "symbol": "BTC",
  "name": "Bitcoin",
  "current_price": 45000.00,
  "market_cap": 850000000000.00,
  "volume_24h": 25000000000.00,
  "price_change_24h": 2.5,
  "last_updated": "2026-01-03T18:30:00Z"
}
```

### Add Portfolio Holding

```bash
curl -X POST http://localhost:8000/api/v1/portfolio \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC",
    "amount": 0.5,
    "purchase_price": 40000.00
  }'
```

### Create Price Alert

```bash
curl -X POST http://localhost:8000/api/v1/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "ETH",
    "alert_type": "price_above",
    "target_price": 3000.00
  }'
```

## Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server
- **OpenAPI 3.0** - Industry-standard API specification
- **Swagger UI** - Interactive API documentation

## OpenAPI Specification

This API follows the OpenAPI 3.1.0 specification. The complete specification can be accessed at `/openapi.json` when the server is running.

Key features of the OpenAPI implementation:
- Comprehensive endpoint documentation
- Request/response schema definitions
- Validation rules and constraints
- Example requests and responses
- Error response documentation
- Type-safe models using Pydantic

## Development

### Project Structure

```
CryptoTracker/
├── main.py              # Main API application with all endpoints
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Endpoints

1. Define Pydantic models for request/response
2. Add endpoint with proper OpenAPI decorators
3. Include comprehensive docstrings
4. Add examples in the model Config class

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.