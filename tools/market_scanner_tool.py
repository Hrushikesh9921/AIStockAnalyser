"""
Market Scanner Tool for CrewAI
Uses dynamic market scanning based on risk levels
"""

import os
from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool("Indian Market Scanner Tool")
def get_top_traded_stocks(limit: int = 5):
    """
    Get top traded stocks using dynamic market scanner based on risk level.
    
    Parameters:
        limit (int): Number of top stocks to analyze (default: 5)
    
    Returns:
        str: List of dynamically found trading opportunities based on risk level
    """
    # Use dynamic market scanner instead of prelisted stocks
    from tools.dynamic_market_scanner import get_dynamic_trading_stocks
    return get_dynamic_trading_stocks.func(limit)

@tool("Bank Nifty Derivatives Scanner Tool")
def get_banknifty_derivatives(limit: int = 5):
    """
    Get Bank Nifty derivatives for F&O trading.
    
    Parameters:
        limit (int): Number of derivatives to analyze (default: 5)
    
    Returns:
        str: List of Bank Nifty derivatives with trading opportunities
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
        
        # Get NFO instruments for Bank Nifty
        try:
            instruments = kite.instruments("NFO")
        except Exception as e:
            return f"Error fetching NFO instruments: {str(e)}"
        
        # Filter for Bank Nifty futures
        banknifty_futures = []
        for inst in instruments:
            if (inst['instrument_type'] == 'FUT' and 
                'BANKNIFTY' in inst['name'].upper()):
                banknifty_futures.append(inst)
        
        if not banknifty_futures:
            return """
=== BANK NIFTY DERIVATIVES SCANNER: NO FUTURES FOUND ===
❌ NO BANK NIFTY FUTURES FOUND

🔍 POSSIBLE REASONS:
• Market is closed (try during 9:15 AM - 3:30 PM IST)
• No Bank Nifty futures available
• API connectivity issues
• Invalid or expired API credentials

💡 RECOMMENDED ACTIONS:
• Check if market is open (9:15 AM - 3:30 PM IST)
• Verify Zerodha API credentials
• Try again during market hours

🚫 ANALYSIS TERMINATED: No Bank Nifty futures found
"""
        
        # Get quotes for Bank Nifty futures
        instrument_tokens = [str(inst['instrument_token']) for inst in banknifty_futures[:limit]]
        
        try:
            quotes = kite.quote(instrument_tokens)
        except Exception as e:
            return f"Error fetching Bank Nifty quotes: {str(e)}"
        
        # Format output
        output = f"""
=== BANK NIFTY DERIVATIVES SCANNER: TOP {limit} FUTURES ===
📊 FILTERS APPLIED: Bank Nifty Futures Only | Limited to Top {limit}

📊 BANK NIFTY FUTURES OVERVIEW:
• Total Futures Found: {len(banknifty_futures)}
• Top Opportunities: {len(instrument_tokens)}
• Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 TOP BANK NIFTY FUTURES:
"""
        
        for i, inst in enumerate(banknifty_futures[:limit], 1):
            token = str(inst['instrument_token'])
            if token in quotes:
                quote = quotes[token]
                current_price = quote.get('last_price', 0)
                volume = quote.get('volume', 0)
                
                output += f"""
{i}. {inst['tradingsymbol']} - {inst['name']}
   • Current Price: ₹{current_price:.2f}
   • Volume: {volume:,}
   • Expiry: {inst.get('expiry', 'N/A')}
   • Lot Size: {inst.get('lot_size', 'N/A')}
"""
        
        output += f"""
💡 BANK NIFTY TRADING INSIGHTS:
• Bank Nifty futures for monthly expiry
• High leverage opportunities
• Sector-specific trading
• F&O segment focus

🎯 RECOMMENDED FOCUS:
• Top 3 Bank Nifty futures for aggressive trading
• Monthly expiry focus
• High leverage opportunities
• Sector rotation strategies

⚠️ RISK CONSIDERATIONS:
• High leverage = Higher risk
• Time decay for futures
• Sector-specific risks
• Use proper position sizing and stop losses
"""
        
        return output
        
    except Exception as e:
        return f"Error in get_banknifty_derivatives: {str(e)}"