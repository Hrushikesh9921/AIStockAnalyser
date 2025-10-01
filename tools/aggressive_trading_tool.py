"""
Aggressive Trading Strategies Tool for CrewAI
Provides higher-return strategies with controlled risk
"""

import os
from datetime import datetime, timedelta
from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool("Aggressive Intraday Strategy Tool")
def get_aggressive_intraday_strategy(symbol: str, current_price: float, daily_range: float, volume: int):
    """
    💡 Provides aggressive intraday trading strategies for higher returns.
    
    Parameters:
        symbol (str): Stock symbol
        current_price (float): Current stock price
        daily_range (float): Daily price range
        volume (int): Current volume
    
    Returns:
        str: Aggressive intraday trading strategy
    """
    
    try:
        # Calculate aggressive targets (higher than conservative)
        daily_range_percent = (daily_range / current_price * 100) if current_price > 0 else 0
        
        # Aggressive targets (2-3x conservative targets)
        aggressive_intraday_target = daily_range_percent * 0.4  # 40% of daily range
        aggressive_swing_target = daily_range_percent * 0.6     # 60% of daily range
        
        # Risk management (tighter stops for aggressive approach)
        stop_loss_percent = daily_range_percent * 0.15  # 15% of daily range
        
        # Position sizing (aggressive but controlled)
        risk_per_trade = 2.0  # 2% risk per trade (aggressive)
        position_size = 100000 / (stop_loss_percent / 100)  # Calculate position size
        
        # Entry strategies
        breakout_entry = current_price + (daily_range * 0.1)  # 10% above current
        pullback_entry = current_price - (daily_range * 0.1)  # 10% below current
        
        # Exit targets
        quick_profit_target = current_price + (current_price * aggressive_intraday_target / 100)
        swing_profit_target = current_price + (current_price * aggressive_swing_target / 100)
        
        # Stop losses
        tight_stop = current_price - (current_price * stop_loss_percent / 100)
        trailing_stop = current_price - (current_price * stop_loss_percent * 0.5 / 100)
        
        output = f"""
=== AGGRESSIVE INTRADAY STRATEGY: {symbol} ===

📊 MARKET ANALYSIS:
• Current Price: ₹{current_price:.2f}
• Daily Range: ₹{daily_range:.2f} ({daily_range_percent:.2f}%)
• Volume: {volume:,}
• Volatility: {'High' if daily_range_percent > 3 else 'Medium' if daily_range_percent > 2 else 'Low'}

🎯 AGGRESSIVE TARGETS:
• Intraday Target: {aggressive_intraday_target:.2f}% (vs 0.5-1.5% conservative)
• Swing Target: {aggressive_swing_target:.2f}% (vs 2-5% conservative)
• Risk per Trade: {risk_per_trade}% (vs 1% conservative)
• Position Size: ₹{position_size:,.0f}

📈 ENTRY STRATEGIES:
1. BREAKOUT STRATEGY (Momentum):
   • Entry: ₹{breakout_entry:.2f} (Breakout above resistance)
   • Target: ₹{quick_profit_target:.2f} (+{aggressive_intraday_target:.2f}%)
   • Stop Loss: ₹{tight_stop:.2f} (-{stop_loss_percent:.2f}%)
   • Risk-Reward: 1:{aggressive_intraday_target/stop_loss_percent:.1f}

2. PULLBACK STRATEGY (Mean Reversion):
   • Entry: ₹{pullback_entry:.2f} (Pullback to support)
   • Target: ₹{swing_profit_target:.2f} (+{aggressive_swing_target:.2f}%)
   • Stop Loss: ₹{tight_stop:.2f} (-{stop_loss_percent:.2f}%)
   • Risk-Reward: 1:{aggressive_swing_target/stop_loss_percent:.1f}

⚡ AGGRESSIVE TECHNIQUES:
• Scalping: Quick 0.5-1% profits with tight stops
• Momentum Trading: Ride strong moves for 2-3% gains
• Breakout Trading: Enter on volume breakouts
• News Trading: React to earnings/news announcements

⚠️ RISK MANAGEMENT:
• Tight Stop Loss: {stop_loss_percent:.2f}% (vs 1-2% conservative)
• Position Sizing: {risk_per_trade}% risk per trade
• Trailing Stops: Move stops to breakeven after 1% profit
• Time Stops: Exit if no movement in 30 minutes

💡 SUCCESS FACTORS:
• High volume confirmation
• Strong momentum indicators
• News catalyst support
• Market sentiment alignment
• Quick decision making
"""
        
        return output
        
    except Exception as e:
        return f"Error generating aggressive intraday strategy: {str(e)}"

