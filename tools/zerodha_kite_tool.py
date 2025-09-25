import requests
import pandas as pd
from datetime import datetime, timedelta
from crewai.tools import tool
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ZerodhaKiteAPI:
    """
    Zerodha Kite Connect API integration for financial data and trading operations.
    """
    
    def __init__(self, api_key, access_token=None):
        """
        Initialize Zerodha Kite API client.
        
        Parameters:
            api_key (str): Your Kite Connect API key
            access_token (str): User's access token (obtained after authentication)
        """
        self.api_key = api_key
        self.access_token = access_token
        self.base_url = "https://api.kite.trade"
        self.headers = {
            "X-Kite-Version": "3",
            "Authorization": f"token {api_key}:{access_token}" if access_token else f"token {api_key}"
        }
    
    def get_quote(self, instruments):
        """
        Get real-time quotes for instruments.
        
        Parameters:
            instruments (list): List of instrument tokens or trading symbols
            
        Returns:
            dict: Real-time quote data
        """
        url = f"{self.base_url}/quote"
        params = {"i": ",".join(instruments)}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch quotes: {str(e)}"}
    
    def get_historical_data(self, instrument_token, from_date, to_date, interval="day"):
        """
        Get historical candle data for an instrument.
        
        Parameters:
            instrument_token (str): Instrument token
            from_date (str): Start date in YYYY-MM-DD format
            to_date (str): End date in YYYY-MM-DD format
            interval (str): Data interval (minute, 3minute, 5minute, 15minute, 30minute, 60minute, day)
            
        Returns:
            dict: Historical candle data
        """
        url = f"{self.base_url}/instruments/historical/{instrument_token}/{interval}"
        params = {
            "from": from_date,
            "to": to_date
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch historical data: {str(e)}"}
    
    def get_instruments(self, exchange=None):
        """
        Get list of all instruments.
        
        Parameters:
            exchange (str): Exchange name (NSE, BSE, NFO, BFO, CDS, MCX)
            
        Returns:
            dict: List of instruments
        """
        url = f"{self.base_url}/instruments"
        if exchange:
            url += f"/{exchange}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch instruments: {str(e)}"}
    
    def get_profile(self):
        """
        Get user profile information.
        
        Returns:
            dict: User profile data
        """
        url = f"{self.base_url}/user/profile"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch profile: {str(e)}"}
    
    def get_positions(self):
        """
        Get user's positions.
        
        Returns:
            dict: Position data
        """
        url = f"{self.base_url}/portfolio/positions"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch positions: {str(e)}"}
    
    def get_holdings(self):
        """
        Get user's holdings.
        
        Returns:
            dict: Holdings data
        """
        url = f"{self.base_url}/portfolio/holdings"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch holdings: {str(e)}"}

def transform_zerodha_quote_data(quote_data):
    """
    Transform Zerodha quote data to match our standard format.
    
    Parameters:
        quote_data (dict): Raw quote data from Zerodha API
    
    Returns:
        dict: Transformed data in standard format
    """
    transformed_data = {}
    
    for instrument, data in quote_data.items():
        if "error" in data:
            continue
            
        ohlc = data.get("ohlc", {})
        last_price = data.get("last_price", 0)
        net_change = data.get("net_change", 0)
        ohlc_high = ohlc.get("high", 0)
        ohlc_low = ohlc.get("low", 0)
        ohlc_open = ohlc.get("open", 0)
        ohlc_close = ohlc.get("close", 0)
        
        # Calculate percentage change
        change_percent = (net_change / ohlc_close * 100) if ohlc_close != 0 else 0
        
        transformed_data[instrument] = {
            "current_price": last_price,
            "previous_close": ohlc_close,
            "open_price": ohlc_open,
            "day_low": ohlc_low,
            "day_high": ohlc_high,
            "daily_change": net_change,
            "daily_change_percent": change_percent,
            "volume": data.get("volume", 0),
            "average_price": data.get("average_price", 0),
            "last_quantity": data.get("last_quantity", 0),
            "last_trade_time": data.get("last_trade_time", ""),
            "oi": data.get("oi", 0),  # Open Interest for F&O
            "oi_day_high": data.get("oi_day_high", 0),
            "oi_day_low": data.get("oi_day_low", 0),
            "timestamp": data.get("timestamp", ""),
            "currency": "INR"
        }
    
    return transformed_data

