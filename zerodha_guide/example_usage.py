"""
ZERODHA API - EXAMPLE USAGE
==========================

This file demonstrates how to use the Zerodha API complete implementation
with practical examples for common trading operations.

Author: AI Assistant
Date: 2025
"""

from zerodha_api_complete import ZerodhaAPI
import os
from datetime import datetime, timedelta

def main():
    """
    Demonstrate various Zerodha API operations with practical examples.
    """
    
    print("🚀 ZERODHA API - PRACTICAL EXAMPLES")
    print("=" * 50)
    
    try:
        # Initialize API
        print("\n1️⃣ Initializing API...")
        api = ZerodhaAPI()
        print("✅ API initialized successfully")
        
        # Check market status
        print("\n2️⃣ Checking Market Status...")
        status = api.get_market_status()
        print(f"Market Open: {status['is_open']}")
        print(f"Current Time: {status['current_time']}")
        print(f"Market Hours: {status['market_hours']}")
        
        # Get user profile
        print("\n3️⃣ Getting User Profile...")
        profile = api.get_profile()
        print(f"User: {profile['user_name']}")
        print(f"Email: {profile['email']}")
        print(f"Broker: {profile['broker']}")
        
        # Get margins
        print("\n4️⃣ Getting Margins...")
        margins = api.get_margins()
        if 'equity' in margins:
            equity = margins['equity']
            print(f"Equity Net: ₹{equity['net']:,.2f}")
            print(f"Available Cash: ₹{equity['available']['cash']:,.2f}")
        
        # Get live quotes for popular stocks
        print("\n5️⃣ Getting Live Quotes...")
        popular_stocks = [
            "NSE:RELIANCE",
            "NSE:TCS", 
            "NSE:INFY",
            "NSE:HDFC",
            "NSE:ICICIBANK"
        ]
        
        quotes = api.get_quotes(popular_stocks)
        print("\n📊 LIVE MARKET DATA:")
        print("-" * 60)
        print(f"{'Stock':<15} {'Price':<10} {'Change':<10} {'Change%':<10}")
        print("-" * 60)
        
        for symbol, data in quotes.items():
            if "error" not in data:
                change = data.get('net_change', 0)
                change_pct = (change / data.get('last_price', 1)) * 100 if data.get('last_price', 0) > 0 else 0
                print(f"{symbol:<15} ₹{data['last_price']:<9.2f} {change:+.2f}     {change_pct:+.2f}%")
        
        # Get historical data for RELIANCE
        print("\n6️⃣ Getting Historical Data for RELIANCE...")
        try:
            # Get RELIANCE token
            reliance_token = api.get_instrument_token("NSE", "RELIANCE")
            print(f"RELIANCE Token: {reliance_token}")
            
            # Get last 30 days data
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            
            historical = api.get_historical_data(
                instrument_token=reliance_token,
                from_date=start_date,
                to_date=end_date,
                interval="day"
            )
            
            if historical:
                print(f"📈 Historical Data Points: {len(historical)}")
                latest = historical[-1]
                print(f"Latest Close: ₹{latest['close']:.2f}")
                print(f"Date: {latest['date']}")
                
                # Calculate 30-day return
                if len(historical) > 1:
                    first_price = historical[0]['close']
                    last_price = historical[-1]['close']
                    return_pct = ((last_price - first_price) / first_price) * 100
                    print(f"30-Day Return: {return_pct:+.2f}%")
        except Exception as e:
            print(f"⚠️ Historical data error: {e}")
        
        # Get portfolio
        print("\n7️⃣ Getting Portfolio...")
        try:
            portfolio = api.get_portfolio()
            if portfolio:
                print(f"📊 Portfolio Holdings: {len(portfolio)}")
                print("\nTop Holdings:")
                print("-" * 50)
                print(f"{'Symbol':<12} {'Qty':<8} {'Avg Price':<12} {'Current':<12} {'P&L':<12}")
                print("-" * 50)
                
                for holding in portfolio[:5]:  # Show top 5
                    pnl = holding.get('pnl', 0)
                    print(f"{holding['tradingsymbol']:<12} {holding['quantity']:<8} "
                          f"₹{holding['average_price']:<11.2f} ₹{holding['last_price']:<11.2f} "
                          f"₹{pnl:<11.2f}")
            else:
                print("📊 No holdings found in portfolio")
        except Exception as e:
            print(f"⚠️ Portfolio error: {e}")
        
        # Get positions
        print("\n8️⃣ Getting Positions...")
        try:
            positions = api.get_positions()
            day_positions = positions.get('day', [])
            net_positions = positions.get('net', [])
            
            print(f"Day Positions: {len(day_positions)}")
            print(f"Net Positions: {len(net_positions)}")
            
            if day_positions:
                print("\nDay Positions:")
                for pos in day_positions[:3]:  # Show first 3
                    print(f"  {pos['tradingsymbol']}: {pos['quantity']} @ ₹{pos['average_price']:.2f}")
        except Exception as e:
            print(f"⚠️ Positions error: {e}")
        
        # Get orders
        print("\n9️⃣ Getting Orders...")
        try:
            orders = api.get_orders()
            print(f"📋 Total Orders: {len(orders)}")
            
            if orders:
                # Show recent orders
                recent_orders = orders[:3]  # Show first 3
                print("\nRecent Orders:")
                print("-" * 80)
                print(f"{'Order ID':<15} {'Symbol':<12} {'Type':<6} {'Qty':<6} {'Status':<12} {'Price':<10}")
                print("-" * 80)
                
                for order in recent_orders:
                    print(f"{order['order_id']:<15} {order['tradingsymbol']:<12} "
                          f"{order['transaction_type']:<6} {order['quantity']:<6} "
                          f"{order['status']:<12} ₹{order['average_price']:<9.2f}")
        except Exception as e:
            print(f"⚠️ Orders error: {e}")
        
        # Get GTT orders
        print("\n🔟 Getting GTT Orders...")
        try:
            gtt_orders = api.get_gtt()
            print(f"⏰ GTT Orders: {len(gtt_orders)}")
            
            if gtt_orders:
                for gtt in gtt_orders[:2]:  # Show first 2
                    print(f"  GTT {gtt['id']}: {gtt['condition']['tradingsymbol']} - {gtt['status']}")
        except Exception as e:
            print(f"⚠️ GTT orders error: {e}")
        
        # Get mutual fund holdings
        print("\n1️⃣1️⃣ Getting Mutual Fund Holdings...")
        try:
            mf_holdings = api.get_mf_holdings()
            print(f"💼 MF Holdings: {len(mf_holdings)}")
            
            if mf_holdings:
                for mf in mf_holdings[:3]:  # Show first 3
                    print(f"  {mf['tradingsymbol']}: {mf['quantity']} units @ ₹{mf['average_price']:.2f}")
        except Exception as e:
            print(f"⚠️ MF holdings error: {e}")
        
        print("\n✅ All examples completed successfully!")
        print("\n💡 TIP: This is a read-only demonstration.")
        print("   For actual trading, ensure you have proper permissions and market is open.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🛠️ TROUBLESHOOTING:")
        print("1. Check your API credentials in .env file")
        print("2. Ensure ZERODHA_API_KEY and ZERODHA_ACCESS_TOKEN are set")
        print("3. Verify your access token is valid and not expired")
        print("4. Check your internet connection")


