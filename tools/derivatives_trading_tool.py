"""
Derivatives Trading Tools for CrewAI
Supports Futures and Options trading analysis for Indian markets
"""

import os
import requests
from datetime import datetime, timedelta
from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()

def get_derivatives_instruments(kite, exchange="NSE", instrument_type="FUT"):
    """
    Get derivatives instruments (Futures/Options) for a given exchange.
    
    Parameters:
        kite: KiteConnect instance
        exchange (str): Exchange (NSE, BSE)
        instrument_type (str): FUT for futures, OPT for options
    
    Returns:
        list: List of derivatives instruments
    """
    try:
        instruments = kite.instruments(exchange)
        derivatives = []
        
        for inst in instruments:
            if inst['instrument_type'] == instrument_type:
                derivatives.append(inst)
        
        return derivatives
    except Exception as e:
        print(f"Error getting derivatives instruments: {e}")
        return []

def get_option_chain_data(kite, symbol, expiry_date=None):
    """
    Get option chain data for a given symbol.
    
    Parameters:
        kite: KiteConnect instance
        symbol (str): Underlying symbol (e.g., "RELIANCE")
        expiry_date (str): Expiry date in YYYY-MM-DD format
    
    Returns:
        dict: Option chain data
    """
    try:
        # Get all NSE instruments
        instruments = kite.instruments("NSE")
        
        # Filter for options of the given symbol
        options = []
        for inst in instruments:
            if (inst['instrument_type'] == 'OPT' and 
                inst['name'] == symbol and
                (expiry_date is None or inst['expiry'].strftime('%Y-%m-%d') == expiry_date)):
                options.append(inst)
        
        # Group by strike price
        option_chain = {}
        for opt in options:
            strike = opt['strike']
            if strike not in option_chain:
                option_chain[strike] = {'CE': None, 'PE': None}
            
            if opt['instrument_token']:
                # Get current price
                quote = kite.quote(opt['instrument_token'])
                if str(opt['instrument_token']) in quote:
                    data = quote[str(opt['instrument_token'])]
                    opt_data = {
                        'instrument_token': opt['instrument_token'],
                        'tradingsymbol': opt['tradingsymbol'],
                        'last_price': data.get('last_price', 0),
                        'volume': data.get('volume', 0),
                        'oi': data.get('oi', 0),
                        'bid': data.get('depth', {}).get('buy', [{}])[0].get('price', 0),
                        'ask': data.get('depth', {}).get('sell', [{}])[0].get('price', 0),
                        'expiry': opt['expiry'].strftime('%Y-%m-%d')
                    }
                    
                    if opt['instrument_type'] == 'OPT':
                        if opt['name'] == symbol:  # This is a call option
                            option_chain[strike]['CE'] = opt_data
                        else:  # This is a put option
                            option_chain[strike]['PE'] = opt_data
        
        return option_chain
    except Exception as e:
        print(f"Error getting option chain: {e}")
        return {}