@tool("Zerodha Live Stock Information Tool")
def get_zerodha_stock_data(instrument_token: str, api_key: str = None, access_token: str = None):
    """
    💡 Retrieves comprehensive stock information using Zerodha Kite Connect API.
    
    Parameters:
        instrument_token (str): Zerodha instrument token (e.g., "NSE:RELIANCE", "BSE:500325")
        api_key (str): Your Zerodha Kite Connect API key (optional, will use env var if not provided)
        access_token (str): User's access token (optional for quote data, will use env var if not provided)
    
    Returns:
        str: A comprehensive summary of stock data from Zerodha
    """
    
    try:
        # Use environment variables if not provided
        if not api_key:
            api_key = os.getenv("ZERODHA_API_KEY")
        if not access_token:
            access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
        
        if not api_key:
            return "Error: ZERODHA_API_KEY not found. Please provide api_key parameter or set ZERODHA_API_KEY environment variable."
        
        # Initialize Zerodha API client
        kite = ZerodhaKiteAPI(api_key, access_token)
        
        # Get real-time quote
        quote_data = kite.get_quote([instrument_token])
        
        if "error" in quote_data:
            return f"Error fetching data: {quote_data['error']}"
        
        # Transform the data
        transformed_data = transform_zerodha_quote_data(quote_data)
        
        if instrument_token not in transformed_data:
            return f"Could not fetch data for {instrument_token}. Please check the instrument token."
        
        data = transformed_data[instrument_token]
        
        # Format large numbers for better readability
        def format_number(num):
            if num is None:
                return "N/A"
            if isinstance(num, (int, float)) and num >= 1e9:
                return f"{num/1e9:.2f}B"
            elif isinstance(num, (int, float)) and num >= 1e6:
                return f"{num/1e6:.2f}M"
            elif isinstance(num, (int, float)) and num >= 1e3:
                return f"{num/1e3:.2f}K"
            else:
                return f"{num:,}" if isinstance(num, (int, float)) else str(num)
        
        return (
            f"=== ZERODHA STOCK ANALYSIS: {instrument_token.upper()} ===\n\n"
            
            f"📊 BASIC PRICE INFORMATION:\n"
            f"• Current Price: {data['current_price']} {data['currency']}\n"
            f"• Previous Close: {data['previous_close']} {data['currency']}\n"
            f"• Open Price: {data['open_price']} {data['currency']}\n"
            f"• Day Low: {data['day_low']} {data['currency']}\n"
            f"• Day High: {data['day_high']} {data['currency']}\n"
            f"• Daily Change: {data['daily_change']} {data['currency']}\n"
            f"• Daily Change %: {data['daily_change_percent']:.2f}%\n\n"
            
            f"📊 TRADING INFORMATION:\n"
            f"• Volume: {format_number(data['volume'])}\n"
            f"• Average Price: {data['average_price']} {data['currency']}\n"
            f"• Last Quantity: {data['last_quantity']}\n"
            f"• Last Trade Time: {data['last_trade_time']}\n"
            f"• Open Interest: {format_number(data['oi'])}\n"
            f"• OI Day High: {format_number(data['oi_day_high'])}\n"
            f"• OI Day Low: {format_number(data['oi_day_low'])}\n\n"
            
            f"🕐 Data Timestamp: {data['timestamp']}\n"
            f"💱 Currency: {data['currency']}\n"
        )
        
    except Exception as e:
        return f"Error processing Zerodha data: {str(e)}"

