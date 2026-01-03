"""
CryptoTracker API - A cryptocurrency tracking and monitoring API
This API provides endpoints for tracking cryptocurrency prices, portfolios, and alerts.
"""

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Initialize FastAPI app with metadata for OpenAPI
app = FastAPI(
    title="CryptoTracker API",
    description="""
    # CryptoTracker API
    
    A comprehensive cryptocurrency tracking and monitoring API that provides:
    
    * **Cryptocurrency Information** - Get real-time and historical data
    * **Portfolio Management** - Track your crypto holdings
    * **Price Alerts** - Set up notifications for price changes
    * **Market Analysis** - Access market trends and statistics
    
    ## Features
    
    - Real-time cryptocurrency price tracking
    - Portfolio management and performance tracking
    - Price alerts and notifications
    - Historical price data
    - Market statistics and trends
    
    ## Getting Started
    
    All endpoints are documented below with example requests and responses.
    Try out the interactive API documentation by clicking on any endpoint.
    """,
    version="1.0.0",
    contact={
        "name": "CryptoTracker Support",
        "email": "support@cryptotracker.example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "cryptocurrencies",
            "description": "Operations related to cryptocurrency data and prices",
        },
        {
            "name": "portfolio",
            "description": "Manage your cryptocurrency portfolio",
        },
        {
            "name": "alerts",
            "description": "Price alerts and notifications",
        },
        {
            "name": "market",
            "description": "Market statistics and analysis",
        },
    ]
)


# Pydantic Models for Request/Response
class CryptoCurrency(BaseModel):
    """Cryptocurrency information model"""
    symbol: str = Field(..., example="BTC", description="Cryptocurrency symbol (e.g., BTC, ETH)")
    name: str = Field(..., example="Bitcoin", description="Full name of the cryptocurrency")
    current_price: float = Field(..., example=45000.00, description="Current price in USD")
    market_cap: float = Field(..., example=850000000000.00, description="Market capitalization in USD")
    volume_24h: float = Field(..., example=25000000000.00, description="24-hour trading volume in USD")
    price_change_24h: float = Field(..., example=2.5, description="24-hour price change percentage")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "BTC",
                "name": "Bitcoin",
                "current_price": 45000.00,
                "market_cap": 850000000000.00,
                "volume_24h": 25000000000.00,
                "price_change_24h": 2.5,
                "last_updated": "2026-01-03T18:30:00Z"
            }
        }


class PortfolioHolding(BaseModel):
    """Portfolio holding model"""
    id: Optional[int] = Field(None, example=1, description="Unique holding ID")
    symbol: str = Field(..., example="BTC", description="Cryptocurrency symbol")
    amount: float = Field(..., gt=0, example=0.5, description="Amount held (must be greater than 0)")
    purchase_price: float = Field(..., gt=0, example=40000.00, description="Purchase price in USD")
    purchase_date: datetime = Field(default_factory=datetime.now, description="Purchase date")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "symbol": "BTC",
                "amount": 0.5,
                "purchase_price": 40000.00,
                "purchase_date": "2025-12-01T10:00:00Z"
            }
        }


class AlertType(str, Enum):
    """Alert type enumeration"""
    PRICE_ABOVE = "price_above"
    PRICE_BELOW = "price_below"
    PRICE_CHANGE = "price_change"


class PriceAlert(BaseModel):
    """Price alert model"""
    id: Optional[int] = Field(None, example=1, description="Unique alert ID")
    symbol: str = Field(..., example="ETH", description="Cryptocurrency symbol")
    alert_type: AlertType = Field(..., description="Type of alert")
    target_price: Optional[float] = Field(None, example=3000.00, description="Target price for price alerts")
    percentage_change: Optional[float] = Field(None, example=5.0, description="Percentage change for change alerts")
    active: bool = Field(default=True, description="Whether the alert is active")
    created_at: datetime = Field(default_factory=datetime.now, description="Alert creation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "symbol": "ETH",
                "alert_type": "price_above",
                "target_price": 3000.00,
                "active": True,
                "created_at": "2026-01-01T12:00:00Z"
            }
        }


class MarketStats(BaseModel):
    """Market statistics model"""
    total_market_cap: float = Field(..., example=1500000000000.00, description="Total crypto market cap in USD")
    total_volume_24h: float = Field(..., example=80000000000.00, description="Total 24h trading volume in USD")
    btc_dominance: float = Field(..., example=45.5, description="Bitcoin market dominance percentage")
    active_cryptocurrencies: int = Field(..., example=10000, description="Number of active cryptocurrencies")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


