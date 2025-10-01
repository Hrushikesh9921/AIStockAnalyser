"""
DEBUG API RESPONSES - CHECK ACTUAL DATA STRUCTURES
=================================================

This script checks the actual response structures from Zerodha API
to understand why some sections are showing "unexpected format".
"""

import os
import json
from zerodha_api_complete import ZerodhaAPI

def debug_api_responses():
    """Debug actual API response structures."""
    print("🔍 DEBUGGING ZERODHA API RESPONSE STRUCTURES")
    print("=" * 60)
    
    try:
        api = ZerodhaAPI()
        
        # Test quotes
        print("\n1️⃣ QUOTES API RESPONSE:")
        print("-" * 30)
        quotes = api.get_quotes(["NSE:RELIANCE"])
        print(f"Type: {type(quotes)}")
        print(f"Content: {quotes}")
        
        # Test portfolio
        print("\n2️⃣ PORTFOLIO API RESPONSE:")
        print("-" * 30)
        portfolio = api.get_portfolio()
        print(f"Type: {type(portfolio)}")
        print(f"Content: {portfolio}")
        
        # Test positions
        print("\n3️⃣ POSITIONS API RESPONSE:")
        print("-" * 30)
        positions = api.get_positions()
        print(f"Type: {type(positions)}")
        print(f"Content: {positions}")
        
        # Test orders
        print("\n4️⃣ ORDERS API RESPONSE:")
        print("-" * 30)
        orders = api.get_orders()
        print(f"Type: {type(orders)}")
        print(f"Content: {orders}")
        
        # Test GTT
        print("\n5️⃣ GTT API RESPONSE:")
        print("-" * 30)
        gtt = api.get_gtt()
        print(f"Type: {type(gtt)}")
        print(f"Content: {gtt}")
        
        # Test MF holdings
        print("\n6️⃣ MF HOLDINGS API RESPONSE:")
        print("-" * 30)
        mf_holdings = api.get_mf_holdings()
        print(f"Type: {type(mf_holdings)}")
        print(f"Content: {mf_holdings}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_api_responses()