@tool("Zerodha Historical Data Tool")
def get_zerodha_historical_data(instrument_token: str, from_date: str, to_date: str, 
                               interval: str = "day", api_key: str = None, access_token: str = None):
    """
    💡 Retrieves historical candle data using Zerodha Kite Connect API.
    
    Parameters:
        instrument_token (str): Zerodha instrument token
        from_date (str): Start date in YYYY-MM-DD format
        to_date (str): End date in YYYY-MM-DD format
        interval (str): Data interval (minute, 3minute, 5minute, 15minute, 30minute, 60minute, day)
        api_key (str): Your Zerodha Kite Connect API key (optional, will use env var if not provided)
        access_token (str): User's access token (optional, will use env var if not provided)
    
    Returns:
        str: Historical data analysis and trends
    """
    
    try:
        # Use environment variables if not provided
        if not api_key:
            api_key = os.getenv("ZERODHA_API_KEY")
        if not access_token:
            access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
        
        if not api_key:
            return "Error: ZERODHA_API_KEY not found. Please provide api_key parameter or set ZERODHA_API_KEY environment variable."
        if not access_token:
            return "Error: ZERODHA_ACCESS_TOKEN not found. Please provide access_token parameter or set ZERODHA_ACCESS_TOKEN environment variable."
        
        # Initialize Zerodha API client
        kite = ZerodhaKiteAPI(api_key, access_token)
        
        # Get historical data
        historical_data = kite.get_historical_data(instrument_token, from_date, to_date, interval)
        
        if "error" in historical_data:
            return f"Error fetching historical data: {historical_data['error']}"
        
        candles = historical_data.get("data", {}).get("candles", [])
        
        if not candles:
            return f"No historical data found for {instrument_token} in the specified date range."
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        # Calculate technical indicators
        df['sma_5'] = df['close'].rolling(window=5).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        # Calculate price change
        df['price_change'] = df['close'].pct_change() * 100
        
        # Calculate volatility
        df['volatility'] = df['price_change'].rolling(window=20).std()
        
        # Get latest values
        latest = df.iloc[-1]
        first = df.iloc[0]
        
        # Calculate overall performance
        total_return = ((latest['close'] - first['close']) / first['close']) * 100
        max_price = df['high'].max()
        min_price = df['low'].min()
        avg_volume = df['volume'].mean()
        
        # Trend analysis
        recent_trend = "Bullish" if latest['close'] > latest['sma_20'] else "Bearish"
        
        return (
            f"=== ZERODHA HISTORICAL ANALYSIS: {instrument_token.upper()} ===\n\n"
            
            f"📅 DATE RANGE: {from_date} to {to_date}\n"
            f"⏱️ INTERVAL: {interval}\n"
            f"📊 TOTAL CANDLES: {len(candles)}\n\n"
            
            f"💰 PRICE PERFORMANCE:\n"
            f"• Starting Price: {first['close']:.2f} INR\n"
            f"• Ending Price: {latest['close']:.2f} INR\n"
            f"• Total Return: {total_return:.2f}%\n"
            f"• Highest Price: {max_price:.2f} INR\n"
            f"• Lowest Price: {min_price:.2f} INR\n"
            f"• Price Range: {max_price - min_price:.2f} INR\n\n"
            
            f"📈 TECHNICAL INDICATORS:\n"
            f"• Current SMA 5: {latest['sma_5']:.2f} INR\n"
            f"• Current SMA 20: {latest['sma_20']:.2f} INR\n"
            f"• Current SMA 50: {latest['sma_50']:.2f} INR\n"
            f"• Current Volatility: {latest['volatility']:.2f}%\n"
            f"• Recent Trend: {recent_trend}\n\n"
            
            f"📊 VOLUME ANALYSIS:\n"
            f"• Average Volume: {format_number(avg_volume)}\n"
            f"• Latest Volume: {format_number(latest['volume'])}\n"
            f"• Volume Trend: {'High' if latest['volume'] > avg_volume else 'Low'}\n\n"
            
            f"🎯 TRADING INSIGHTS:\n"
            f"• Price vs SMA 20: {'Above' if latest['close'] > latest['sma_20'] else 'Below'}\n"
            f"• Price vs SMA 50: {'Above' if latest['close'] > latest['sma_50'] else 'Below'}\n"
            f"• Volatility Level: {'High' if latest['volatility'] > df['volatility'].mean() else 'Low'}\n"
        )
        
    except Exception as e:
        return f"Error processing historical data: {str(e)}"

