"""
Test script to demonstrate Zerodha tools with environment variables.
This shows how the tools automatically use environment variables when no parameters are provided.
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

def test_zerodha_tools():
    """
    Test Zerodha tools with environment variables.
    """
    
    print("🧪 Testing Zerodha Tools with Environment Variables\n")
    
    # Check if environment variables are set
    api_key = os.getenv("ZERODHA_API_KEY")
    access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
    
    print("📋 Environment Variables Status:")
    print(f"• ZERODHA_API_KEY: {'✅ Set' if api_key else '❌ Not set'}")
    print(f"• ZERODHA_ACCESS_TOKEN: {'✅ Set' if access_token else '❌ Not set'}")
    print()
    
    if not api_key:
        print("❌ ZERODHA_API_KEY not found in environment variables")
        print("Please add to your .env file:")
        print("ZERODHA_API_KEY=your_api_key_here")
        print("ZERODHA_ACCESS_TOKEN=your_access_token_here")
        return
    
    # Test 1: Stock data (only requires API key)
    print("📊 Test 1: Real-time Stock Data")
    print("=" * 50)
    
    # This will automatically use environment variables
    result = get_zerodha_stock_data.func("NSE:RELIANCE")
    print(result)
    print()
    
    # Test 2: Historical data (requires access token)
    if access_token:
        print("📈 Test 2: Historical Data")
        print("=" * 50)
        
        from datetime import datetime, timedelta
        
        # Get data for last 7 days
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        # This will automatically use environment variables
        result = get_zerodha_historical_data.func(
            "NSE:RELIANCE", 
            start_date, 
            end_date, 
            "day"
        )
        print(result)
        print()
        
        # Test 3: Portfolio information (requires access token)
        print("💼 Test 3: Portfolio Information")
        print("=" * 50)
        
        # This will automatically use environment variables
        result = get_zerodha_portfolio_info.func()
        print(result)
    else:
        print("⚠️  ACCESS_TOKEN not found. Skipping historical data and portfolio tests.")
        print("Please add ZERODHA_ACCESS_TOKEN to your .env file for full functionality.")

def show_usage_examples():
    """
    Show different ways to use the Zerodha tools.
    """
    
    print("\n" + "=" * 60)
    print("📚 USAGE EXAMPLES")
    print("=" * 60)
    
    print("""
🔧 Method 1: Using Environment Variables (Recommended)
----------------------------------------------------
# Set in .env file:
ZERODHA_API_KEY=your_api_key_here
ZERODHA_ACCESS_TOKEN=your_access_token_here

# Use in code (automatically uses env vars):
result = get_zerodha_stock_data.func("NSE:RELIANCE")
result = get_zerodha_historical_data.func("NSE:RELIANCE", "2024-01-01", "2024-01-31", "day")
result = get_zerodha_portfolio_info.func()

🔧 Method 2: Passing Parameters Directly
---------------------------------------
# Pass credentials as parameters:
result = get_zerodha_stock_data.func("NSE:RELIANCE", "your_api_key", "your_access_token")
result = get_zerodha_historical_data.func("NSE:RELIANCE", "2024-01-01", "2024-01-31", "day", "your_api_key", "your_access_token")
result = get_zerodha_portfolio_info.func("your_api_key", "your_access_token")

🔧 Method 3: Mixed Approach
--------------------------
# Use env var for API key, pass access token:
result = get_zerodha_stock_data.func("NSE:RELIANCE", access_token="your_access_token")

🎯 CrewAI Integration
--------------------
# In your CrewAI agents, the tools will automatically use environment variables:
from tools.zerodha_kite_tool import get_zerodha_stock_data

# Add to agent tools list - no need to pass credentials
agent = Agent(
    role="Stock Analyst",
    tools=[get_zerodha_stock_data],  # Automatically uses env vars
    # ... other parameters
)
""")

if __name__ == "__main__":
    test_zerodha_tools()
    show_usage_examples()
