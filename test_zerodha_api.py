"""
Zerodha API Test Script
Tests API connectivity and data access
"""

import os
from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()

def test_zerodha_api():
    """
    Test Zerodha API connectivity and data access
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get credentials from environment
        api_key = os.getenv("ZERODHA_API_KEY")
        access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
        
        if not api_key:
            print("❌ Error: ZERODHA_API_KEY not found in .env file")
            return False
        
        if not access_token:
            print("❌ Error: ZERODHA_ACCESS_TOKEN not found in .env file")
            return False
        
        print("🔍 ZERODHA API CONNECTIVITY TEST")
        print("="*50)
        print(f"📋 API Key: {'✅ Found' if api_key else '❌ Missing'}")
        print(f"📋 Access Token: {'✅ Found' if access_token else '❌ Missing'}")
        print()
        
        # Initialize KiteConnect
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)
        
        print("🔗 Testing API Connection...")
        
        # Test user profile
        try:
            profile = kite.profile()
            print(f"✅ User Profile: {profile['user_name']} ({profile['user_id']})")
            print(f"✅ Email: {profile['email']}")
            print(f"✅ Broker: {profile['broker']}")
        except Exception as e:
            print(f"❌ Profile Error: {str(e)}")
            return False
        
        print()
        print("📊 Testing Instruments API...")
        
        # Test instruments
        try:
            instruments = kite.instruments("NSE")
            print(f"✅ NSE Instruments: {len(instruments)} instruments found")
        except Exception as e:
            print(f"❌ Instruments Error: {str(e)}")
            return False
        
        print()
        print("💰 Testing Quotes API...")
        
        # Test quotes
        try:
            quotes = kite.quote("NSE:RELIANCE")
            if "NSE:RELIANCE" in quotes:
                quote = quotes["NSE:RELIANCE"]
                price = quote.get('last_price', 0)
                volume = quote.get('volume', 0)
                print(f"✅ RELIANCE Quote: ₹{price}")
                print(f"✅ Volume: {volume:,}")
            else:
                print("❌ No quote data received")
                return False
        except Exception as e:
            print(f"❌ Quotes Error: {str(e)}")
            return False
        
        print()
        print("✅ All API tests passed successfully!")
        print("🎯 Your Zerodha API is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error in API test: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 ZERODHA API TEST - STANDALONE")
    print("="*50)
    success = test_zerodha_api()
    if success:
        print("\n✅ API test completed successfully!")
    else:
        print("\n❌ API test failed!")