def demonstrate_order_placement():
    """
    Demonstrate order placement (READ-ONLY - No actual orders placed)
    """
    print("\n" + "="*60)
    print("📋 ORDER PLACEMENT DEMONSTRATION (READ-ONLY)")
    print("="*60)
    
    try:
        api = ZerodhaAPI()
        
        print("\n🔍 This demonstrates how to place orders (NOT ACTUALLY PLACED):")
        print("\n1. Market Order Example:")
        print("   api.place_order(")
        print("       variety='regular',")
        print("       exchange='NSE',")
        print("       tradingsymbol='RELIANCE',")
        print("       transaction_type='BUY',")
        print("       quantity=1,")
        print("       product='CNC',")
        print("       order_type='MARKET'")
        print("   )")
        
        print("\n2. Limit Order Example:")
        print("   api.place_order(")
        print("       variety='regular',")
        print("       exchange='NSE',")
        print("       tradingsymbol='RELIANCE',")
        print("       transaction_type='BUY',")
        print("       quantity=1,")
        print("       product='CNC',")
        print("       order_type='LIMIT',")
        print("       price=2450.00")
        print("   )")
        
        print("\n3. Stop Loss Order Example:")
        print("   api.place_order(")
        print("       variety='regular',")
        print("       exchange='NSE',")
        print("       tradingsymbol='RELIANCE',")
        print("       transaction_type='SELL',")
        print("       quantity=1,")
        print("       product='MIS',")
        print("       order_type='SL',")
        print("       trigger_price=2400.00,")
        print("       price=2395.00")
        print("   )")
        
        print("\n⚠️  WARNING: These are examples only!")
        print("   Do not uncomment and run these in live trading without proper testing.")
        
    except Exception as e:
        print(f"❌ Error in order demonstration: {e}")


if __name__ == "__main__":
    # Run main examples
    main()
    
    # Demonstrate order placement (read-only)
    demonstrate_order_placement()
    
    print("\n" + "="*60)
    print("🎯 NEXT STEPS:")
    print("="*60)
    print("1. Review the ZERODHA_API_COMPLETE_GUIDE.md for detailed documentation")
    print("2. Use zerodha_api_complete.py for your trading applications")
    print("3. Always test with small amounts first")
    print("4. Implement proper error handling and risk management")
    print("5. Follow Zerodha's terms and conditions")
    print("\n📚 Happy Trading! 🚀")
