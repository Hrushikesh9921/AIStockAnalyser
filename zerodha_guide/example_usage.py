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
        if profile.get('status') == 'success' and 'data' in profile:
            profile_data = profile['data']
            print(f"User: {profile_data['user_name']}")
            print(f"Email: {profile_data['email']}")
            print(f"Broker: {profile_data['broker']}")
            print(f"User ID: {profile_data['user_id']}")
            print(f"Exchanges: {', '.join(profile_data['exchanges'])}")
        else:
            print(f"❌ Profile fetch failed: {profile}")
        
        # Get margins
        print("\n4️⃣ Getting Margins...")
        margins = api.get_margins()
        if margins.get('status') == 'success' and 'data' in margins:
            margins_data = margins['data']
            if 'equity' in margins_data:
                equity = margins_data['equity']
                print(f"Equity Net: ₹{equity['net']:,.2f}")
                print(f"Available Cash: ₹{equity['available']['cash']:,.2f}")
            else:
                print("No equity margins found")
        else:
            print(f"❌ Margins fetch failed: {margins}")
        
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
        
        if isinstance(quotes, dict) and quotes.get('status') == 'success' and 'data' in quotes:
            quotes_data = quotes['data']
            for symbol, data in quotes_data.items():
                if isinstance(data, dict) and "error" not in data:
                    change = data.get('net_change', 0)
                    last_price = data.get('last_price', 0)
                    change_pct = (change / last_price) * 100 if last_price > 0 else 0
                    print(f"{symbol:<15} ₹{last_price:<9.2f} {change:+.2f}     {change_pct:+.2f}%")
                else:
                    print(f"{symbol:<15} Error: {data}")
        else:
            print("❌ Quotes API returned unexpected format")
        
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
            
            if historical and isinstance(historical, list) and len(historical) > 0:
                print(f"📈 Historical Data Points: {len(historical)}")
                latest = historical[-1]
                if isinstance(latest, dict):
                    print(f"Latest Close: ₹{latest.get('close', 0):.2f}")
                    print(f"Date: {latest.get('date', 'N/A')}")
                    
                    # Calculate 30-day return
                    if len(historical) > 1:
                        first_candle = historical[0]
                        if isinstance(first_candle, dict):
                            first_price = first_candle.get('close', 0)
                            last_price = latest.get('close', 0)
                            if first_price > 0:
                                return_pct = ((last_price - first_price) / first_price) * 100
                                print(f"30-Day Return: {return_pct:+.2f}%")
            else:
                print("📈 No historical data available (market may be closed)")
        except Exception as e:
            print(f"⚠️ Historical data error: {e}")
            print("💡 This is normal when market is closed or for new instruments")
        
        # Get portfolio
        print("\n7️⃣ Getting Portfolio...")
        try:
            portfolio = api.get_portfolio()
            if portfolio and portfolio.get('status') == 'success' and 'data' in portfolio:
                portfolio_data = portfolio['data']
                if isinstance(portfolio_data, list):
                    print(f"📊 Portfolio Holdings: {len(portfolio_data)}")
                    print("\nTop Holdings:")
                    print("-" * 50)
                    print(f"{'Symbol':<12} {'Qty':<8} {'Avg Price':<12} {'Current':<12} {'P&L':<12}")
                    print("-" * 50)
                    
                    # Show top 5 holdings safely
                    top_holdings = portfolio_data[:5] if len(portfolio_data) >= 5 else portfolio_data
                    for holding in top_holdings:
                        if isinstance(holding, dict):
                            pnl = holding.get('pnl', 0)
                            print(f"{holding.get('tradingsymbol', 'N/A'):<12} {holding.get('quantity', 0):<8} "
                                  f"₹{holding.get('average_price', 0):<11.2f} ₹{holding.get('last_price', 0):<11.2f} "
                                  f"₹{pnl:<11.2f}")
                else:
                    print("📊 No holdings found in portfolio")
            else:
                print("📊 No holdings found in portfolio")
        except Exception as e:
            print(f"⚠️ Portfolio error: {e}")
        
        # Get positions
        print("\n8️⃣ Getting Positions...")
        try:
            positions = api.get_positions()
            if isinstance(positions, dict) and positions.get('status') == 'success' and 'data' in positions:
                positions_data = positions['data']
                day_positions = positions_data.get('day', [])
                net_positions = positions_data.get('net', [])
                
                print(f"Day Positions: {len(day_positions)}")
                print(f"Net Positions: {len(net_positions)}")
                
                if day_positions and isinstance(day_positions, list):
                    print("\nDay Positions:")
                    # Show first 3 positions safely
                    top_positions = day_positions[:3] if len(day_positions) >= 3 else day_positions
                    for pos in top_positions:
                        if isinstance(pos, dict):
                            print(f"  {pos.get('tradingsymbol', 'N/A')}: {pos.get('quantity', 0)} @ ₹{pos.get('average_price', 0):.2f}")
            else:
                print("❌ Positions API returned unexpected format")
        except Exception as e:
            print(f"⚠️ Positions error: {e}")
        
        # Get orders
        print("\n9️⃣ Getting Orders...")
        try:
            orders = api.get_orders()
            if isinstance(orders, dict) and orders.get('status') == 'success' and 'data' in orders:
                orders_data = orders['data']
                if isinstance(orders_data, list):
                    print(f"📋 Total Orders: {len(orders_data)}")
                    
                    if orders_data:
                        # Show recent orders safely
                        recent_orders = orders_data[:3] if len(orders_data) >= 3 else orders_data
                        print("\nRecent Orders:")
                        print("-" * 80)
                        print(f"{'Order ID':<15} {'Symbol':<12} {'Type':<6} {'Qty':<6} {'Status':<12} {'Price':<10}")
                        print("-" * 80)
                        
                        for order in recent_orders:
                            if isinstance(order, dict):
                                print(f"{order.get('order_id', 'N/A'):<15} {order.get('tradingsymbol', 'N/A'):<12} "
                                      f"{order.get('transaction_type', 'N/A'):<6} {order.get('quantity', 0):<6} "
                                      f"{order.get('status', 'N/A'):<12} ₹{order.get('average_price', 0):<9.2f}")
                    else:
                        print("📋 No orders found")
                else:
                    print("📋 No orders found")
            else:
                print("❌ Orders API returned unexpected format")
        except Exception as e:
            print(f"⚠️ Orders error: {e}")
        
        # Get GTT orders
        print("\n🔟 Getting GTT Orders...")
        try:
            gtt_orders = api.get_gtt()
            if isinstance(gtt_orders, dict) and gtt_orders.get('status') == 'success' and 'data' in gtt_orders:
                gtt_data = gtt_orders['data']
                if isinstance(gtt_data, list):
                    print(f"⏰ GTT Orders: {len(gtt_data)}")
                    
                    if gtt_data:
                        # Show first 2 GTT orders safely
                        top_gtt = gtt_data[:2] if len(gtt_data) >= 2 else gtt_data
                        for gtt in top_gtt:
                            if isinstance(gtt, dict):
                                condition = gtt.get('condition', {})
                                print(f"  GTT {gtt.get('id', 'N/A')}: {condition.get('tradingsymbol', 'N/A')} - {gtt.get('status', 'N/A')}")
                    else:
                        print("⏰ No GTT orders found")
                else:
                    print("⏰ No GTT orders found")
            else:
                print("❌ GTT orders API returned unexpected format")
        except Exception as e:
            print(f"⚠️ GTT orders error: {e}")
        
        # Get mutual fund holdings
        print("\n1️⃣1️⃣ Getting Mutual Fund Holdings...")
        try:
            mf_holdings = api.get_mf_holdings()
            if isinstance(mf_holdings, dict) and mf_holdings.get('status') == 'success' and 'data' in mf_holdings:
                mf_data = mf_holdings['data']
                if isinstance(mf_data, list):
                    print(f"💼 MF Holdings: {len(mf_data)}")
                    
                    if mf_data:
                        # Show first 3 MF holdings safely
                        top_mf = mf_data[:3] if len(mf_data) >= 3 else mf_data
                        for mf in top_mf:
                            if isinstance(mf, dict):
                                print(f"  {mf.get('tradingsymbol', 'N/A')}: {mf.get('quantity', 0)} units @ ₹{mf.get('average_price', 0):.2f}")
                    else:
                        print("💼 No MF holdings found")
                else:
                    print("💼 No MF holdings found")
            else:
                print("❌ MF holdings API returned unexpected format")
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
