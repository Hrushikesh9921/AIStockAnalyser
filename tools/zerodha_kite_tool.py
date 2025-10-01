"""
Zerodha Kite Connect Tools for CrewAI
Simplified version that works with CrewAI's parameter handling
"""

import os
import requests
from datetime import datetime, timedelta
from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()

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
        
        # Ensure data is a dictionary
        if not isinstance(data, dict):
            continue
            
        ohlc = data.get("ohlc", {})
        last_price = data.get("last_price", 0)
        net_change = data.get("net_change", 0)
        ohlc_high = ohlc.get("high", 0) if isinstance(ohlc, dict) else 0
        ohlc_low = ohlc.get("low", 0) if isinstance(ohlc, dict) else 0
        ohlc_open = ohlc.get("open", 0) if isinstance(ohlc, dict) else 0
        ohlc_close = ohlc.get("close", 0) if isinstance(ohlc, dict) else 0
        
        # Calculate percentage change
        change_percent = (net_change / ohlc_close * 100) if ohlc_close != 0 else 0
        
        transformed_data[instrument] = {
            "current_price": last_price,
            "previous_close": ohlc_close,
            "open_price": ohlc_open,
            "day_high": ohlc_high,
            "day_low": ohlc_low,
            "net_change": net_change,
            "change_percent": change_percent,
            "volume": data.get("volume", 0),
            "average_volume": data.get("average_volume", 0),
            "last_quantity": data.get("last_quantity", 0),
            "buy_quantity": data.get("buy_quantity", 0),
            "sell_quantity": data.get("sell_quantity", 0),
            "oi": data.get("oi", 0),
            "oi_day_high": data.get("oi_day_high", 0),
            "oi_day_low": data.get("oi_day_low", 0),
            "timestamp": data.get("timestamp", ""),
            "last_trade_time": data.get("last_trade_time", ""),
            "currency": "INR"
        }
    
    return transformed_data

@tool("Zerodha Live Stock Information Tool")
def get_zerodha_stock_data(instrument_token: str):
    """
    💡 Retrieves comprehensive stock information using Zerodha Kite Connect API.
    
    Parameters:
        instrument_token (str): Zerodha instrument token (e.g., "NSE:RELIANCE", "BSE:500325")
    
    Returns:
        str: A comprehensive summary of stock data from Zerodha
    """
    
    try:
        # Get credentials from environment variables
        api_key = os.getenv("ZERODHA_API_KEY")
        access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
        
        if not api_key:
            return "Error: ZERODHA_API_KEY not found. Please set ZERODHA_API_KEY environment variable."
        
        if not access_token:
            return "Error: ZERODHA_ACCESS_TOKEN not found. Please set ZERODHA_ACCESS_TOKEN environment variable."
        
        # Initialize Zerodha API client using official library
        from kiteconnect import KiteConnect
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)
        
        # Convert instrument token format if needed
        numeric_token = None
        if ":" in instrument_token:
            # Format like "NSE:RELIANCE" - need to get numeric token
            exchange = instrument_token.split(":")[0]
            symbol = instrument_token.split(":")[1]
            
            # Get instruments list to find the numeric token
            instruments = kite.instruments(exchange)
            for inst in instruments:
                if inst['tradingsymbol'] == symbol:
                    numeric_token = inst['instrument_token']
                    break
            
            if not numeric_token:
                return f"Error: Could not find instrument token for {instrument_token}. Please check the symbol."
        else:
            # Check if it's a numeric string or symbol name
            try:
                numeric_token = int(instrument_token)
            except ValueError:
                # It's a symbol name, try to find it in NSE instruments
                instruments = kite.instruments("NSE")
                for inst in instruments:
                    if inst['tradingsymbol'] == instrument_token:
                        numeric_token = inst['instrument_token']
                        break
                
                if not numeric_token:
                    return f"Error: Could not find instrument token for {instrument_token}. Please use format 'NSE:SYMBOL' or numeric token."
        
        # Get real-time quote
        quote_data = kite.quote(numeric_token)
        
        if "error" in quote_data:
            return f"Error fetching data: {quote_data['error']}"
        
        # Transform the data
        transformed_data = transform_zerodha_quote_data(quote_data)
        
        if str(numeric_token) not in transformed_data:
            return f"Could not fetch data for {instrument_token}. Please check the instrument token."
        
        data = transformed_data[str(numeric_token)]
        
        # Format the output
        output = f"""
=== ZERODHA LIVE STOCK DATA: {instrument_token} ===

📊 BASIC PRICE INFORMATION:
• Current Price: {data['current_price']:.2f} INR
• Previous Close: {data['previous_close']:.2f} INR
• Open Price: {data['open_price']:.2f} INR
• Day High: {data['day_high']:.2f} INR
• Day Low: {data['day_low']:.2f} INR
• Net Change: {data['net_change']:.2f} INR
• Change %: {data['change_percent']:.2f}%

📈 VOLUME INFORMATION:
• Current Volume: {data['volume']:,}
• Average Volume: {data['average_volume']:,}
• Last Quantity: {data['last_quantity']:,}
• Buy Quantity: {data['buy_quantity']:,}
• Sell Quantity: {data['sell_quantity']:,}

📊 TRADING INFORMATION:
• Open Interest: {data['oi']:,}
• OI Day High: {data['oi_day_high']:,}
• OI Day Low: {data['oi_day_low']:,}
• Last Trade Time: {data['last_trade_time']}
• Timestamp: {data['timestamp']}

💱 Currency: {data['currency']}

📊 ZERODHA MARKET INDICATORS:
• Daily Range: {data['day_high'] - data['day_low']:.2f} INR ({(data['day_high'] - data['day_low']) / data['current_price'] * 100:.2f}%)
• Price vs Day High: {((data['current_price'] - data['day_low']) / (data['day_high'] - data['day_low']) * 100):.1f}% (0%=Low, 100%=High)
• Typical Daily Movement: 1-3% (Large Cap Stock)
• Realistic Intraday Target: ±0.5-1.5%
• Realistic Swing Target: ±2-5%

"""
        
        return output
        
    except Exception as e:
        return f"Error processing Zerodha data: {str(e)}"