@tool("Aggressive F&O Strategy Tool")
def get_aggressive_fno_strategy(symbol: str, current_price: float, volatility: float, days_to_expiry: int):
    """
    💡 Provides aggressive F&O trading strategies for higher returns.
    
    Parameters:
        symbol (str): Stock/Index symbol
        current_price (float): Current price
        volatility (float): Volatility percentage
        days_to_expiry (int): Days to expiry
    
    Returns:
        str: Aggressive F&O trading strategy
    """
    
    try:
        # Calculate aggressive F&O targets
        aggressive_futures_target = volatility * 0.8  # 80% of volatility
        aggressive_options_target = volatility * 1.2   # 120% of volatility (leverage)
        
        # Time decay consideration
        theta_factor = max(0.5, 1 - (days_to_expiry / 30))  # Higher decay near expiry
        
        # Position sizing for F&O
        futures_leverage = 3.0  # 3x leverage
        options_leverage = 5.0  # 5x leverage (approximate)
        
        # Risk management
        futures_stop = volatility * 0.3  # 30% of volatility
        options_stop = volatility * 0.4  # 40% of volatility
        
        output = f"""
=== AGGRESSIVE F&O STRATEGY: {symbol} ===

📊 MARKET CONDITIONS:
• Current Price: ₹{current_price:.2f}
• Volatility: {volatility:.2f}%
• Days to Expiry: {days_to_expiry}
• Theta Factor: {theta_factor:.2f}

🎯 AGGRESSIVE F&O TARGETS:
• Futures Target: {aggressive_futures_target:.2f}% (3x leverage)
• Options Target: {aggressive_options_target:.2f}% (5x+ leverage)
• Risk per Trade: 2.5% (vs 1% conservative)
• Position Size: Aggressive but controlled

📈 FUTURES STRATEGIES:
1. DIRECTIONAL FUTURES:
   • Entry: Current price ±0.5%
   • Target: ±{aggressive_futures_target:.2f}% (₹{current_price * aggressive_futures_target / 100:.2f})
   • Stop Loss: ±{futures_stop:.2f}% (₹{current_price * futures_stop / 100:.2f})
   • Leverage: {futures_leverage}x
   • Risk-Reward: 1:{aggressive_futures_target/futures_stop:.1f}

2. SPREAD STRATEGIES:
   • Bull Call Spread: Buy ATM, Sell OTM
   • Bear Put Spread: Buy ATM, Sell OTM
   • Risk: Limited to net premium
   • Reward: Spread difference

📊 OPTIONS STRATEGIES:
1. AGGRESSIVE OPTIONS:
   • Long Call/Put: High leverage, time decay risk
   • Target: {aggressive_options_target:.2f}% (₹{current_price * aggressive_options_target / 100:.2f})
   • Stop Loss: {options_stop:.2f}% (₹{current_price * options_stop / 100:.2f})
   • Theta Impact: {theta_factor:.2f}x decay rate

2. SPREAD STRATEGIES:
   • Iron Condor: Range-bound, limited risk
   • Butterfly: Low volatility, high probability
   • Straddle: Volatility expansion play

⚡ AGGRESSIVE TECHNIQUES:
• High Leverage: Use maximum available leverage
• Quick Profits: Target 2-3% moves for 6-9% returns
• Momentum Riding: Stay in winning positions longer
• News Trading: React to major announcements
• Sector Rotation: Switch between high-beta stocks

⚠️ RISK MANAGEMENT:
• Stop Loss: {futures_stop:.2f}% for futures, {options_stop:.2f}% for options
• Position Sizing: 2.5% risk per trade
• Time Management: Exit before 3 days to expiry
• Volatility Management: Reduce size in high volatility
• Correlation Risk: Avoid correlated positions

💡 SUCCESS FACTORS:
• Strong directional bias
• High volume confirmation
• News catalyst support
• Technical breakout confirmation
• Market sentiment alignment
• Quick execution and exit
"""
        
        return output
        
    except Exception as e:
        return f"Error generating aggressive F&O strategy: {str(e)}"

