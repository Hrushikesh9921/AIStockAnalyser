"""
Technical Analysis Tool for CrewAI
Provides realistic technical analysis based on current market data
"""

import os
from datetime import datetime, timedelta
from crewai.tools import tool
from dotenv import load_dotenv
from kiteconnect import KiteConnect
import pandas as pd

load_dotenv()

def _initialize_kite():
    api_key = os.getenv("ZERODHA_API_KEY")
    access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
    if not api_key or not access_token:
        raise ValueError("ZERODHA_API_KEY or ZERODHA_ACCESS_TOKEN not found in environment variables.")
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    return kite

@tool("Technical Analysis Tool")
def get_technical_analysis(symbol: str, current_price: float):
    """
    💡 Performs realistic technical analysis based on current market data.
    
    Parameters:
        symbol (str): Stock symbol (e.g., "RELIANCE", "TCS")
        current_price (float): Current market price of the stock
    
    Returns:
        str: Realistic technical analysis with proper entry/exit points
    """
    try:
        kite = _initialize_kite()
        
        # Get historical data for technical analysis
        from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")
        
        # Convert symbol to proper format
        if ":" not in symbol:
            symbol = f"NSE:{symbol}"
        
        # Get instruments to find numeric token
        instruments = kite.instruments("NSE")
        numeric_token = None
        for inst in instruments:
            if inst['tradingsymbol'] == symbol.split(":")[1]:
                numeric_token = inst['instrument_token']
                break
        
        if not numeric_token:
            return f"Error: Could not find instrument token for {symbol}"
        
        # Get historical data
        historical_data = kite.historical_data(
            instrument_token=numeric_token,
            from_date=from_date,
            to_date=to_date,
            interval="day"
        )
        
        if not historical_data:
            return f"No historical data found for {symbol}"
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(historical_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Calculate technical indicators
        df['sma_5'] = df['close'].rolling(window=5).mean()
        df['sma_10'] = df['close'].rolling(window=10).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['ema_12'] = df['close'].ewm(span=12).mean()
        df['ema_26'] = df['close'].ewm(span=26).mean()
        
        # Calculate MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Calculate Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        # Get latest values
        latest = df.iloc[-1]
        prev_close = df.iloc[-2]['close'] if len(df) > 1 else current_price
        
        # Calculate realistic support and resistance
        recent_high = df['high'].tail(20).max()
        recent_low = df['low'].tail(20).min()
        recent_range = recent_high - recent_low
        
        # Realistic intraday targets (0.5-2% of current price)
        intraday_target_up = current_price * 1.015  # 1.5% up
        intraday_target_down = current_price * 0.985  # 1.5% down
        
        # Realistic swing targets (2-5% of current price)
        swing_target_up = current_price * 1.035  # 3.5% up
        swing_target_down = current_price * 0.965  # 3.5% down
        
        # Realistic stop losses (0.5-1.5% of current price)
        stop_loss_up = current_price * 0.992  # 0.8% down
        stop_loss_down = current_price * 1.008  # 0.8% up
        
        # Calculate realistic entry points (more realistic for actual trading)
        entry_buy = current_price * 0.995  # 0.5% below current price
        entry_sell = current_price * 1.005  # 0.5% above current price
        
        # Market sentiment analysis - PRIORITIZE ACTUAL PRICE MOVEMENT
        price_change = current_price - prev_close
        price_change_percent = (price_change / prev_close) * 100
        
        # Primary signal based on ACTUAL price movement (most important)
        if price_change_percent > 0.5:  # Stock is up more than 0.5%
            primary_signal = "BUY"
            confidence = min(80, 60 + abs(price_change_percent) * 10)
        elif price_change_percent < -0.5:  # Stock is down more than 0.5%
            primary_signal = "SELL"
            confidence = min(80, 60 + abs(price_change_percent) * 10)
        else:  # Stock is relatively flat (-0.5% to +0.5%)
            primary_signal = "HOLD"
            confidence = 50
        
        # Technical signals (secondary to actual price movement)
        bullish_signals = 0
        bearish_signals = 0
        
        if current_price > latest['sma_20']:
            bullish_signals += 1
        else:
            bearish_signals += 1
            
        if latest['rsi'] > 50:
            bullish_signals += 1
        else:
            bearish_signals += 1
            
        if current_price > latest['bb_middle']:
            bullish_signals += 1
        else:
            bearish_signals += 1
            
        if latest['macd'] > latest['macd_signal']:
            bullish_signals += 1
        else:
            bearish_signals += 1
        
        # Determine overall sentiment and strategy - PRIORITIZE ACTUAL PRICE MOVEMENT
        if primary_signal == "BUY":
            sentiment = "BULLISH"
            primary_strategy = "BUY"
        elif primary_signal == "SELL":
            sentiment = "BEARISH"
            primary_strategy = "SELL"
        else:  # HOLD or neutral
            # Use technical indicators as secondary
            if bullish_signals > bearish_signals:
                sentiment = "BULLISH"
                primary_strategy = "BUY"
            elif bearish_signals > bullish_signals:
                sentiment = "BEARISH"
                primary_strategy = "SELL"
            else:
                sentiment = "NEUTRAL"
                primary_strategy = "HOLD"
        
        # Ensure signal matches the actual trading strategy
        # If target is above entry, it's a BUY signal
        # If target is below entry, it's a SELL signal
        if primary_strategy == "BUY":
            # For BUY: entry should be below current, target above entry
            entry_price = entry_buy
            target_price = intraday_target_up
            stop_price = stop_loss_up
        else:
            # For SELL: entry should be above current, target below entry
            entry_price = entry_sell
            target_price = intraday_target_down
            stop_price = stop_loss_down
        
        # Calculate probability based on technical strength
        total_signals = bullish_signals + bearish_signals
        confidence = max(bullish_signals, bearish_signals) / total_signals * 100 if total_signals > 0 else 50
        
        output = f"""
=== REALISTIC TECHNICAL ANALYSIS: {symbol.split(':')[1]} ===

📊 CURRENT MARKET DATA:
• Current Price: ₹{current_price:.2f}
• Previous Close: ₹{prev_close:.2f}
• Daily Change: ₹{price_change:.2f} ({price_change_percent:.2f}%)
• 20-Day SMA: ₹{latest['sma_20']:.2f}
• RSI (14): {latest['rsi']:.1f}
• MACD: {latest['macd']:.2f}
• Bollinger Middle: ₹{latest['bb_middle']:.2f}

🎯 REALISTIC TRADING LEVELS:
• Support Level: ₹{recent_low:.2f}
• Resistance Level: ₹{recent_high:.2f}
• Recent Range: ₹{recent_range:.2f} ({recent_range/current_price*100:.1f}%)

📈 REALISTIC INTRADAY STRATEGY:
• Entry (Buy): ₹{entry_buy:.2f} (0.2% below current)
• Target (Buy): ₹{intraday_target_up:.2f} (+1.5%)
• Stop Loss (Buy): ₹{stop_loss_up:.2f} (-0.8%)
• Risk-Reward: 1:1.9

📉 REALISTIC INTRADAY STRATEGY:
• Entry (Sell): ₹{entry_sell:.2f} (0.2% above current)
• Target (Sell): ₹{intraday_target_down:.2f} (-1.5%)
• Stop Loss (Sell): ₹{stop_loss_down:.2f} (+0.8%)
• Risk-Reward: 1:1.9

🎯 RECOMMENDED STRATEGY ({primary_strategy}):
• Entry: ₹{entry_price:.2f}
• Target: ₹{target_price:.2f}
• Stop Loss: ₹{stop_price:.2f}
• Signal: {primary_strategy}

📊 SWING TRADING LEVELS:
• Buy Entry: ₹{entry_buy:.2f}
• Buy Target: ₹{swing_target_up:.2f} (+3.5%)
• Buy Stop: ₹{stop_loss_up:.2f} (-0.8%)

• Sell Entry: ₹{entry_sell:.2f}
• Sell Target: ₹{swing_target_down:.2f} (-3.5%)
• Sell Stop: ₹{stop_loss_down:.2f} (+0.8%)

🔍 TECHNICAL SIGNALS:
• Bullish Signals: {bullish_signals}/4
• Bearish Signals: {bearish_signals}/4
• Overall Sentiment: {sentiment}
• Confidence Level: {confidence:.1f}%
• Primary Strategy: {primary_strategy}

⚠️ REALISTIC CONSTRAINTS:
• Maximum Intraday Move: ±2% (₹{current_price*0.02:.2f})
• Realistic Entry Range: ±0.5% of current price
• Stop Loss: 0.5-1% of current price
• Target: 1-2% for intraday, 3-5% for swing
• Success Probability: {confidence:.1f}%

💡 MARKET INSIGHTS:
• Price vs SMA20: {'Above' if current_price > latest['sma_20'] else 'Below'} (Trend: {'Bullish' if current_price > latest['sma_20'] else 'Bearish'})
• RSI Level: {'Overbought' if latest['rsi'] > 70 else 'Oversold' if latest['rsi'] < 30 else 'Neutral'}
• MACD Signal: {'Bullish' if latest['macd'] > latest['macd_signal'] else 'Bearish'}
• Bollinger Position: {'Upper Band' if current_price > latest['bb_upper'] else 'Lower Band' if current_price < latest['bb_lower'] else 'Middle Range'}
"""
        return output
        
    except Exception as e:
        return f"Error in technical analysis: {str(e)}"

@tool("Market Sentiment Analysis Tool")
def get_market_sentiment_analysis(symbol: str, current_price: float, volume: int):
    """
    💡 Analyzes market sentiment and provides realistic trading recommendations.
    
    Parameters:
        symbol (str): Stock symbol
        current_price (float): Current market price
        volume (int): Current trading volume
    
    Returns:
        str: Market sentiment analysis with realistic recommendations
    """
    try:
        kite = _initialize_kite()
        
        # Get current quote for volume analysis
        if ":" not in symbol:
            symbol = f"NSE:{symbol}"
        
        quote = kite.quote(symbol)
        if symbol not in quote:
            return f"Error: Could not fetch quote for {symbol}"
        
        quote_data = quote[symbol]
        
        # Get volume data
        current_volume = quote_data.get('volume', volume)
        avg_volume = quote_data.get('average_volume', current_volume)
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        
        # Calculate realistic market parameters
        day_high = quote_data.get('ohlc', {}).get('high', current_price)
        day_low = quote_data.get('ohlc', {}).get('low', current_price)
        daily_range = day_high - day_low
        daily_range_percent = (daily_range / current_price) * 100
        
        # Volume analysis
        if volume_ratio > 2:
            volume_sentiment = "HIGH VOLUME - Strong interest"
            volume_impact = "Positive for momentum"
        elif volume_ratio > 1.5:
            volume_sentiment = "ABOVE AVERAGE - Good participation"
            volume_impact = "Supportive for moves"
        elif volume_ratio > 0.8:
            volume_sentiment = "NORMAL - Standard participation"
            volume_impact = "Neutral impact"
        else:
            volume_sentiment = "LOW VOLUME - Weak interest"
            volume_impact = "Negative for momentum"
        
        # Price position analysis
        price_position = ((current_price - day_low) / (day_high - day_low)) * 100 if day_high != day_low else 50
        
        if price_position > 80:
            price_sentiment = "NEAR HIGH - Resistance zone"
            price_impact = "Potential selling pressure"
        elif price_position > 60:
            price_sentiment = "UPPER RANGE - Bullish bias"
            price_impact = "Positive momentum"
        elif price_position > 40:
            price_sentiment = "MID RANGE - Neutral"
            price_impact = "Balanced sentiment"
        elif price_position > 20:
            price_sentiment = "LOWER RANGE - Bearish bias"
            price_impact = "Negative momentum"
        else:
            price_sentiment = "NEAR LOW - Support zone"
            price_impact = "Potential buying opportunity"
        
        # Volatility analysis
        if daily_range_percent > 3:
            volatility_level = "HIGH VOLATILITY"
            volatility_impact = "Wide price swings expected"
        elif daily_range_percent > 2:
            volatility_level = "MODERATE VOLATILITY"
            volatility_impact = "Normal price movements"
        else:
            volatility_level = "LOW VOLATILITY"
            volatility_impact = "Limited price movements"
        
        # Realistic trading recommendations - PRIORITIZE ACTUAL PRICE MOVEMENT
        price_change = current_price - prev_close
        price_change_percent = (price_change / prev_close) * 100 if prev_close > 0 else 0
        
        if price_change_percent > 0.5:  # Stock is up more than 0.5%
            recommendation = "BUY"
            confidence = min(85, 70 + abs(price_change_percent) * 10)
            reasoning = f"Positive momentum: +{price_change_percent:.2f}% - Follow the trend"
        elif price_change_percent < -0.5:  # Stock is down more than 0.5%
            recommendation = "SELL"
            confidence = min(85, 70 + abs(price_change_percent) * 10)
            reasoning = f"Negative momentum: {price_change_percent:.2f}% - Follow the trend"
        else:  # Stock is relatively flat
            # Use volume and position as secondary factors
            if volume_ratio > 1.5 and price_position > 60:
                recommendation = "BUY"
                confidence = 65
                reasoning = "High volume + Upper price range = Bullish momentum"
            elif volume_ratio > 1.5 and price_position < 40:
                recommendation = "SELL"
                confidence = 65
                reasoning = "High volume + Lower price range = Bearish momentum"
            else:
                recommendation = "HOLD"
                confidence = 50
                reasoning = "Mixed signals - Wait for clearer direction"
        
        # Realistic entry/exit points based on signal
        if recommendation == "BUY":
            entry_price = current_price * 0.995  # 0.5% below current
            target_price = current_price * 1.015  # 1.5% up
            stop_price = current_price * 0.990  # 1.0% down
        else:
            entry_price = current_price * 1.005  # 0.5% above current
            target_price = current_price * 0.985  # 1.5% down
            stop_price = current_price * 1.010  # 1.0% up
        
        output = f"""
=== MARKET SENTIMENT ANALYSIS: {symbol.split(':')[1]} ===

📊 VOLUME ANALYSIS:
• Current Volume: {current_volume:,}
• Average Volume: {avg_volume:,}
• Volume Ratio: {volume_ratio:.2f}x
• Volume Sentiment: {volume_sentiment}
• Volume Impact: {volume_impact}

📈 PRICE POSITION ANALYSIS:
• Day High: ₹{day_high:.2f}
• Day Low: ₹{day_low:.2f}
• Current Price: ₹{current_price:.2f}
• Price Position: {price_position:.1f}% (0%=Low, 100%=High)
• Price Sentiment: {price_sentiment}
• Price Impact: {price_impact}

📊 VOLATILITY ANALYSIS:
• Daily Range: ₹{daily_range:.2f} ({daily_range_percent:.2f}%)
• Volatility Level: {volatility_level}
• Volatility Impact: {volatility_impact}

🎯 REALISTIC TRADING RECOMMENDATION:
• Recommendation: {recommendation}
• Confidence: {confidence:.1f}%
• Reasoning: {reasoning}

📋 REALISTIC ENTRY/EXIT POINTS:
• Buy Entry: ₹{current_price * 0.999:.2f} (0.1% below current)
• Buy Target: ₹{current_price * 1.012:.2f} (+1.2%)
• Buy Stop: ₹{current_price * 0.995:.2f} (-0.5%)
• Risk-Reward: 1:2.4

• Sell Entry: ₹{current_price * 1.001:.2f} (0.1% above current)
• Sell Target: ₹{current_price * 0.988:.2f} (-1.2%)
• Sell Stop: ₹{current_price * 1.005:.2f} (+0.5%)
• Risk-Reward: 1:2.4

🎯 RECOMMENDED STRATEGY ({recommendation}):
• Entry: ₹{entry_price:.2f}
• Target: ₹{target_price:.2f}
• Stop Loss: ₹{stop_price:.2f}
• Signal: {recommendation}

⚠️ REALISTIC CONSTRAINTS:
• Maximum Expected Move: ±{daily_range_percent:.1f}%
• Entry Tolerance: ±0.2% of current price
• Stop Loss: 0.5% of current price
• Target: 1-2% for intraday
• Success Probability: {confidence:.1f}%

💡 MARKET INSIGHTS:
• Volume confirms: {'Yes' if volume_ratio > 1.2 else 'No'}
• Price momentum: {'Bullish' if price_position > 60 else 'Bearish' if price_position < 40 else 'Neutral'}
• Volatility: {'High' if daily_range_percent > 2.5 else 'Normal'}
• Overall sentiment: {'Bullish' if recommendation == 'BUY' else 'Bearish' if recommendation == 'SELL' else 'Neutral'}
"""
        return output
        
    except Exception as e:
        return f"Error in market sentiment analysis: {str(e)}"