@tool("Zerodha Historical Data Tool")
def get_zerodha_historical_data(instrument_token: str, from_date: str = None, to_date: str = None, interval: str = "day"):
    """
    💡 Retrieves historical candle data using Zerodha Kite Connect API.
    
    Parameters:
        instrument_token (str): Zerodha instrument token (e.g., "NSE:RELIANCE" or "738561")
        from_date (str): Start date in YYYY-MM-DD format (default: 30 days ago)
        to_date (str): End date in YYYY-MM-DD format (default: today)
        interval (str): Data interval (minute, 3minute, 5minute, 15minute, 30minute, 60minute, day)
    
    Returns:
        str: Historical data analysis and trends
    """
    
    try:
        # Get credentials from environment variables
        api_key = os.getenv("ZERODHA_API_KEY")
        access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
        
        if not api_key:
            return "Error: ZERODHA_API_KEY not found. Please set ZERODHA_API_KEY environment variable."
        
        if not access_token:
            return "Error: ZERODHA_ACCESS_TOKEN not found. Please set ZERODHA_ACCESS_TOKEN environment variable."
        
        # Set default dates if not provided
        if not from_date:
            from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
        
        # Initialize Zerodha API client
        from kiteconnect import KiteConnect
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)
        
        # Convert instrument token format if needed
        numeric_token = None
        if ":" in instrument_token:
            # Format like "NSE:RELIANCE" - need to get numeric token
            exchange = instrument_token.split(":")[0]
            symbol = instrument_token.split(":")[1]
            
            # Get instruments list to find the numeric token
            instruments = kite.instruments(exchange)
            for inst in instruments:
                if inst['tradingsymbol'] == symbol:
                    numeric_token = inst['instrument_token']
                    break
            
            if not numeric_token:
                return f"Error: Could not find instrument token for {instrument_token}. Please check the symbol."
        else:
            # Check if it's a numeric string or symbol name
            try:
                numeric_token = int(instrument_token)
            except ValueError:
                # It's a symbol name, try to find it in NSE instruments
                instruments = kite.instruments("NSE")
                for inst in instruments:
                    if inst['tradingsymbol'] == instrument_token:
                        numeric_token = inst['instrument_token']
                        break
                
                if not numeric_token:
                    return f"Error: Could not find instrument token for {instrument_token}. Please use format 'NSE:SYMBOL' or numeric token."
        
        # Get historical data
        historical_data = kite.historical_data(
            instrument_token=numeric_token,
            from_date=from_date,
            to_date=to_date,
            interval=interval
        )
        
        if not historical_data:
            return f"No historical data found for {instrument_token} from {from_date} to {to_date}"
        
        # Calculate basic statistics
        prices = [candle['close'] for candle in historical_data]
        volumes = [candle['volume'] for candle in historical_data]
        
        if not prices:
            return f"No price data found for {instrument_token}"
        
        current_price = prices[-1]
        first_price = prices[0]
        highest_price = max(prices)
        lowest_price = min(prices)
        total_change = current_price - first_price
        total_change_percent = (total_change / first_price) * 100
        
        avg_volume = sum(volumes) / len(volumes) if volumes else 0
        max_volume = max(volumes) if volumes else 0
        
        # Format the output
        output = f"""
=== ZERODHA HISTORICAL DATA: {instrument_token} ===

📅 PERIOD: {from_date} to {to_date}
📊 INTERVAL: {interval}

📈 PRICE ANALYSIS:
• First Price: {first_price:.2f} INR
• Current Price: {current_price:.2f} INR
• Highest Price: {highest_price:.2f} INR
• Lowest Price: {lowest_price:.2f} INR
• Total Change: {total_change:.2f} INR
• Total Change %: {total_change_percent:.2f}%

📊 VOLUME ANALYSIS:
• Average Volume: {avg_volume:,.0f}
• Maximum Volume: {max_volume:,.0f}
• Data Points: {len(historical_data)}

📈 TREND ANALYSIS:
• Price Range: {highest_price - lowest_price:.2f} INR ({(highest_price - lowest_price) / current_price * 100:.2f}%)
• Volatility: {((highest_price - lowest_price) / current_price * 100):.2f}%
• Trend Direction: {'Bullish' if total_change > 0 else 'Bearish' if total_change < 0 else 'Sideways'}

💡 INDIAN MARKET INSIGHTS:
• Historical pattern analysis for Indian market conditions
• Volume trends specific to NSE/BSE trading
• Price movement patterns over the selected period
• Market sentiment indicators from historical data

"""
        
        return output
        
    except Exception as e:
        return f"Error fetching historical data: {str(e)}"

