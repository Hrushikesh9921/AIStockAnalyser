from dotenv import load_dotenv
from crew import pre_post_market_crew, live_market_crew
import sys

load_dotenv()

def run_market_scan(crew_type="pre_post", risk_level="1"):
    try:
        # Set risk level in environment for tools to use
        import os
        os.environ["TRADING_RISK_LEVEL"] = risk_level
        
        if crew_type == "pre_post":
            result = pre_post_market_crew.kickoff()
        else:
            result = live_market_crew.kickoff()
        
            # Check if result contains "NO REAL DATA AVAILABLE" or "ANALYSIS TERMINATED" or "NO OPPORTUNITIES FOUND"
            if "NO REAL DATA AVAILABLE" in str(result) or "ANALYSIS TERMINATED" in str(result) or "NO OPPORTUNITIES FOUND" in str(result):
                print("\n" + "="*60)
                print("❌ ANALYSIS TERMINATED - NO REAL DATA AVAILABLE")
                print("="*60)
                print("🔍 The analysis could not proceed due to lack of real market data.")
                print("💡 This could be due to:")
                print("   • Market is closed (try during 9:15 AM - 3:30 PM IST)")
                print("   • Zerodha API connectivity issues")
                print("   • Invalid or expired API credentials")
                print("   • No trading opportunities meeting criteria")
                print("\n🛠️ TROUBLESHOOTING STEPS:")
                print("1. Run: python test_zerodha_api.py")
                print("2. If token is expired, run: python refresh_zerodha_token.py")
                print("3. Check if market is open (9:15 AM - 3:30 PM IST)")
                print("4. Verify your .env file has correct credentials")
                print("="*60)
                sys.exit(1)
            else:
                print(result)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("💡 Please check your API credentials and try again.")
        print("🛠️ Run: python test_zerodha_api.py to check connectivity")
        sys.exit(1)

def show_menu():
    print("\n" + "="*60)
    print("🚀 CREWAI INTELLIGENT TRADING ANALYZER & EXECUTION GUIDE")
    print("="*60)
    print("📊 Primary Data Source: Zerodha Kite Connect")
    print("📈 Secondary Data Source: Yahoo Finance (Optional)")
    print("🇮🇳 Focus: Indian Market Analysis (NSE/BSE)")
    print("🎯 Derivatives: Futures & Options Trading Support")
    print("⚡ Approach: DYNAMIC RISK-BASED TRADING")
    print("📈 Bank Nifty: Monthly Expiry Focus")
    print("="*60)
    print("\n📋 SELECT ANALYSIS MODE:")
    print("1. 🌅 PRE/POST MARKET ANALYSIS")
    print("   - Perfect trades for market open")
    print("   - Single-day execution strategy")
    print("   - Based on previous day close + technical factors")
    print()
    print("2. 🔴 LIVE MARKET ANALYSIS")
    print("   - Real-time market scanning")
    print("   - Live trading opportunities")
    print("   - Current market conditions analysis")
    print()
    print("3. 🔧 TEST ZERODHA API")
    print("   - Check API connectivity")
    print("   - Verify token validity")
    print("   - Test data access")
    print()
    print("4. 🔄 REFRESH ZERODHA TOKEN")
    print("   - Generate new access token")
    print("   - Update credentials")
    print()
    print("5. ❌ EXIT")
    print("="*60)

def show_risk_menu(analysis_type="PRE/POST MARKET"):
    print(f"\n📊 {analysis_type} - SELECT RISK LEVEL:")
    print("="*50)
    print("1. 🟢 LOW RISK TRADES")
    print("   - 1-2% price movements")
    print("   - Large cap, stable stocks")
    print("   - Conservative approach")
    print("   - Lower volatility, steady gains")
    print()
    print("2. 🟡 MID RISK TRADES")
    print("   - 2-4% price movements")
    print("   - Mid cap stocks")
    print("   - Balanced risk-reward")
    print("   - Moderate volatility")
    print()
    print("3. 🔴 HIGH RISK TRADES")
    print("   - 5%+ price movements")
    print("   - Small cap, volatile stocks")
    print("   - Aggressive approach")
    print("   - High volatility, big spikes")
    print("="*50)

