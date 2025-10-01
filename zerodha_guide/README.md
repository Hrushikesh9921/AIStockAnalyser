# ZERODHA API GUIDE

## 📁 Folder Contents

This folder contains a comprehensive guide and implementation for the Zerodha Kite Connect API.

### Files:

1. **`zerodha_api_complete.py`** - Complete standalone Python implementation
2. **`ZERODHA_API_COMPLETE_GUIDE.md`** - Detailed documentation with all endpoints
3. **`example_usage.py`** - Practical examples and demonstrations
4. **`README.md`** - This file

## 🚀 Quick Start

### 1. Setup Environment Variables

Create a `.env` file in your project root:

```bash
ZERODHA_API_KEY=your_api_key_here
ZERODHA_ACCESS_TOKEN=your_access_token_here
```

### 2. Install Dependencies

```bash
pip install kiteconnect requests python-dotenv
```

### 3. Basic Usage

```python
from zerodha_api_complete import ZerodhaAPI

# Initialize API
api = ZerodhaAPI()

# Get live quotes
quotes = api.get_quotes(["NSE:RELIANCE", "NSE:TCS"])
print(quotes)

# Get portfolio
portfolio = api.get_portfolio()
print(portfolio)
```

## 📚 Documentation

### Complete API Reference
- **File**: `ZERODHA_API_COMPLETE_GUIDE.md`
- **Content**: All endpoints, parameters, examples, error handling
- **Sections**: Authentication, Market Data, Orders, Portfolio, GTT, Mutual Funds

### Standalone Implementation
- **File**: `zerodha_api_complete.py`
- **Content**: Complete Python class with all API methods
- **Features**: Error handling, logging, utility functions

### Practical Examples
- **File**: `example_usage.py`
- **Content**: Real-world usage examples
- **Features**: Market data, portfolio, orders, error handling

## 🔧 Features Covered

### ✅ Market Data
- Live quotes (single & multiple)
- OHLC data
- Last Traded Price (LTP)
- Historical data (all intervals)
- Real-time market status

### ✅ Trading Operations
- Place orders (Market, Limit, SL, SL-M)
- Modify orders
- Cancel orders
- Order history and status
- Trade history

### ✅ Portfolio Management
- Holdings information
- Position tracking
- Margin details
- P&L calculations

### ✅ Advanced Features
- GTT (Good Till Triggered) orders
- Mutual fund operations
- SIP management
- User profile and margins

### ✅ Utility Functions
- Instrument token lookup
- Market hours checking
- Data validation
- Error handling

## 🛠️ API Endpoints Covered

| Category | Endpoints | Methods |
|----------|-----------|---------|
| **Profile** | `/user/profile`, `/user/margins` | GET |
| **Instruments** | `/instruments`, `/instruments/{exchange}` | GET |
| **Market Data** | `/quote`, `/quote/ohlc`, `/quote/ltp` | GET |
| **Historical** | `/instruments/historical/{token}/{interval}` | GET |
| **Portfolio** | `/portfolio/holdings`, `/portfolio/positions` | GET |
| **Orders** | `/orders`, `/orders/regular` | GET, POST, PUT, DELETE |
| **Trades** | `/trades`, `/orders/{id}/trades` | GET |
| **GTT** | `/gtt/triggers` | GET, POST, PUT, DELETE |
| **Mutual Funds** | `/mf/orders`, `/mf/sips`, `/mf/holdings` | GET, POST, PUT, DELETE |

## 📖 Usage Examples

### Get Live Market Data
```python
# Get quotes for multiple stocks
quotes = api.get_quotes(["NSE:RELIANCE", "NSE:TCS", "NSE:INFY"])

# Get OHLC data
ohlc = api.get_ohlc(["NSE:RELIANCE"])

# Get historical data
historical = api.get_historical_data(
    instrument_token=738561,
    from_date="2024-01-01",
    to_date="2024-01-31",
    interval="day"
)
```

### Portfolio Operations
```python
# Get holdings
portfolio = api.get_portfolio()

# Get positions
positions = api.get_positions()

# Get margins
margins = api.get_margins()
```

### Order Management
```python
# Place market order
order_id = api.place_order(
    variety="regular",
    exchange="NSE",
    tradingsymbol="RELIANCE",
    transaction_type="BUY",
    quantity=1,
    product="CNC",
    order_type="MARKET"
)

# Get all orders
orders = api.get_orders()

# Cancel order
api.cancel_order(order_id, "regular")
```

### GTT Orders
```python
# Place GTT order
gtt_id = api.place_gtt(
    condition={
        "exchange": "NSE",
        "tradingsymbol": "RELIANCE",
        "last_price": 2456.75,
        "trigger_values": [2500.00],
        "operators": ["gte"]
    },
    orders=[{
        "exchange": "NSE",
        "tradingsymbol": "RELIANCE",
        "transaction_type": "SELL",
        "quantity": 1,
        "product": "CNC",
        "order_type": "LIMIT",
        "price": 2500.00
    }]
)
```

## ⚠️ Important Notes

### Security
- Never expose API keys in code
- Use environment variables for credentials
- Implement proper error handling
- Monitor API usage

### Rate Limits
- Market Data: 3 requests/second
- Orders: 10 requests/second
- Historical Data: 1 request/second
- Portfolio: 1 request/second

### Market Hours
- Indian Market: 9:15 AM - 3:30 PM IST (Monday to Friday)
- Use `api.is_market_open()` to check market status

## 🚦 Error Handling

The implementation includes comprehensive error handling for:
- Authentication errors
- Rate limit exceeded
- Invalid parameters
- Network connectivity issues
- Order placement errors

## 📞 Support

### Official Resources
- [Zerodha Kite Connect](https://kite.trade/)
- [API Documentation](https://kite.trade/docs/connect/v3/)
- [Developer Forum](https://kite.trade/forum/)

### Contact
- Email: connect@zerodha.com
- Phone: +91-80-4040-2020

## 📄 License

This guide is for educational purposes. Please refer to Zerodha's official terms and conditions for commercial usage.

---

**Created by:** AI Assistant  
**Date:** January 2025  
**Version:** 1.0