@tool("Zerodha Futures Data Tool")
def get_zerodha_futures_data(symbol: str, expiry_date: str = None):
    """
    💡 Retrieves futures data for a given symbol using Zerodha Kite Connect API.
    
    Parameters:
        symbol (str): Underlying symbol (e.g., "RELIANCE", "NIFTY")
        expiry_date (str): Expiry date in YYYY-MM-DD format (optional, gets nearest expiry if not provided)
    
    Returns:
        str: Comprehensive futures data analysis
    """
    
    try:
        # Get credentials from environment variables
        api_key = os.getenv("ZERODHA_API_KEY")
        access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
        
        if not api_key:
            return "Error: ZERODHA_API_KEY not found. Please set ZERODHA_API_KEY environment variable."
        
        if not access_token:
            return "Error: ZERODHA_ACCESS_TOKEN not found. Please set ZERODHA_ACCESS_TOKEN environment variable."
        
        # Initialize Zerodha API client
        from kiteconnect import KiteConnect
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)
        
        # Get futures instruments
        futures_instruments = get_derivatives_instruments(kite, "NSE", "FUT")
        
        # Filter for the given symbol
        symbol_futures = []
        for fut in futures_instruments:
            if fut['name'] == symbol:
                symbol_futures.append(fut)
        
        if not symbol_futures:
            return f"Error: No futures found for symbol {symbol}"
        
        # Sort by expiry date
        symbol_futures.sort(key=lambda x: x['expiry'])
        
        # Get the nearest expiry or specified expiry
        target_future = None
        if expiry_date:
            for fut in symbol_futures:
                if fut['expiry'].strftime('%Y-%m-%d') == expiry_date:
                    target_future = fut
                    break
        else:
            target_future = symbol_futures[0]  # Nearest expiry
        
        if not target_future:
            return f"Error: No futures found for {symbol} with expiry {expiry_date}"
        
        # Get current quote
        quote_data = kite.quote(target_future['instrument_token'])
        
        if str(target_future['instrument_token']) not in quote_data:
            return f"Error: Could not fetch quote for {target_future['tradingsymbol']}"
        
        data = quote_data[str(target_future['instrument_token'])]
        
        # Calculate days to expiry
        days_to_expiry = (target_future['expiry'] - datetime.now().date()).days
        
        # Format the output
        output = f"""
=== ZERODHA FUTURES DATA: {symbol} ===

📊 BASIC INFORMATION:
• Symbol: {target_future['name']}
• Trading Symbol: {target_future['tradingsymbol']}
• Expiry Date: {target_future['expiry'].strftime('%Y-%m-%d')}
• Days to Expiry: {days_to_expiry}
• Lot Size: {target_future['lot_size']}

📈 PRICE INFORMATION:
• Current Price: {data.get('last_price', 0):.2f} INR
• Open Price: {data.get('ohlc', {}).get('open', 0):.2f} INR
• Day High: {data.get('ohlc', {}).get('high', 0):.2f} INR
• Day Low: {data.get('ohlc', {}).get('low', 0):.2f} INR
• Previous Close: {data.get('ohlc', {}).get('close', 0):.2f} INR
• Net Change: {data.get('net_change', 0):.2f} INR
• Change %: {data.get('net_change', 0) / data.get('ohlc', {}).get('close', 1) * 100:.2f}%

📊 VOLUME & OI:
• Current Volume: {data.get('volume', 0):,}
• Open Interest: {data.get('oi', 0):,}
• Average Volume: {data.get('average_volume', 0):,}

💰 TRADING INFORMATION:
• Bid: {data.get('depth', {}).get('buy', [{}])[0].get('price', 0):.2f} INR
• Ask: {data.get('depth', {}).get('sell', [{}])[0].get('price', 0):.2f} INR
• Last Trade Time: {data.get('last_trade_time', 'N/A')}

📊 FUTURES ANALYSIS:
• Time Decay: {days_to_expiry} days remaining
• Liquidity: {'High' if data.get('volume', 0) > 1000000 else 'Medium' if data.get('volume', 0) > 100000 else 'Low'}
• Volatility: Based on daily range and volume
• Risk Level: {'High' if days_to_expiry < 7 else 'Medium' if days_to_expiry < 30 else 'Low'}

💡 TRADING INSIGHTS:
• Futures leverage provides amplified exposure to underlying
• Time decay accelerates as expiry approaches
• Consider rollover if holding near expiry
• Monitor open interest for trend confirmation

"""
        
        return output
        
    except Exception as e:
        return f"Error processing futures data: {str(e)}"