@tool("Bank Nifty Aggressive Strategy Tool")
def get_banknifty_aggressive_strategy(current_price: float, volatility: float, days_to_expiry: int):
    """
    💡 Provides aggressive Bank Nifty trading strategies for higher returns.
    
    Parameters:
        current_price (float): Current Bank Nifty price
        volatility (float): Volatility percentage
        days_to_expiry (int): Days to expiry
    
    Returns:
        str: Aggressive Bank Nifty trading strategy
    """
    
    try:
        # Bank Nifty specific calculations
        banknifty_volatility = volatility * 1.2  # Bank Nifty is typically 20% more volatile
        aggressive_target = banknifty_volatility * 0.7  # 70% of volatility
        aggressive_stop = banknifty_volatility * 0.25   # 25% of volatility
        
        # ATM strikes for options
        atm_strike = round(current_price / 100) * 100  # Round to nearest 100
        otm_strike = atm_strike + 200  # 200 points OTM
        itm_strike = atm_strike - 200  # 200 points ITM
        
        # Time decay factor
        theta_factor = max(0.3, 1 - (days_to_expiry / 15))  # Higher decay for Bank Nifty
        
        output = f"""
=== AGGRESSIVE BANK NIFTY STRATEGY ===

📊 BANK NIFTY ANALYSIS:
• Current Price: ₹{current_price:.2f}
• Volatility: {banknifty_volatility:.2f}% (20% higher than Nifty)
• Days to Expiry: {days_to_expiry}
• ATM Strike: ₹{atm_strike}
• Theta Factor: {theta_factor:.2f}

🎯 AGGRESSIVE TARGETS:
• Futures Target: ±{aggressive_target:.2f}% (₹{current_price * aggressive_target / 100:.2f})
• Options Target: ±{aggressive_target * 1.5:.2f}% (₹{current_price * aggressive_target * 1.5 / 100:.2f})
• Risk per Trade: 3% (vs 2% for individual stocks)
• Position Size: Higher due to index stability

📈 BANK NIFTY FUTURES:
1. DIRECTIONAL TRADING:
   • Entry: Current price ±0.3%
   • Target: ±{aggressive_target:.2f}% (₹{current_price * aggressive_target / 100:.2f})
   • Stop Loss: ±{aggressive_stop:.2f}% (₹{current_price * aggressive_stop / 100:.2f})
   • Leverage: 4x (Bank Nifty has higher margin)
   • Risk-Reward: 1:{aggressive_target/aggressive_stop:.1f}

2. SCALPING STRATEGY:
   • Target: 0.5-1% moves (₹{current_price * 0.01:.2f})
   • Stop Loss: 0.3% (₹{current_price * 0.003:.2f})
   • Time Frame: 15-30 minutes
   • Frequency: Multiple trades per day

📊 BANK NIFTY OPTIONS:
1. ATM OPTIONS (₹{atm_strike}):
   • High liquidity, moderate premium
   • Target: {aggressive_target:.2f}% (₹{current_price * aggressive_target / 100:.2f})
   • Stop Loss: {aggressive_stop:.2f}% (₹{current_price * aggressive_stop / 100:.2f})
   • Theta Impact: {theta_factor:.2f}x decay

2. OTM OPTIONS (₹{otm_strike}):
   • Lower premium, higher leverage
   • Target: {aggressive_target * 1.5:.2f}% (₹{current_price * aggressive_target * 1.5 / 100:.2f})
   • Stop Loss: {aggressive_stop * 1.5:.2f}% (₹{current_price * aggressive_stop * 1.5 / 100:.2f})
   • Higher risk-reward ratio

3. ITM OPTIONS (₹{itm_strike}):
   • Higher premium, lower leverage
   • Target: {aggressive_target * 0.8:.2f}% (₹{current_price * aggressive_target * 0.8 / 100:.2f})
   • Stop Loss: {aggressive_stop * 0.8:.2f}% (₹{current_price * aggressive_stop * 0.8 / 100:.2f})
   • More stable, lower risk

⚡ AGGRESSIVE BANK NIFTY TECHNIQUES:
• RBI Announcements: Trade around policy decisions
• Banking Results: React to major bank earnings
• Sector Rotation: Switch between private/public banks
• News Trading: React to banking sector news
• Volatility Expansion: Trade during high volatility periods

⚠️ RISK MANAGEMENT:
• Stop Loss: {aggressive_stop:.2f}% for futures, {aggressive_stop * 1.5:.2f}% for options
• Position Sizing: 3% risk per trade
• Time Management: Exit before 5 days to expiry
• Volatility Management: Reduce size in extreme volatility
• Sector Risk: Monitor banking sector health

💡 SUCCESS FACTORS:
• Strong directional bias
• High volume confirmation
• Banking sector news
• Technical breakout confirmation
• RBI policy alignment
• Quick execution and exit
"""
        
        return output
        
    except Exception as e:
        return f"Error generating aggressive Bank Nifty strategy: {str(e)}"

if __name__ == "__main__":
    # Test the tools
    print("🧪 Testing Aggressive Trading Tools")
    print("=" * 50)
    
    # Test aggressive intraday strategy
    print("📊 Testing Aggressive Intraday Strategy:")
    result = get_aggressive_intraday_strategy.func("RELIANCE", 1372.80, 21.00, 14231999)
    print(result)
    
    print("\n📈 Testing Aggressive F&O Strategy:")
    result = get_aggressive_fno_strategy.func("BANKNIFTY", 45000, 2.5, 15)
    print(result)
    
    print("\n🎯 Testing Bank Nifty Aggressive Strategy:")
    result = get_banknifty_aggressive_strategy.func(45000, 2.5, 15)
    print(result)
