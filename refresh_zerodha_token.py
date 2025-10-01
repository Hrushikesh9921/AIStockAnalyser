"""
Zerodha Token Refresh Script
Generates new access token when current one expires
"""

import os
import webbrowser
import requests
from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()

def refresh_token():
    """
    Refresh Zerodha access token using interactive browser login
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get credentials from environment
        api_key = os.getenv("ZERODHA_API_KEY")
        api_secret = os.getenv("ZERODHA_API_SECRET")
        
        if not api_key or not api_secret:
            print("❌ Error: ZERODHA_API_KEY or ZERODHA_API_SECRET not found in .env file")
            return False
        
        print("🔑 Zerodha Token Refresh Process")
        print("="*50)
        print("📋 Step 1: Opening browser for login...")
        
        # Generate login URL
        kite = KiteConnect(api_key=api_key)
        login_url = kite.login_url()
        
        # Open browser
        webbrowser.open(login_url)
        
        print("🌐 Browser opened. Please login to Zerodha and authorize the app.")
        print("📋 Step 2: After login, you'll get a request token in the URL.")
        print("📋 Step 3: Copy the request token and paste it below.")
        print()
        
        # Get request token from user
        request_token = input("🔑 Enter the request token from URL: ").strip()
        
        if not request_token:
            print("❌ No request token provided!")
            return False
        
        print("📋 Step 4: Generating access token...")
        
        # Generate access token
        try:
            data = kite.generate_session(request_token, api_secret=api_secret)
            access_token = data["access_token"]
            
            print("✅ Access token generated successfully!")
            
            # Update .env file
            env_file = ".env"
            if os.path.exists(env_file):
                # Read current .env file
                with open(env_file, 'r') as f:
                    lines = f.readlines()
                
                # Update or add access token
                updated = False
                for i, line in enumerate(lines):
                    if line.startswith("ZERODHA_ACCESS_TOKEN="):
                        lines[i] = f"ZERODHA_ACCESS_TOKEN={access_token}\n"
                        updated = True
                        break
                
                if not updated:
                    lines.append(f"ZERODHA_ACCESS_TOKEN={access_token}\n")
                
                # Write back to .env file
                with open(env_file, 'w') as f:
                    f.writelines(lines)
                
                print("✅ .env file updated with new access token!")
                print("🔄 You can now use the application with the new token.")
                return True
            else:
                print("❌ .env file not found!")
                return False
                
        except Exception as e:
            print(f"❌ Error generating access token: {str(e)}")
            print("💡 Possible reasons:")
            print("   • Request token expired (get a fresh one)")
            print("   • Invalid API secret")
            print("   • Network connectivity issues")
            return False
            
    except Exception as e:
        print(f"❌ Error in token refresh process: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔄 ZERODHA TOKEN REFRESH - STANDALONE")
    print("="*50)
    success = refresh_token()
    if success:
        print("\n✅ Token refresh completed successfully!")
    else:
        print("\n❌ Token refresh failed!")
