# ZERODHA KITE CONNECT API - COMPLETE GUIDE

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [API Endpoints Reference](#api-endpoints-reference)
4. [User Profile & Authentication](#user-profile--authentication)
5. [Instruments & Master Data](#instruments--master-data)
6. [Market Data - Quotes](#market-data---quotes)
7. [Historical Data](#historical-data)
8. [Portfolio & Holdings](#portfolio--holdings)
9. [Orders Management](#orders-management)
10. [GTT (Good Till Triggered) Orders](#gtt-good-till-triggered-orders)
11. [Mutual Funds](#mutual-funds)
12. [Error Handling](#error-handling)
13. [Rate Limits](#rate-limits)
14. [Examples & Use Cases](#examples--use-cases)
15. [Best Practices](#best-practices)

---

## 🔍 Overview

The Zerodha Kite Connect API is a comprehensive REST API that provides access to all trading and market data functionality available on the Kite trading platform. This guide covers ALL available endpoints, methods, and parameters.

### Key Features:
- **Real-time Market Data**: Live quotes, OHLC, LTP
- **Historical Data**: Candlestick data with multiple intervals
- **Order Management**: Place, modify, cancel orders
- **Portfolio Management**: Holdings, positions, margins
- **GTT Orders**: Good Till Triggered orders
- **Mutual Funds**: MF orders, SIPs, holdings
- **User Profile**: Account information, margins

### Base URL:
```
https://api.kite.trade
```

### API Version:
```
X-Kite-Version: 3
```

---

## 🔐 Authentication

### Required Headers:
```http
Authorization: token {api_key}:{access_token}
X-Kite-Version: 3
Content-Type: application/x-www-form-urlencoded
```

### Environment Variables:
```bash
ZERODHA_API_KEY=your_api_key
ZERODHA_ACCESS_TOKEN=your_access_token
```

---

## 📚 API Endpoints Reference

### 🔗 Complete Endpoint List

| Category | Method | Endpoint | Description |
|----------|--------|----------|-------------|
| **Profile** | GET | `/user/profile` | Get user profile |
| **Margins** | GET | `/user/margins` | Get all margins |
| **Margins** | GET | `/user/margins/{segment}` | Get segment margins |
| **Instruments** | GET | `/instruments` | Get all instruments |
| **Instruments** | GET | `/instruments/{exchange}` | Get exchange instruments |
| **Instruments** | GET | `/instruments/csv` | Get instruments CSV |
| **Instruments** | GET | `/instruments/csv/{exchange}` | Get exchange instruments CSV |
| **Quotes** | GET | `/quote` | Get quotes |
| **OHLC** | GET | `/quote/ohlc` | Get OHLC data |
| **LTP** | GET | `/quote/ltp` | Get LTP data |
| **Historical** | GET | `/instruments/historical/{instrument_token}/{interval}` | Get historical data |
| **Portfolio** | GET | `/portfolio/holdings` | Get holdings |
| **Positions** | GET | `/portfolio/positions` | Get positions |
| **Orders** | GET | `/orders` | Get all orders |
| **Orders** | GET | `/orders/{order_id}` | Get order history |
| **Orders** | POST | `/orders/regular` | Place order |
| **Orders** | PUT | `/orders/regular/{order_id}` | Modify order |
| **Orders** | DELETE | `/orders/regular/{order_id}` | Cancel order |
| **Trades** | GET | `/trades` | Get all trades |
| **Trades** | GET | `/orders/{order_id}/trades` | Get order trades |
| **GTT** | GET | `/gtt/triggers` | Get GTT orders |
| **GTT** | GET | `/gtt/triggers/{trigger_id}` | Get GTT by ID |
| **GTT** | POST | `/gtt/triggers` | Place GTT |
| **GTT** | PUT | `/gtt/triggers/{trigger_id}` | Modify GTT |
| **GTT** | DELETE | `/gtt/triggers/{trigger_id}` | Delete GTT |
| **MF Orders** | GET | `/mf/orders` | Get MF orders |
| **MF Orders** | POST | `/mf/orders` | Place MF order |
| **MF Orders** | DELETE | `/mf/orders/{order_id}` | Cancel MF order |
| **MF SIPs** | GET | `/mf/sips` | Get MF SIPs |
| **MF SIPs** | POST | `/mf/sips` | Place MF SIP |
| **MF SIPs** | PUT | `/mf/sips/{sip_id}` | Modify MF SIP |
| **MF SIPs** | DELETE | `/mf/sips/{sip_id}` | Delete MF SIP |
| **MF Holdings** | GET | `/mf/holdings` | Get MF holdings |

---

## 👤 User Profile & Authentication

### Get User Profile
```http
GET /user/profile
```

**Response:**
```json
{
  "user_id": "AB1234",
  "user_name": "John Doe",
  "email": "john@example.com",
  "user_type": "individual",
  "broker": "ZERODHA"
}
```

### Get Margins
```http
GET /user/margins
GET /user/margins/{segment}
```

**Segments:** `equity`, `commodity`, `currency`

**Response:**
```json
{
  "equity": {
    "enabled": true,
    "net": 100000.0,
    "available": {
      "ad_hoc_margin": 0,
      "cash": 100000.0,
      "opening_balance": 100000.0
    },
    "utilised": {
      "debits": 0,
      "exposure": 0,
      "m2m_realised": 0,
      "m2m_unrealised": 0,
      "option_premium": 0,
      "payout": 0,
      "span": 0,
      "holding_sales": 0,
      "turnover": 0
    }
  }
}
```

---

## 📊 Instruments & Master Data

### Get All Instruments
```http
GET /instruments
```

### Get Exchange Instruments
```http
GET /instruments/{exchange}
```

**Exchanges:** `NSE`, `BSE`, `NFO`, `BFO`, `CDS`, `MCX`

**Response:**
```json
[
  {
    "instrument_token": 738561,
    "exchange_token": 2885633,
    "tradingsymbol": "RELIANCE",
    "name": "RELIANCE",
    "last_price": 2456.75,
    "expiry": null,
    "strike": 0,
    "tick_size": 0.05,
    "lot_size": 1,
    "instrument_type": "EQ",
    "segment": "NSE",
    "exchange": "NSE"
  }
]
```

### Get Instruments CSV
```http
GET /instruments/csv
GET /instruments/csv/{exchange}
```

**Response:** CSV file download URL

---

## 📈 Market Data - Quotes

### Get Single Quote
```http
GET /quote?i=NSE:RELIANCE
```

### Get Multiple Quotes
```http
GET /quote?i=NSE:RELIANCE,NSE:TCS,NSE:INFY
```

**Response:**
```json
{
  "NSE:RELIANCE": {
    "instrument_token": 738561,
    "last_price": 2456.75,
    "last_quantity": 1,
    "last_trade_time": "2024-01-15 14:30:00",
    "average_price": 2450.25,
    "volume": 1234567,
    "buy_quantity": 500,
    "sell_quantity": 300,
    "ohlc": {
      "open": 2450.00,
      "high": 2460.00,
      "low": 2440.00,
      "close": 2456.75
    },
    "net_change": 6.75,
    "oi": 0,
    "oi_day_high": 0,
    "oi_day_low": 0,
    "timestamp": "2024-01-15 14:30:00"
  }
}
```

### Get OHLC Data
```http
GET /quote/ohlc?i=NSE:RELIANCE,NSE:TCS
```

**Response:**
```json
{
  "NSE:RELIANCE": {
    "ohlc": {
      "open": 2450.00,
      "high": 2460.00,
      "low": 2440.00,
      "close": 2456.75
    }
  }
}
```

### Get LTP (Last Traded Price)
```http
GET /quote/ltp?i=NSE:RELIANCE,NSE:TCS
```

**Response:**
```json
{
  "NSE:RELIANCE": {
    "instrument_token": 738561,
    "last_price": 2456.75
  }
}
```

---

## 📊 Historical Data

### Get Historical Data
```http
GET /instruments/historical/{instrument_token}/{interval}?from=2024-01-01&to=2024-01-31&continuous=0&oi=0
```

**Parameters:**
- `instrument_token` (int): Instrument token
- `interval` (str): Data interval
- `from` (str): Start date (YYYY-MM-DD)
- `to` (str): End date (YYYY-MM-DD)
- `continuous` (int): Continuous data (0/1)
- `oi` (int): Include open interest (0/1)

**Intervals:**
- `minute` - 1 minute
- `3minute` - 3 minutes
- `5minute` - 5 minutes
- `15minute` - 15 minutes
- `30minute` - 30 minutes
- `60minute` - 1 hour
- `day` - Daily

**Response:**
```json
[
  {
    "date": "2024-01-15T00:00:00+05:30",
    "open": 2450.00,
    "high": 2460.00,
    "low": 2440.00,
    "close": 2456.75,
    "volume": 1234567,
    "oi": 0
  }
]
```

---

## 💰 Portfolio & Holdings

### Get Holdings
```http
GET /portfolio/holdings
```

**Response:**
```json
[
  {
    "tradingsymbol": "RELIANCE",
    "exchange": "NSE",
    "instrument_token": 738561,
    "product": "CNC",
    "quantity": 10,
    "overnight_quantity": 10,
    "collateral_quantity": 0,
    "day_quantity": 0,
    "average_price": 2450.00,
    "last_price": 2456.75,
    "pnl": 67.50,
    "day_change": 6.75,
    "day_change_percentage": 0.28
  }
]
```

### Get Positions
```http
GET /portfolio/positions
```

**Response:**
```json
{
  "day": [
    {
      "tradingsymbol": "RELIANCE",
      "exchange": "NSE",
      "instrument_token": 738561,
      "product": "MIS",
      "quantity": 5,
      "overnight_quantity": 0,
      "collateral_quantity": 0,
      "day_quantity": 5,
      "average_price": 2450.00,
      "last_price": 2456.75,
      "pnl": 33.75,
      "day_change": 6.75,
      "day_change_percentage": 0.28
    }
  ],
  "net": []
}
```

---

## 📋 Orders Management

### Place Order
```http
POST /orders/regular
```

**Request Body:**
```json
{
  "variety": "regular",
  "exchange": "NSE",
  "tradingsymbol": "RELIANCE",
  "transaction_type": "BUY",
  "quantity": 1,
  "product": "CNC",
  "order_type": "MARKET",
  "price": 0,
  "validity": "DAY",
  "disclosed_quantity": 0,
  "trigger_price": 0,
  "squareoff": 0,
  "stoploss": 0,
  "trailing_stoploss": 0,
  "tag": "my_order"
}
```

**Parameters:**
- `variety` (str): `regular`, `amo`, `bracket`, `cover`, `iceberg`
- `exchange` (str): `NSE`, `BSE`, `NFO`, `BFO`, `CDS`, `MCX`
- `tradingsymbol` (str): Trading symbol
- `transaction_type` (str): `BUY`, `SELL`
- `quantity` (int): Quantity
- `product` (str): `CNC`, `MIS`, `NRML`
- `order_type` (str): `MARKET`, `LIMIT`, `SL`, `SL-M`
- `price` (float): Price (for LIMIT orders)
- `validity` (str): `DAY`, `IOC`
- `disclosed_quantity` (int): Disclosed quantity
- `trigger_price` (float): Trigger price (for SL orders)
- `squareoff` (float): Square off price (for bracket orders)
- `stoploss` (float): Stop loss price (for bracket orders)
- `trailing_stoploss` (float): Trailing stop loss (for bracket orders)
- `tag` (str): Order tag

**Response:**
```json
{
  "data": {
    "order_id": "240115000000000"
  }
}
```

### Modify Order
```http
PUT /orders/regular/{order_id}
```

**Request Body:**
```json
{
  "variety": "regular",
  "quantity": 2,
  "price": 2460.00,
  "order_type": "LIMIT",
  "validity": "DAY"
}
```

### Cancel Order
```http
DELETE /orders/regular/{order_id}
```

**Request Body:**
```json
{
  "variety": "regular"
}
```

### Get All Orders
```http
GET /orders
```

**Response:**
```json
[
  {
    "order_id": "240115000000000",
    "parent_order_id": null,
    "exchange_order_id": "123456789",
    "placed_by": "AB1234",
    "variety": "regular",
    "status": "COMPLETE",
    "tradingsymbol": "RELIANCE",
    "exchange": "NSE",
    "instrument_token": 738561,
    "transaction_type": "BUY",
    "product": "CNC",
    "order_type": "MARKET",
    "price": 0.00,
    "quantity": 1,
    "disclosed_quantity": 0,
    "trigger_price": 0.00,
    "average_price": 2456.75,
    "filled_quantity": 1,
    "pending_quantity": 0,
    "cancelled_quantity": 0,
    "order_timestamp": "2024-01-15 14:30:00",
    "exchange_timestamp": "2024-01-15 14:30:00",
    "validity": "DAY",
    "validity_ttl": 0,
    "tag": "my_order"
  }
]
```

### Get Order History
```http
GET /orders/{order_id}
```

### Get Trades
```http
GET /trades
```

### Get Order Trades
```http
GET /orders/{order_id}/trades
```

---

## ⏰ GTT (Good Till Triggered) Orders

### Place GTT
```http
POST /gtt/triggers
```

**Request Body:**
```json
{
  "condition": {
    "exchange": "NSE",
    "tradingsymbol": "RELIANCE",
    "last_price": 2456.75,
    "trigger_values": [2500.00],
    "operators": ["gte"]
  },
  "orders": [
    {
      "exchange": "NSE",
      "tradingsymbol": "RELIANCE",
      "transaction_type": "SELL",
      "quantity": 1,
      "product": "CNC",
      "order_type": "LIMIT",
      "price": 2500.00
    }
  ]
}
```

### Get GTT Orders
```http
GET /gtt/triggers
```

### Get GTT by ID
```http
GET /gtt/triggers/{trigger_id}
```

### Modify GTT
```http
PUT /gtt/triggers/{trigger_id}
```

### Delete GTT
```http
DELETE /gtt/triggers/{trigger_id}
```

---

## 💼 Mutual Funds

### Get MF Orders
```http
GET /mf/orders
```

### Place MF Order
```http
POST /mf/orders
```

**Request Body:**
```json
{
  "tradingsymbol": "INF090I01239",
  "transaction_type": "BUY",
  "amount": 5000,
  "tag": "my_mf_order"
}
```

### Cancel MF Order
```http
DELETE /mf/orders/{order_id}
```

### Get MF SIPs
```http
GET /mf/sips
```

### Place MF SIP
```http
POST /mf/sips
```

**Request Body:**
```json
{
  "tradingsymbol": "INF090I01239",
  "amount": 5000,
  "instalments": 12,
  "frequency": "monthly",
  "instalment_day": 5,
  "tag": "my_sip"
}
```

### Modify MF SIP
```http
PUT /mf/sips/{sip_id}
```

### Delete MF SIP
```http
DELETE /mf/sips/{sip_id}
```

### Get MF Holdings
```http
GET /mf/holdings
```

---

## ⚠️ Error Handling

### Common Error Responses

**401 Unauthorized:**
```json
{
  "status": "error",
  "error_type": "TokenException",
  "message": "Invalid token"
}
```

**403 Forbidden:**
```json
{
  "status": "error",
  "error_type": "PermissionException",
  "message": "Access denied"
}
```

**429 Too Many Requests:**
```json
{
  "status": "error",
  "error_type": "RateLimitException",
  "message": "Rate limit exceeded"
}
```

**500 Internal Server Error:**
```json
{
  "status": "error",
  "error_type": "GeneralException",
  "message": "Internal server error"
}
```

### Error Types:
- `TokenException` - Invalid or expired token
- `PermissionException` - Insufficient permissions
- `OrderException` - Order-related errors
- `InputException` - Invalid input parameters
- `NetworkException` - Network connectivity issues
- `GeneralException` - General server errors
- `RateLimitException` - Rate limit exceeded

---

## 🚦 Rate Limits

### API Rate Limits:
- **Market Data**: 3 requests per second
- **Orders**: 10 requests per second
- **Historical Data**: 1 request per second
- **Portfolio**: 1 request per second

### Best Practices:
1. **Implement exponential backoff** for retries
2. **Cache frequently accessed data** (instruments, quotes)
3. **Use WebSocket** for real-time data when possible
4. **Batch requests** when possible
5. **Monitor rate limit headers**

---

## 💡 Examples & Use Cases

### 1. Basic Market Data Fetching
```python
from zerodha_api_complete import ZerodhaAPI

# Initialize API
api = ZerodhaAPI()

# Get live quotes
quotes = api.get_quotes(["NSE:RELIANCE", "NSE:TCS", "NSE:INFY"])
for symbol, data in quotes.items():
    print(f"{symbol}: ₹{data['last_price']:.2f}")

# Get historical data
historical = api.get_historical_data(
    instrument_token=738561,  # RELIANCE
    from_date="2024-01-01",
    to_date="2024-01-31",
    interval="day"
)
```

### 2. Portfolio Management
```python
# Get portfolio
portfolio = api.get_portfolio()
for holding in portfolio:
    print(f"{holding['tradingsymbol']}: {holding['quantity']} @ ₹{holding['average_price']:.2f}")

# Get positions
positions = api.get_positions()
print(f"Day positions: {len(positions['day'])}")
print(f"Net positions: {len(positions['net'])}")
```

### 3. Order Management
```python
# Place a market order
order_id = api.place_order(
    variety="regular",
    exchange="NSE",
    tradingsymbol="RELIANCE",
    transaction_type="BUY",
    quantity=1,
    product="CNC",
    order_type="MARKET"
)
print(f"Order placed: {order_id}")

# Get order status
orders = api.get_orders()
for order in orders:
    print(f"Order {order['order_id']}: {order['status']}")
```

### 4. GTT Orders
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

### 5. Mutual Fund Operations
```python
# Place MF order
mf_order_id = api.place_mf_order(
    tradingsymbol="INF090I01239",
    transaction_type="BUY",
    amount=5000
)

# Place SIP
sip_id = api.place_mf_sip(
    tradingsymbol="INF090I01239",
    amount=5000,
    instalments=12,
    frequency="monthly",
    instalment_day=5
)
```

---

## 🎯 Best Practices

### 1. Authentication
- **Store credentials securely** in environment variables
- **Implement token refresh** mechanism
- **Handle token expiration** gracefully

### 2. Error Handling
- **Always check for errors** in API responses
- **Implement retry logic** with exponential backoff
- **Log errors** for debugging

### 3. Rate Limiting
- **Respect rate limits** to avoid blocking
- **Implement request queuing** for high-frequency operations
- **Use caching** for frequently accessed data

### 4. Data Management
- **Cache instruments list** (rarely changes)
- **Store historical data** locally when possible
- **Implement data validation** before API calls

### 5. Order Management
- **Validate orders** before placing
- **Check market hours** before trading
- **Implement order status tracking**
- **Use appropriate order types** (MARKET vs LIMIT)

### 6. Security
- **Never expose API keys** in code
- **Use HTTPS** for all API calls
- **Implement request signing** if required
- **Monitor API usage** for anomalies

---

## 🔧 Utility Functions

### Market Status Check
```python
# Check if market is open
if api.is_market_open():
    print("Market is open - trading allowed")
else:
    print("Market is closed - trading not allowed")
```

### Instrument Token Lookup
```python
# Get instrument token
token = api.get_instrument_token("NSE", "RELIANCE")
print(f"RELIANCE token: {token}")

# Get trading symbol
symbol = api.get_trading_symbol("NSE", 738561)
print(f"Token 738561 symbol: {symbol}")
```

### Format Instrument Key
```python
# Format instrument key
key = api.format_instrument_key("NSE", "RELIANCE")
print(f"Instrument key: {key}")  # NSE:RELIANCE
```

---

## 🔧 Debug Tools & Troubleshooting

### Debug Tools Overview

This guide includes comprehensive debug tools to help you troubleshoot and understand the Zerodha API:

#### 1. `debug_api.py` - API Diagnostic Tool

**Purpose:** Comprehensive API debugging and diagnostics

**Features:**
- Environment variable validation
- API credential verification
- Network connectivity testing
- Response structure analysis
- Detailed error reporting

**Usage:**
```bash
python debug_api.py
```

**When to use:**
- First time API setup
- Authentication issues
- Network connectivity problems
- API response errors

**Example Output:**
```
🔍 DEBUGGING ZERODHA API SETUP
1️⃣ Environment Variables:
ZERODHA_API_KEY: ✅ Set
ZERODHA_ACCESS_TOKEN: ✅ Set

2️⃣ .env File Check:
✅ .env file exists
✅ ZERODHA_API_KEY found in .env

3️⃣ API Response Debug:
✅ Profile API call successful
📋 Full API Response:
{
  "status": "success",
  "data": {
    "user_name": "Your Name",
    "email": "your@email.com"
  }
}
```

#### 2. `debug_responses.py` - Response Structure Analyzer

**Purpose:** Analyze and understand API response structures

**Features:**
- Response type analysis
- Content structure inspection
- Data format understanding
- Response validation

**Usage:**
```bash
python debug_responses.py
```

**When to use:**
- Understanding API response formats
- Debugging data parsing issues
- Development and testing
- Response structure analysis

**Example Output:**
```
🔍 DEBUGGING ZERODHA API RESPONSE STRUCTURES
1️⃣ QUOTES API RESPONSE:
Type: <class 'dict'>
Content: {'status': 'success', 'data': {'NSE:RELIANCE': {...}}}

2️⃣ PORTFOLIO API RESPONSE:
Type: <class 'dict'>
Content: {'status': 'success', 'data': [...]}
```

### Common Issues & Solutions

#### Issue 1: Authentication Errors
```bash
# Run debug tool
python debug_api.py

# Check output for:
❌ ZERODHA_API_KEY: Not Set
❌ ZERODHA_ACCESS_TOKEN: Not Set
```

**Solution:**
1. Create `.env` file with your credentials
2. Ensure environment variables are set correctly
3. Verify API key and access token are valid

#### Issue 2: Response Parsing Errors
```bash
# Run response analyzer
python debug_responses.py

# Check response structure
Type: <class 'dict'>
Content: {'status': 'success', 'data': [...]}
```

**Solution:**
1. Access data using `response['data']` instead of `response` directly
2. Check for `status` field before processing data
3. Handle empty data arrays gracefully

#### Issue 3: Network Connectivity Issues
```bash
# Run debug tool
python debug_api.py

# Check network section
❌ Network test failed: Connection timeout
```

**Solution:**
1. Check internet connection
2. Verify Zerodha server status
3. Check firewall settings
4. Try again during market hours

### Debug Workflow

#### Step 1: Initial Setup
```bash
# Check environment setup
python debug_api.py
```

#### Step 2: Understand Response Format
```bash
# Analyze API responses
python debug_responses.py
```

#### Step 3: Test with Examples
```bash
# Run practical examples
python example_usage.py
```

#### Step 4: Use in Production
```python
from zerodha_api_complete import ZerodhaAPI

# Initialize and use
api = ZerodhaAPI()
quotes = api.get_quotes(["NSE:RELIANCE"])
```

### Debug Tool Features Comparison

| Feature | debug_api.py | debug_responses.py |
|---------|--------------|-------------------|
| **Environment Check** | ✅ | ❌ |
| **Network Testing** | ✅ | ❌ |
| **Response Analysis** | ✅ | ✅ |
| **Error Diagnosis** | ✅ | ❌ |
| **Data Structure** | ❌ | ✅ |
| **Format Understanding** | ❌ | ✅ |

### Best Practices

1. **Always run debug tools first** when setting up API
2. **Use debug_responses.py** to understand data structures
3. **Check debug_api.py output** for authentication issues
4. **Run examples** to test your implementation
5. **Handle errors gracefully** in production code

## 📞 Support & Resources

### Official Documentation:
- [Zerodha Kite Connect](https://kite.trade/)
- [API Documentation](https://kite.trade/docs/connect/v3/)

### Community:
- [Zerodha Developer Forum](https://kite.trade/forum/)
- [GitHub Issues](https://github.com/zerodhatech/pykiteconnect/issues)

### Support:
- Email: connect@zerodha.com
- Phone: +91-80-4040-2020

---

## 📝 License

This guide is provided for educational purposes. Please refer to Zerodha's official terms and conditions for commercial usage.

---

**Last Updated:** January 2025  
**Version:** 1.0  
**Author:** AI Assistant