def run_pre_post_market():
    print("\n🌅 PRE/POST MARKET ANALYSIS MODE")
    print("="*50)
    print("📊 Analysis: Previous Day Close + Technical Factors + Market Sentiment")
    print("⚡ Strategy: Place Orders at Market Open - Execute Once - No More Trading")
    print("📋 Output: Perfect Entry Points + Targets + Stop Losses for Market Open")
    print("="*50)
    
    show_risk_menu("PRE/POST MARKET")
    try:
        risk_choice = input("\n🎯 Select risk level (1-3): ").strip()
        if risk_choice in ["1", "2", "3"]:
            run_market_scan("pre_post", risk_choice)
        else:
            print("❌ Invalid choice! Please select 1, 2, or 3.")
    except KeyboardInterrupt:
        print("\n👋 Analysis cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def run_live_market():
    print("\n🔴 LIVE MARKET ANALYSIS MODE")
    print("="*50)
    print("📊 Analysis: Real-time Market Conditions + Live Opportunities")
    print("⚡ Strategy: Live Trading Opportunities + Real-time Execution")
    print("📋 Output: Current Market Opportunities + Live Entry Points")
    print("="*50)
    
    show_risk_menu("LIVE MARKET")
    try:
        risk_choice = input("\n🎯 Select risk level (1-3): ").strip()
        if risk_choice in ["1", "2", "3"]:
            run_market_scan("live", risk_choice)
        else:
            print("❌ Invalid choice! Please select 1, 2, or 3.")
    except KeyboardInterrupt:
        print("\n👋 Analysis cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def run_api_test():
    print("\n🔧 ZERODHA API TEST MODE")
    print("="*50)
    print("📊 Testing: API Connectivity + Token Validity + Data Access")
    print("⚡ Purpose: Verify Zerodha API is working correctly")
    print("📋 Output: Detailed test results and recommendations")
    print("="*50)
    print()
    
    # Import the test function directly instead of using subprocess
    try:
        from test_zerodha_api import test_zerodha_api
        success = test_zerodha_api()
        if success:
            print("\n✅ API test completed successfully!")
        else:
            print("\n❌ API test failed!")
    except Exception as e:
        print(f"❌ Error running API test: {e}")
        print("💡 Please run the API test script:")
        print("   python test_zerodha_api.py")

def run_token_refresh():
    print("\n🔄 ZERODHA TOKEN REFRESH MODE")
    print("="*50)
    print("📊 Purpose: Generate new access token when current one expires")
    print("⚡ Process: Interactive token generation with browser login")
    print("📋 Output: Updated .env file with new access token")
    print("="*50)
    print()
    
    # Import the refresh function directly instead of using subprocess
    try:
        from refresh_zerodha_token import refresh_token
        success = refresh_token()
        if success:
            print("\n✅ Token refresh completed successfully!")
        else:
            print("\n❌ Token refresh failed!")
    except Exception as e:
        print(f"❌ Error running token refresh: {e}")
        print("💡 Please run the token refresh script:")
        print("   python refresh_zerodha_token.py")

if __name__ == "__main__":
    while True:
        show_menu()
        try:
            choice = input("\n🎯 Enter your choice (1-5): ").strip()
            
            if choice == "1":
                run_pre_post_market()
                break
            elif choice == "2":
                run_live_market()
                break
            elif choice == "3":
                run_api_test()
                input("\nPress Enter to continue...")
            elif choice == "4":
                run_token_refresh()
                input("\nPress Enter to continue...")
            elif choice == "5":
                print("\n👋 Thank you for using CrewAI Trading Analyzer!")
                print("📈 Happy Trading! 🚀")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice! Please enter 1, 2, 3, 4, or 5.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using CrewAI Trading Analyzer!")
            print("📈 Happy Trading! 🚀")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")