@tool("Zerodha Portfolio Information Tool")
def get_zerodha_portfolio_info(api_key: str = None, access_token: str = None):
    """
    💡 Retrieves user's portfolio information using Zerodha Kite Connect API.
    
    Parameters:
        api_key (str): Your Zerodha Kite Connect API key (optional, will use env var if not provided)
        access_token (str): User's access token (optional, will use env var if not provided)
    
    Returns:
        str: Portfolio summary and holdings information
    """
    
    try:
        # Use environment variables if not provided
        if not api_key:
            api_key = os.getenv("ZERODHA_API_KEY")
        if not access_token:
            access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
        
        if not api_key:
            return "Error: ZERODHA_API_KEY not found. Please provide api_key parameter or set ZERODHA_API_KEY environment variable."
        if not access_token:
            return "Error: ZERODHA_ACCESS_TOKEN not found. Please provide access_token parameter or set ZERODHA_ACCESS_TOKEN environment variable."
        
        # Initialize Zerodha API client
        kite = ZerodhaKiteAPI(api_key, access_token)
        
        # Get user profile
        profile = kite.get_profile()
        if "error" in profile:
            return f"Error fetching profile: {profile['error']}"
        
        # Get positions
        positions = kite.get_positions()
        if "error" in positions:
            return f"Error fetching positions: {positions['error']}"
        
        # Get holdings
        holdings = kite.get_holdings()
        if "error" in holdings:
            return f"Error fetching holdings: {holdings['error']}"
        
        # Process portfolio data
        total_holdings = len(holdings.get("data", []))
        total_positions = len(positions.get("data", {}).get("net", []))
        
        # Calculate total portfolio value
        total_value = 0
        for holding in holdings.get("data", []):
            total_value += holding.get("average_price", 0) * holding.get("quantity", 0)
        
        return (
            f"=== ZERODHA PORTFOLIO SUMMARY ===\n\n"
            
            f"👤 USER PROFILE:\n"
            f"• User ID: {profile.get('data', {}).get('user_id', 'N/A')}\n"
            f"• User Name: {profile.get('data', {}).get('user_name', 'N/A')}\n"
            f"• Email: {profile.get('data', {}).get('email', 'N/A')}\n"
            f"• Broker: {profile.get('data', {}).get('broker', 'N/A')}\n\n"
            
            f"📊 PORTFOLIO OVERVIEW:\n"
            f"• Total Holdings: {total_holdings}\n"
            f"• Total Positions: {total_positions}\n"
            f"• Estimated Portfolio Value: {total_value:,.2f} INR\n\n"
            
            f"💼 RECENT HOLDINGS:\n"
        ) + "\n".join([
            f"• {holding.get('tradingsymbol', 'N/A')}: {holding.get('quantity', 0)} shares @ {holding.get('average_price', 0):.2f} INR"
            for holding in holdings.get("data", [])[:5]  # Show first 5 holdings
        ])
        
    except Exception as e:
        return f"Error processing portfolio data: {str(e)}"

def format_number(num):
    """Helper function to format large numbers"""
    if num is None:
        return "N/A"
    if isinstance(num, (int, float)) and num >= 1e9:
        return f"{num/1e9:.2f}B"
    elif isinstance(num, (int, float)) and num >= 1e6:
        return f"{num/1e6:.2f}M"
    elif isinstance(num, (int, float)) and num >= 1e3:
        return f"{num/1e3:.2f}K"
    else:
        return f"{num:,}" if isinstance(num, (int, float)) else str(num)

# Example usage and testing
if __name__ == "__main__":
    # Get API credentials from environment variables
    API_KEY = os.getenv("ZERODHA_API_KEY")
    ACCESS_TOKEN = os.getenv("ZERODHA_ACCESS_TOKEN")
    
    if not API_KEY:
        print("❌ ZERODHA_API_KEY not found in environment variables")
        print("Please add your Zerodha API key to .env file:")
        print("ZERODHA_API_KEY=your_api_key_here")
        print("ZERODHA_ACCESS_TOKEN=your_access_token_here")
        exit(1)
    
    print("🚀 Testing Zerodha Kite Connect API Integration\n")
    
    # Test with a popular Indian stock
    print("📊 Testing Real-time Stock Data:")
    result = get_zerodha_stock_data.func("NSE:RELIANCE", API_KEY, ACCESS_TOKEN)
    print(result)
    
    # Test historical data if access token is available
    if ACCESS_TOKEN:
        print("\n📈 Testing Historical Data:")
        from datetime import datetime, timedelta
        
        # Get data for last 7 days
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        historical_result = get_zerodha_historical_data.func(
            "NSE:RELIANCE", 
            start_date, 
            end_date, 
            "day",
            API_KEY, 
            ACCESS_TOKEN
        )
        print(historical_result)
        
        print("\n💼 Testing Portfolio Information:")
        portfolio_result = get_zerodha_portfolio_info.func(API_KEY, ACCESS_TOKEN)
        print(portfolio_result)
    else:
        print("\n⚠️  ACCESS_TOKEN not found. Historical data and portfolio features require authentication.")
        print("Please add your Zerodha access token to .env file:")
        print("ZERODHA_ACCESS_TOKEN=your_access_token_here")
