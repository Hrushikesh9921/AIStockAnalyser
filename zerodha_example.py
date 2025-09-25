"""
Zerodha Kite Connect API Integration Example
This file demonstrates how to use the Zerodha tools for financial data and trading.
"""

import os
from dotenv import load_dotenv
from tools.zerodha_kite_tool import (
    get_zerodha_stock_data,
    get_zerodha_historical_data,
    get_zerodha_portfolio_info
)

# Load environment variables
load_dotenv()

def main():
    """
    Example usage of Zerodha Kite Connect tools.
    """
    
    # Get API credentials from environment variables
    API_KEY = os.getenv("ZERODHA_API_KEY")
    ACCESS_TOKEN = os.getenv("ZERODHA_ACCESS_TOKEN")
    
    if not API_KEY:
        print("❌ ZERODHA_API_KEY not found in environment variables")
        print("Please add your Zerodha API key to .env file:")
        print("ZERODHA_API_KEY=your_api_key_here")
        return
    
    print("🚀 Zerodha Kite Connect API Integration Example\n")
    
    # Example 1: Get real-time stock data
    print("=" * 60)
    print("📊 EXAMPLE 1: Real-time Stock Data")
    print("=" * 60)
    
    # Popular Indian stocks
    stocks = [
        "NSE:RELIANCE",    # Reliance Industries
        "NSE:TCS",         # Tata Consultancy Services
        "NSE:HDFCBANK",    # HDFC Bank
        "NSE:INFY",        # Infosys
        "BSE:500325"       # Reliance Industries (BSE)
    ]
    
    for stock in stocks:
        print(f"\n🔍 Analyzing: {stock}")
        result = get_zerodha_stock_data(stock, API_KEY, ACCESS_TOKEN)
        print(result)
        print("-" * 40)
    
    # Example 2: Get historical data (requires access token)
    if ACCESS_TOKEN:
        print("\n" + "=" * 60)
        print("📈 EXAMPLE 2: Historical Data Analysis")
        print("=" * 60)
        
        from datetime import datetime, timedelta
        
        # Get data for last 30 days
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        historical_stocks = ["NSE:RELIANCE", "NSE:TCS"]
        
        for stock in historical_stocks:
            print(f"\n📊 Historical Analysis: {stock}")
            result = get_zerodha_historical_data(
                stock, 
                API_KEY, 
                ACCESS_TOKEN, 
                start_date, 
                end_date, 
                "day"
            )
            print(result)
            print("-" * 40)
        
        # Example 3: Get portfolio information
        print("\n" + "=" * 60)
        print("💼 EXAMPLE 3: Portfolio Information")
        print("=" * 60)
        
        portfolio_info = get_zerodha_portfolio_info(API_KEY, ACCESS_TOKEN)
        print(portfolio_info)
        
    else:
        print("\n⚠️  ACCESS_TOKEN not found. Historical data and portfolio features require authentication.")
        print("Please add your Zerodha access token to .env file:")
        print("ZERODHA_ACCESS_TOKEN=your_access_token_here")
        print("\nTo get an access token, you need to complete the Zerodha authentication flow.")
        print("Visit: https://kite.trade/docs/connect/v3/ for authentication details.")

def setup_instructions():
    """
    Print setup instructions for Zerodha Kite Connect.
    """
    print("""
🔧 ZERODHA KITE CONNECT SETUP INSTRUCTIONS

1. 📝 Create Zerodha Developer Account:
   - Visit: https://kite.trade/docs/connect/v3/
   - Sign up for a developer account
   - Create a new app to get API credentials

2. 🔑 Get API Credentials:
   - Note down your api_key and api_secret
   - Set up redirect URL for authentication
   - Complete the authentication flow to get access_token

3. ⚙️ Environment Setup:
   - Add to your .env file:
     ZERODHA_API_KEY=your_api_key_here
     ZERODHA_ACCESS_TOKEN=your_access_token_here

4. 📊 Available Features:
   ✅ Real-time stock quotes (requires API key only)
   ✅ Historical candle data (requires access token)
   ✅ Portfolio information (requires access token)
   ✅ Technical analysis and trends
   ✅ Volume and volatility analysis

5. 🎯 Supported Instruments:
   - NSE stocks: NSE:RELIANCE, NSE:TCS, NSE:HDFCBANK
   - BSE stocks: BSE:500325, BSE:532540
   - F&O instruments: NFO:NIFTY24JANFUT, NFO:BANKNIFTY24JANFUT
   - Commodities: MCX:GOLD24JANFUT, MCX:SILVER24JANFUT

6. 📈 Data Intervals:
   - minute, 3minute, 5minute, 15minute, 30minute, 60minute, day

7. 🔒 Security Notes:
   - Never expose your api_secret in client-side code
   - Use access_token for authenticated requests
   - Implement proper error handling for API calls
   - Respect rate limits and API quotas

For more details, visit: https://kite.trade/docs/connect/v3/
""")

if __name__ == "__main__":
    setup_instructions()
    print("\n" + "=" * 60)
    print("🚀 RUNNING EXAMPLES")
    print("=" * 60)
    main()