@tool("Zerodha Options Chain Tool")
def get_zerodha_options_chain(symbol: str, expiry_date: str = None):
    """
    💡 Retrieves options chain data for a given symbol using Zerodha Kite Connect API.
    
    Parameters:
        symbol (str): Underlying symbol (e.g., "RELIANCE", "NIFTY")
        expiry_date (str): Expiry date in YYYY-MM-DD format (optional, gets nearest expiry if not provided)
    
    Returns:
        str: Comprehensive options chain analysis
    """
    
    try:
        # Get credentials from environment variables
        api_key = os.getenv("ZERODHA_API_KEY")
        access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
        
        if not api_key:
            return "Error: ZERODHA_API_KEY not found. Please set ZERODHA_API_KEY environment variable."
        
        if not access_token:
            return "Error: ZERODHA_ACCESS_TOKEN not found. Please set ZERODHA_ACCESS_TOKEN environment variable."
        
        # Initialize Zerodha API client
        from kiteconnect import KiteConnect
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)
        
        # Get current underlying price - need to use NSE: format
        underlying_symbol = f"NSE:{symbol}" if ":" not in symbol else symbol
        underlying_quote = kite.quote(underlying_symbol)
        if underlying_symbol not in underlying_quote:
            return f"Error: Could not fetch underlying price for {symbol}"
        
        underlying_price = underlying_quote[underlying_symbol]['last_price']
        
        # Get options chain
        option_chain = get_option_chain_data(kite, symbol, expiry_date)
        
        if not option_chain:
            return f"Error: No options chain found for {symbol}"
        
        # Find ATM strikes (closest to current price)
        strikes = sorted(option_chain.keys())
        atm_strikes = []
        for strike in strikes:
            if abs(strike - underlying_price) <= 50:  # Within 50 points
                atm_strikes.append(strike)
        
        # Format the output
        output = f"""
=== ZERODHA OPTIONS CHAIN: {symbol} ===

📊 UNDERLYING INFORMATION:
• Current Price: {underlying_price:.2f} INR
• Expiry Date: {expiry_date or 'Nearest Expiry'}

📈 ATM OPTIONS (Near Current Price):
"""
        
        # Show ATM options
        for strike in atm_strikes[:5]:  # Show top 5 ATM strikes
            ce_data = option_chain[strike]['CE']
            pe_data = option_chain[strike]['PE']
            
            output += f"""
• Strike: {strike} INR
  - CE: {ce_data['last_price']:.2f} INR (Vol: {ce_data['volume']:,}, OI: {ce_data['oi']:,})
  - PE: {pe_data['last_price']:.2f} INR (Vol: {pe_data['volume']:,}, OI: {pe_data['oi']:,})
"""
        
        # Calculate key metrics
        total_ce_oi = sum(opt['CE']['oi'] for opt in option_chain.values() if opt['CE'])
        total_pe_oi = sum(opt['PE']['oi'] for opt in option_chain.values() if opt['PE'])
        put_call_ratio = total_pe_oi / total_ce_oi if total_ce_oi > 0 else 0
        
        output += f"""
📊 OPTIONS METRICS:
• Total CE Open Interest: {total_ce_oi:,}
• Total PE Open Interest: {total_pe_oi:,}
• Put-Call Ratio: {put_call_ratio:.2f}
• Market Sentiment: {'Bearish' if put_call_ratio > 1.2 else 'Bullish' if put_call_ratio < 0.8 else 'Neutral'}

💡 OPTIONS TRADING INSIGHTS:
• High PCR (>1.2): Bearish sentiment, potential support
• Low PCR (<0.8): Bullish sentiment, potential resistance
• ATM options have highest liquidity
• Monitor volume and OI for trend confirmation
• Consider time decay (theta) in strategy selection

🎯 STRATEGY SUGGESTIONS:
• Long Call: Bullish outlook, limited risk
• Long Put: Bearish outlook, limited risk
• Straddle: High volatility expected
• Strangle: Moderate volatility expected
• Iron Condor: Range-bound market
• Butterfly: Low volatility expected

"""
        
        return output
        
    except Exception as e:
        return f"Error processing options chain: {str(e)}"