# In-memory storage (for demonstration purposes)
cryptocurrencies_db = [
    {
        "symbol": "BTC",
        "name": "Bitcoin",
        "current_price": 45000.00,
        "market_cap": 850000000000.00,
        "volume_24h": 25000000000.00,
        "price_change_24h": 2.5,
        "last_updated": datetime.now()
    },
    {
        "symbol": "ETH",
        "name": "Ethereum",
        "current_price": 2800.00,
        "market_cap": 340000000000.00,
        "volume_24h": 15000000000.00,
        "price_change_24h": 3.2,
        "last_updated": datetime.now()
    },
    {
        "symbol": "BNB",
        "name": "Binance Coin",
        "current_price": 320.00,
        "market_cap": 50000000000.00,
        "volume_24h": 2000000000.00,
        "price_change_24h": -1.5,
        "last_updated": datetime.now()
    }
]

portfolio_db = []
alerts_db = []


# API Endpoints

@app.get("/", tags=["default"])
async def root():
    """
    Root endpoint - API health check
    
    Returns a welcome message and links to API documentation.
    """
    return {
        "message": "Welcome to CryptoTracker API",
        "version": "1.0.0",
        "documentation": "/docs",
        "openapi_spec": "/openapi.json"
    }


@app.get(
    "/api/v1/cryptocurrencies",
    response_model=List[CryptoCurrency],
    tags=["cryptocurrencies"],
    summary="List all cryptocurrencies",
    description="Retrieve a list of all tracked cryptocurrencies with their current prices and market data."
)
async def get_cryptocurrencies(
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of results to return"),
    sort_by: str = Query(default="market_cap", description="Field to sort by (market_cap, price, volume)")
):
    """
    Get a list of cryptocurrencies with optional filtering and sorting.
    
    - **limit**: Maximum number of cryptocurrencies to return (1-100)
    - **sort_by**: Sort results by market_cap, price, or volume
    
    Returns a list of cryptocurrency objects with current market data.
    """
    # Simple implementation - return limited results
    return cryptocurrencies_db[:limit]


@app.get(
    "/api/v1/cryptocurrencies/{symbol}",
    response_model=CryptoCurrency,
    tags=["cryptocurrencies"],
    summary="Get cryptocurrency by symbol",
    description="Retrieve detailed information about a specific cryptocurrency by its symbol."
)
async def get_cryptocurrency(
    symbol: str = Path(..., example="BTC", description="Cryptocurrency symbol (e.g., BTC, ETH)")
):
    """
    Get detailed information about a specific cryptocurrency.
    
    - **symbol**: The cryptocurrency symbol (case-insensitive)
    
    Returns cryptocurrency details including price, market cap, and volume.
    """
    symbol = symbol.upper()
    for crypto in cryptocurrencies_db:
        if crypto["symbol"] == symbol:
            return crypto
    raise HTTPException(status_code=404, detail=f"Cryptocurrency {symbol} not found")


@app.get(
    "/api/v1/portfolio",
    response_model=List[PortfolioHolding],
    tags=["portfolio"],
    summary="Get portfolio holdings",
    description="Retrieve all holdings in your cryptocurrency portfolio."
)
async def get_portfolio():
    """
    Get all holdings in your cryptocurrency portfolio.
    
    Returns a list of portfolio holdings with purchase information and current values.
    """
    return portfolio_db


@app.post(
    "/api/v1/portfolio",
    response_model=PortfolioHolding,
    status_code=201,
    tags=["portfolio"],
    summary="Add portfolio holding",
    description="Add a new cryptocurrency holding to your portfolio."
)
async def add_portfolio_holding(holding: PortfolioHolding):
    """
    Add a new holding to your cryptocurrency portfolio.
    
    - **symbol**: Cryptocurrency symbol (must exist in tracked cryptocurrencies)
    - **amount**: Amount of cryptocurrency held (must be > 0)
    - **purchase_price**: Price at which the cryptocurrency was purchased (must be > 0)
    - **purchase_date**: Date of purchase (optional, defaults to current time)
    
    Returns the created holding with an assigned ID.
    """
    # Validate that the cryptocurrency exists
    symbol_exists = any(crypto["symbol"] == holding.symbol.upper() for crypto in cryptocurrencies_db)
    if not symbol_exists:
        raise HTTPException(status_code=400, detail=f"Cryptocurrency {holding.symbol} not found")
    
    # Assign ID
    holding.id = len(portfolio_db) + 1
    holding.symbol = holding.symbol.upper()
    portfolio_db.append(holding.dict())
    return holding


@app.delete(
    "/api/v1/portfolio/{holding_id}",
    status_code=204,
    tags=["portfolio"],
    summary="Delete portfolio holding",
    description="Remove a holding from your cryptocurrency portfolio."
)
async def delete_portfolio_holding(
    holding_id: int = Path(..., ge=1, description="ID of the holding to delete")
):
    """
    Delete a holding from your portfolio.
    
    - **holding_id**: The ID of the holding to remove
    
    Returns 204 No Content on success.
    """
    for i, holding in enumerate(portfolio_db):
        if holding["id"] == holding_id:
            portfolio_db.pop(i)
            return JSONResponse(status_code=204, content={})
    raise HTTPException(status_code=404, detail=f"Holding {holding_id} not found")