@tool("Zerodha Portfolio Information Tool")
def get_zerodha_portfolio_info():
    """
    💡 Retrieves portfolio information using Zerodha Kite Connect API.
    
    Returns:
        str: Portfolio summary and holdings
    """
    
    try:
        # Get credentials from environment variables
        api_key = os.getenv("ZERODHA_API_KEY")
        access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
        
        if not api_key:
            return "Error: ZERODHA_API_KEY not found. Please set ZERODHA_API_KEY environment variable."
        
        if not access_token:
            return "Error: ZERODHA_ACCESS_TOKEN not found. Please set ZERODHA_ACCESS_TOKEN environment variable."
        
        # Initialize Zerodha API client
        from kiteconnect import KiteConnect
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)
        
        # Get portfolio
        portfolio = kite.portfolio()
        
        if not portfolio:
            return "No portfolio data found or portfolio is empty."
        
        # Calculate summary statistics
        total_investment = sum([holding['average_price'] * holding['quantity'] for holding in portfolio])
        total_current_value = sum([holding['last_price'] * holding['quantity'] for holding in portfolio])
        total_pnl = total_current_value - total_investment
        total_pnl_percent = (total_pnl / total_investment * 100) if total_investment > 0 else 0
        
        # Format the output
        output = f"""
=== ZERODHA PORTFOLIO SUMMARY ===

💰 PORTFOLIO OVERVIEW:
• Total Investment: {total_investment:,.2f} INR
• Current Value: {total_current_value:,.2f} INR
• Total P&L: {total_pnl:,.2f} INR
• Total P&L %: {total_pnl_percent:.2f}%
• Number of Holdings: {len(portfolio)}

📊 TOP HOLDINGS:
"""
        
        # Sort by current value and show top 5
        sorted_portfolio = sorted(portfolio, key=lambda x: x['last_price'] * x['quantity'], reverse=True)
        
        for i, holding in enumerate(sorted_portfolio[:5]):
            current_value = holding['last_price'] * holding['quantity']
            pnl = (holding['last_price'] - holding['average_price']) * holding['quantity']
            pnl_percent = ((holding['last_price'] - holding['average_price']) / holding['average_price'] * 100) if holding['average_price'] > 0 else 0
            
            output += f"""
• {holding['tradingsymbol']} ({holding['instrument_token']}):
  - Quantity: {holding['quantity']:,}
  - Avg Price: {holding['average_price']:.2f} INR
  - Current Price: {holding['last_price']:.2f} INR
  - Current Value: {current_value:,.2f} INR
  - P&L: {pnl:,.2f} INR ({pnl_percent:.2f}%)
"""
        
        return output
        
    except Exception as e:
        return f"Error fetching portfolio data: {str(e)}"

if __name__ == "__main__":
    # Test the tools
    print("🧪 Testing Zerodha Kite Connect Tools")
    print("=" * 50)
    
    # Test live data
    print("📊 Testing Live Stock Data:")
    result = get_zerodha_stock_data.func("NSE:RELIANCE")
    print(result)
    
    print("\n📈 Testing Historical Data:")
    result = get_zerodha_historical_data.func("NSE:RELIANCE")
    print(result)
    
    print("\n💰 Testing Portfolio Data:")
    result = get_zerodha_portfolio_info.func()
    print(result)