@tool("Zerodha Derivatives Strategy Tool")
def get_zerodha_derivatives_strategy(symbol: str, strategy_type: str = "auto", market_outlook: str = "neutral"):
    """
    💡 Provides derivatives trading strategies based on market conditions.
    
    Parameters:
        symbol (str): Underlying symbol (e.g., "RELIANCE", "NIFTY")
        strategy_type (str): Strategy type (auto, bullish, bearish, neutral, volatile)
        market_outlook (str): Market outlook (bullish, bearish, neutral, volatile)
    
    Returns:
        str: Comprehensive derivatives trading strategy
    """
    
    try:
        # Get credentials from environment variables
        api_key = os.getenv("ZERODHA_API_KEY")
        access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
        
        if not api_key:
            return "Error: ZERODHA_API_KEY not found. Please set ZERODHA_API_KEY environment variable."
        
        if not access_token:
            return "Error: ZERODHA_ACCESS_TOKEN not found. Please set ZERODHA_ACCESS_TOKEN environment variable."
        
        # Initialize Zerodha API client
        from kiteconnect import KiteConnect
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)
        
        # Get current underlying price - need to use NSE: format
        underlying_symbol = f"NSE:{symbol}" if ":" not in symbol else symbol
        underlying_quote = kite.quote(underlying_symbol)
        if underlying_symbol not in underlying_quote:
            return f"Error: Could not fetch underlying price for {symbol}"
        
        underlying_price = underlying_quote[underlying_symbol]['last_price']
        
        # Get options chain for strategy analysis
        option_chain = get_option_chain_data(kite, symbol)
        
        if not option_chain:
            return f"Error: No options chain found for {symbol}"
        
        # Calculate key metrics
        total_ce_oi = sum(opt['CE']['oi'] for opt in option_chain.values() if opt['CE'])
        total_pe_oi = sum(opt['PE']['oi'] for opt in option_chain.values() if opt['PE'])
        put_call_ratio = total_pe_oi / total_ce_oi if total_ce_oi > 0 else 0
        
        # Determine market sentiment
        if put_call_ratio > 1.2:
            sentiment = "Bearish"
        elif put_call_ratio < 0.8:
            sentiment = "Bullish"
        else:
            sentiment = "Neutral"
        
        # Generate strategy recommendations
        strategies = []
        
        if strategy_type == "auto" or strategy_type == "bullish":
            if sentiment == "Bullish" or market_outlook == "bullish":
                strategies.append({
                    "name": "Long Call",
                    "description": "Buy ATM or ITM call options",
                    "risk": "Limited to premium paid",
                    "reward": "Unlimited upside",
                    "suitability": "Strong bullish conviction"
                })
                
                strategies.append({
                    "name": "Bull Call Spread",
                    "description": "Buy lower strike call, sell higher strike call",
                    "risk": "Limited",
                    "reward": "Limited but higher probability",
                    "suitability": "Moderate bullish outlook"
                })
        
        if strategy_type == "auto" or strategy_type == "bearish":
            if sentiment == "Bearish" or market_outlook == "bearish":
                strategies.append({
                    "name": "Long Put",
                    "description": "Buy ATM or ITM put options",
                    "risk": "Limited to premium paid",
                    "reward": "Unlimited downside",
                    "suitability": "Strong bearish conviction"
                })
                
                strategies.append({
                    "name": "Bear Put Spread",
                    "description": "Buy higher strike put, sell lower strike put",
                    "risk": "Limited",
                    "reward": "Limited but higher probability",
                    "suitability": "Moderate bearish outlook"
                })
        
        if strategy_type == "auto" or strategy_type == "volatile":
            if market_outlook == "volatile":
                strategies.append({
                    "name": "Long Straddle",
                    "description": "Buy ATM call and put with same strike",
                    "risk": "Limited to total premium",
                    "reward": "Unlimited in both directions",
                    "suitability": "High volatility expected"
                })
                
                strategies.append({
                    "name": "Long Strangle",
                    "description": "Buy OTM call and put",
                    "risk": "Limited to total premium",
                    "reward": "Unlimited in both directions",
                    "suitability": "Moderate volatility expected"
                })
        
        if strategy_type == "auto" or strategy_type == "neutral":
            if sentiment == "Neutral" or market_outlook == "neutral":
                strategies.append({
                    "name": "Iron Condor",
                    "description": "Sell OTM call spread and put spread",
                    "risk": "Limited",
                    "reward": "Limited but high probability",
                    "suitability": "Range-bound market"
                })
                
                strategies.append({
                    "name": "Butterfly Spread",
                    "description": "Buy ITM, sell 2 ATM, buy OTM options",
                    "risk": "Limited",
                    "reward": "Limited but high probability",
                    "suitability": "Low volatility expected"
                })
        
        # Format the output
        output = f"""
=== DERIVATIVES TRADING STRATEGY: {symbol} ===

📊 MARKET ANALYSIS:
• Current Price: {underlying_price:.2f} INR
• Market Sentiment: {sentiment}
• Put-Call Ratio: {put_call_ratio:.2f}
• Strategy Type: {strategy_type.title()}
• Market Outlook: {market_outlook.title()}

🎯 RECOMMENDED STRATEGIES:
"""
        
        for i, strategy in enumerate(strategies, 1):
            output += f"""
{i}. {strategy['name']}
   • Description: {strategy['description']}
   • Risk: {strategy['risk']}
   • Reward: {strategy['reward']}
   • Suitability: {strategy['suitability']}
"""
        
        output += f"""
⚠️ RISK MANAGEMENT:
• Always use stop losses
• Never risk more than 2-3% of capital per trade
• Consider position sizing based on volatility
• Monitor time decay (theta) for options
• Have an exit plan before entering

💡 DERIVATIVES TRADING TIPS:
• Options provide leverage but with time decay
• Futures provide direct exposure with margin
• Consider implied volatility for options pricing
• Monitor open interest for trend confirmation
• Use technical analysis for entry/exit timing

"""
        
        return output
        
    except Exception as e:
        return f"Error generating derivatives strategy: {str(e)}"

if __name__ == "__main__":
    # Test the tools
    print("🧪 Testing Derivatives Trading Tools")
    print("=" * 50)
    
    # Test futures data
    print("📊 Testing Futures Data:")
    result = get_zerodha_futures_data.func("RELIANCE")
    print(result)
    
    print("\n📈 Testing Options Chain:")
    result = get_zerodha_options_chain.func("RELIANCE")
    print(result)
    
    print("\n🎯 Testing Strategy Tool:")
    result = get_zerodha_derivatives_strategy.func("RELIANCE", "auto", "bullish")
    print(result)