@app.get(
    "/api/v1/alerts",
    response_model=List[PriceAlert],
    tags=["alerts"],
    summary="Get price alerts",
    description="Retrieve all configured price alerts."
)
async def get_alerts(
    active_only: bool = Query(default=True, description="Filter to show only active alerts")
):
    """
    Get all configured price alerts.
    
    - **active_only**: If True, return only active alerts
    
    Returns a list of price alerts.
    """
    if active_only:
        return [alert for alert in alerts_db if alert.get("active", True)]
    return alerts_db


@app.post(
    "/api/v1/alerts",
    response_model=PriceAlert,
    status_code=201,
    tags=["alerts"],
    summary="Create price alert",
    description="Create a new price alert for a cryptocurrency."
)
async def create_alert(alert: PriceAlert):
    """
    Create a new price alert.
    
    - **symbol**: Cryptocurrency symbol to monitor
    - **alert_type**: Type of alert (price_above, price_below, price_change)
    - **target_price**: Target price for price-based alerts (required for price_above/price_below)
    - **percentage_change**: Percentage change for change-based alerts (required for price_change)
    - **active**: Whether the alert is active (optional, defaults to True)
    
    Returns the created alert with an assigned ID.
    """
    # Validate that the cryptocurrency exists
    symbol_exists = any(crypto["symbol"] == alert.symbol.upper() for crypto in cryptocurrencies_db)
    if not symbol_exists:
        raise HTTPException(status_code=400, detail=f"Cryptocurrency {alert.symbol} not found")
    
    # Validate alert configuration
    if alert.alert_type in [AlertType.PRICE_ABOVE, AlertType.PRICE_BELOW]:
        if alert.target_price is None:
            raise HTTPException(status_code=400, detail="target_price is required for price alerts")
    elif alert.alert_type == AlertType.PRICE_CHANGE:
        if alert.percentage_change is None:
            raise HTTPException(status_code=400, detail="percentage_change is required for price change alerts")
    
    # Assign ID
    alert.id = len(alerts_db) + 1
    alert.symbol = alert.symbol.upper()
    alerts_db.append(alert.dict())
    return alert


@app.delete(
    "/api/v1/alerts/{alert_id}",
    status_code=204,
    tags=["alerts"],
    summary="Delete price alert",
    description="Remove a price alert."
)
async def delete_alert(
    alert_id: int = Path(..., ge=1, description="ID of the alert to delete")
):
    """
    Delete a price alert.
    
    - **alert_id**: The ID of the alert to remove
    
    Returns 204 No Content on success.
    """
    for i, alert in enumerate(alerts_db):
        if alert["id"] == alert_id:
            alerts_db.pop(i)
            return JSONResponse(status_code=204, content={})
    raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")


@app.get(
    "/api/v1/market/stats",
    response_model=MarketStats,
    tags=["market"],
    summary="Get market statistics",
    description="Retrieve overall cryptocurrency market statistics."
)
async def get_market_stats():
    """
    Get overall cryptocurrency market statistics.
    
    Returns aggregated market data including total market cap, volume, and Bitcoin dominance.
    """
    return {
        "total_market_cap": 1500000000000.00,
        "total_volume_24h": 80000000000.00,
        "btc_dominance": 45.5,
        "active_cryptocurrencies": 10000,
        "last_updated": datetime.now()
    }


@app.get(
    "/api/v1/cryptocurrencies/{symbol}/history",
    tags=["cryptocurrencies"],
    summary="Get price history",
    description="Retrieve historical price data for a cryptocurrency."
)
async def get_price_history(
    symbol: str = Path(..., example="BTC", description="Cryptocurrency symbol"),
    days: int = Query(default=7, ge=1, le=365, description="Number of days of history to retrieve")
):
    """
    Get historical price data for a cryptocurrency.
    
    - **symbol**: The cryptocurrency symbol
    - **days**: Number of days of historical data (1-365)
    
    Returns a list of historical price points.
    """
    symbol = symbol.upper()
    # Validate that the cryptocurrency exists
    symbol_exists = any(crypto["symbol"] == symbol for crypto in cryptocurrencies_db)
    if not symbol_exists:
        raise HTTPException(status_code=404, detail=f"Cryptocurrency {symbol} not found")
    
    # Return mock historical data
    return {
        "symbol": symbol,
        "days": days,
        "data_points": [
            {
                "date": "2026-01-03",
                "price": 45000.00,
                "volume": 25000000000.00
            },
            {
                "date": "2026-01-02",
                "price": 44500.00,
                "volume": 24000000000.00
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
