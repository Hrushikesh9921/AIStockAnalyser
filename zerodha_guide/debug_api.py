"""
DEBUG ZERODHA API - DETAILED ERROR ANALYSIS
==========================================

This script provides detailed debugging information for Zerodha API issues.
"""

import os
import json
from zerodha_api_complete import ZerodhaAPI

def debug_environment():
    """Debug environment variables and API setup."""
    print("🔍 DEBUGGING ZERODHA API SETUP")
    print("=" * 50)
    
    # Check environment variables
    print("\n1️⃣ Environment Variables:")
    api_key = os.getenv("ZERODHA_API_KEY")
    access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
    
    print(f"ZERODHA_API_KEY: {'✅ Set' if api_key else '❌ Not Set'}")
    print(f"ZERODHA_ACCESS_TOKEN: {'✅ Set' if access_token else '❌ Not Set'}")
    
    if api_key:
        print(f"API Key (first 10 chars): {api_key[:10]}...")
    if access_token:
        print(f"Access Token (first 10 chars): {access_token[:10]}...")
    
    # Check .env file
    print("\n2️⃣ .env File Check:")
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file exists")
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                print(f"File size: {len(content)} characters")
                # Don't print actual content for security
                if "ZERODHA_API_KEY" in content:
                    print("✅ ZERODHA_API_KEY found in .env")
                else:
                    print("❌ ZERODHA_API_KEY not found in .env")
                if "ZERODHA_ACCESS_TOKEN" in content:
                    print("✅ ZERODHA_ACCESS_TOKEN found in .env")
                else:
                    print("❌ ZERODHA_ACCESS_TOKEN not found in .env")
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
    else:
        print("❌ .env file not found")
        print("💡 Create .env file with:")
        print("ZERODHA_API_KEY=your_api_key_here")
        print("ZERODHA_ACCESS_TOKEN=your_access_token_here")
    
    return api_key, access_token

def debug_api_response():
    """Debug API response structure."""
    print("\n3️⃣ API Response Debug:")
    
    try:
        # Initialize API
        api = ZerodhaAPI()
        print("✅ API client initialized")
        
        # Try to get profile with detailed error handling
        print("\n📊 Attempting to fetch profile...")
        try:
            profile = api.get_profile()
            print("✅ Profile API call successful")
            print(f"Response type: {type(profile)}")
            print(f"Response keys: {list(profile.keys()) if isinstance(profile, dict) else 'Not a dict'}")
            
            # Check for specific fields
            if isinstance(profile, dict):
                if 'user_name' in profile:
                    print(f"✅ user_name found: {profile['user_name']}")
                else:
                    print("❌ user_name not found in response")
                    print(f"Available fields: {list(profile.keys())}")
                
                if 'error' in profile:
                    print(f"❌ API Error: {profile['error']}")
                else:
                    print("✅ No error field in response")
                    
                # Print full response for debugging
                print("\n📋 Full API Response:")
                print(json.dumps(profile, indent=2))
            else:
                print(f"❌ Unexpected response type: {type(profile)}")
                print(f"Response content: {profile}")
                
        except Exception as e:
            print(f"❌ Profile API call failed: {e}")
            print(f"Error type: {type(e).__name__}")
            
            # Try to get more details about the error
            if hasattr(e, 'response'):
                print(f"HTTP Status: {e.response.status_code if hasattr(e.response, 'status_code') else 'Unknown'}")
                try:
                    error_response = e.response.json()
                    print(f"Error Response: {json.dumps(error_response, indent=2)}")
                except:
                    print(f"Error Response (text): {e.response.text if hasattr(e.response, 'text') else 'Unknown'}")
    
    except Exception as e:
        print(f"❌ API initialization failed: {e}")
        print(f"Error type: {type(e).__name__}")

def debug_network_connectivity():
    """Debug network connectivity to Zerodha API."""
    print("\n4️⃣ Network Connectivity Test:")
    
    try:
        import requests
        
        # Test basic connectivity
        print("Testing connectivity to Zerodha API...")
        response = requests.get("https://api.kite.trade", timeout=10)
        print(f"✅ Basic connectivity: HTTP {response.status_code}")
        
        # Test with API key (without access token)
        api_key = os.getenv("ZERODHA_API_KEY")
        if api_key:
            print("Testing API key authentication...")
            headers = {
                "X-Kite-Version": "3",
                "Authorization": f"token {api_key}:dummy_token"
            }
            try:
                response = requests.get("https://api.kite.trade/user/profile", headers=headers, timeout=10)
                print(f"API Key test: HTTP {response.status_code}")
                if response.status_code == 401:
                    print("✅ API key is valid (401 expected without access token)")
                else:
                    print(f"Unexpected status: {response.status_code}")
            except Exception as e:
                print(f"❌ API key test failed: {e}")
        else:
            print("❌ Cannot test API key - not set")
            
    except Exception as e:
        print(f"❌ Network test failed: {e}")

def main():
    """Main debug function."""
    print("🚀 ZERODHA API DEBUG TOOL")
    print("=" * 50)
    
    # Debug environment
    api_key, access_token = debug_environment()
    
    # Debug API response
    if api_key and access_token:
        debug_api_response()
    else:
        print("\n⚠️ Skipping API tests - credentials not available")
    
    # Debug network connectivity
    debug_network_connectivity()
    
    print("\n" + "=" * 50)
    print("🎯 DEBUG SUMMARY:")
    print("=" * 50)
    
    if not api_key or not access_token:
        print("❌ Missing credentials - check .env file")
        print("💡 Create .env file with your Zerodha credentials")
    else:
        print("✅ Credentials found - check API response details above")
        print("💡 If API calls fail, check:")
        print("   - Access token validity")
        print("   - API key permissions")
        print("   - Network connectivity")
        print("   - Zerodha account status")

if __name__ == "__main__":
    main()
