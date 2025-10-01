"""
Dynamic Market Scanner Tool
Fetches stocks based on actual market data and risk levels
"""

from crewai.tools import tool
import os
from datetime import datetime
from kiteconnect import KiteConnect

@tool("Dynamic Market Scanner Tool")
def get_dynamic_trading_stocks(limit: int = 5):
    """
    Dynamically scan the market for trading opportunities based on risk level.
    
    Parameters:
        limit (int): Number of stocks to analyze (default: 5)
    
    Returns:
        str: List of dynamically found trading opportunities based on risk level
    """
    
    try:
        # Get credentials from environment variables
        api_key = os.getenv("ZERODHA_API_KEY")
        access_token = os.getenv("ZERODHA_ACCESS_TOKEN")
        risk_level = os.getenv("TRADING_RISK_LEVEL", "1")
        
        if not api_key:
            return "Error: ZERODHA_API_KEY not found. Please set ZERODHA_API_KEY environment variable."
        
        if not access_token:
            return "Error: ZERODHA_ACCESS_TOKEN not found. Please set ZERODHA_ACCESS_TOKEN environment variable."
        
        # Initialize Zerodha API client
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)
        
        # Get NSE instruments
        try:
            instruments = kite.instruments("NSE")
        except Exception as e:
            return f"Error fetching NSE instruments: {str(e)}"
        
        # Filter for equity stocks based on risk level
        equity_stocks = []
        
        # Use popular stocks when market is closed or for better performance
        popular_stocks_by_risk = {
            "1": ["RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "SBIN", "BAJFINANCE", "WIPRO", "LT", "MARUTI"],  # Large Cap
            "2": ["ADANIPORTS", "ADANIENT", "BAJAJFINSV", "JSWSTEEL", "TATASTEEL", "HINDALCO", "UPL", "HEROMOTOCO", "EICHERMOT", "BOSCHLTD"],  # Mid Cap
            "3": ["IRCTC", "ZOMATO", "PAYTM", "NYKA", "DELTACORP", "SUZLON", "JPASSOCIAT", "YESBANK", "IDFC", "IDFCFIRSTB"]  # Small Cap
        }
        
        # Get popular stocks for the risk level
        risk_stocks = popular_stocks_by_risk.get(risk_level, popular_stocks_by_risk["1"])
        
        for inst in instruments:
            if (inst['instrument_type'] == 'EQ' and 
                inst['segment'] == 'NSE' and 
                inst['tradingsymbol'] in risk_stocks):
                equity_stocks.append(inst)
        
        # Get quotes for equity stocks (limit to 50 for performance and rate limits)
        instrument_tokens = [str(inst['instrument_token']) for inst in equity_stocks[:50]]
        
        if not instrument_tokens:
            return "Error: No equity stocks found"
        
        # Get quotes in smaller batches to avoid rate limits
        quotes = {}
        batch_size = 10
        for i in range(0, len(instrument_tokens), batch_size):
            batch = instrument_tokens[i:i+batch_size]
            try:
                batch_quotes = kite.quote(batch)
                quotes.update(batch_quotes)
            except Exception as e:
                print(f"Warning: Error fetching quotes for batch {i//batch_size + 1}: {str(e)}")
                continue
        
        # Analyze stocks based on risk level
        analyzed_stocks = []
        for i, inst in enumerate(equity_stocks[:500]):
            token = str(inst['instrument_token'])
            if token in quotes:
                quote = quotes[token]
                
                # Calculate key metrics
                current_price = quote.get('last_price', 0)
                volume = quote.get('volume', 0)
                ohlc = quote.get('ohlc', {})
                day_high = ohlc.get('high', 0)
                day_low = ohlc.get('low', 0)
                day_open = ohlc.get('open', 0)
                
                # Skip stocks with invalid data
                if current_price <= 0:
                    continue
                
                # Calculate metrics
                daily_range = day_high - day_low if day_high and day_low else 0
                daily_range_percent = (daily_range / current_price * 100) if current_price > 0 else 0
                price_change = current_price - day_open if day_open else 0
                price_change_percent = (price_change / day_open * 100) if day_open else 0
                
                # Volume analysis
                avg_volume = quote.get('average_volume', 0)
                volume_ratio = volume / avg_volume if avg_volume > 0 else 0
                
                # Liquidity score
                liquidity_score = volume * current_price
                
                # Volatility score - use actual price change percentage, not daily range
                volatility_score = abs(price_change_percent)
                
                # Momentum score - use price change percentage
                momentum_score = abs(price_change_percent)
                
                # Risk-based filtering
                risk_category = get_risk_category(risk_level, current_price, volatility_score, volume_ratio)
                
                if risk_category:
                    # Opportunity score based on risk level
                    if risk_level == "1":  # Low risk
                        opportunity_score = (volume_ratio * 0.3 + volatility_score * 0.2 + momentum_score * 0.1 + liquidity_score/1000000 * 0.4)
                    elif risk_level == "2":  # Mid risk
                        opportunity_score = (volume_ratio * 0.4 + volatility_score * 0.3 + momentum_score * 0.2 + liquidity_score/1000000 * 0.1)
                    else:  # High risk
                        opportunity_score = (volume_ratio * 0.2 + volatility_score * 0.4 + momentum_score * 0.4)
                    
                    analyzed_stocks.append({
                        'symbol': inst['tradingsymbol'],
                        'name': inst['name'],
                        'token': token,
                        'current_price': current_price,
                        'volume': volume,
                        'daily_range': daily_range,
                        'daily_range_percent': daily_range_percent,
                        'price_change_percent': price_change_percent,
                        'volume_ratio': volume_ratio,
                        'liquidity_score': liquidity_score,
                        'volatility_score': volatility_score,
                        'momentum_score': momentum_score,
                        'opportunity_score': opportunity_score,
                        'risk_category': risk_category
                    })
        
        # Sort by opportunity score
        analyzed_stocks.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        # Take top stocks
        top_stocks = analyzed_stocks[:limit]
        
        if not top_stocks:
            return f"""
=== DYNAMIC MARKET SCANNER: NO OPPORTUNITIES FOUND ===
📊 RISK LEVEL: {get_risk_level_name(risk_level)}
❌ NO TRADING OPPORTUNITIES FOUND - EXITING ANALYSIS

🔍 POSSIBLE REASONS:
• Market is closed (try during 9:15 AM - 3:30 PM IST)
• No stocks meeting risk criteria
• API connectivity issues
• Invalid or expired API credentials

💡 RECOMMENDED ACTIONS:
• Check if market is open (9:15 AM - 3:30 PM IST)
• Try a different risk level
• Verify Zerodha API credentials
• Try again during market hours

🚫 ANALYSIS TERMINATED: No opportunities found for {get_risk_level_name(risk_level)} risk level
"""
        
        # Format output
        risk_name = get_risk_level_name(risk_level)
        output = f"""
=== DYNAMIC MARKET SCANNER: {risk_name.upper()} TRADING OPPORTUNITIES ===
📊 RISK LEVEL: {risk_name}
📊 FILTERS APPLIED: Dynamic Market Scan | Risk-Based Selection | Limited to Top {limit}

📊 MARKET OVERVIEW:
• Total Stocks Analyzed: {len(analyzed_stocks)}
• Top Opportunities: {len(top_stocks)}
• Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• Risk Level: {risk_name}
• Selection Criteria: Dynamic market data analysis

🎯 TOP {risk_name.upper()} TRADING OPPORTUNITIES:
"""
        
        for i, stock in enumerate(top_stocks, 1):
            output += f"""
STOCK {i}: {stock['symbol']}
PRICE: ₹{stock['current_price']:.2f}
VOLUME: {stock['volume']:,}
VOLATILITY: {stock['volatility_score']:.2f}%
MOMENTUM: {stock['momentum_score']:.2f}%
OPPORTUNITY_SCORE: {stock['opportunity_score']:.2f}
RISK_CATEGORY: {stock['risk_category']}
"""
        
        output += f"""
💡 {risk_name.upper()} RISK TRADING INSIGHTS:
• Risk Level: {risk_name}
• Expected Movements: {get_expected_movements(risk_level)}
• Stock Types: {get_stock_types(risk_level)}
• Volatility Range: {get_volatility_range(risk_level)}
• Risk-Reward Profile: {get_risk_reward_profile(risk_level)}

🎯 RECOMMENDED FOCUS:
• {get_focus_recommendations(risk_level)}

⚠️ RISK CONSIDERATIONS:
• {get_risk_considerations(risk_level)}
"""
        
        return output
        
    except Exception as e:
        return f"Error in get_dynamic_trading_stocks: {str(e)}"

def get_risk_category(risk_level, current_price, volatility_score, volume_ratio):
    """Determine if stock fits the risk category"""
    if risk_level == "1":  # Low risk
        return (current_price > 100 and  # Any price above ₹100
                volatility_score < 2.0 and  # Low volatility (0-2%)
                volume_ratio > 0.1)  # Any volume
    elif risk_level == "2":  # Mid risk
        return (current_price > 50 and  # Any price above ₹50
                volatility_score >= 1.0 and volatility_score <= 4.0 and  # Medium volatility (1-4%)
                volume_ratio > 0.05)  # Any volume
    else:  # High risk
        return (current_price > 10 and  # Any price above ₹10
                volatility_score > 3.0 and  # High volatility (>3%)
                volume_ratio > 0.01)  # Any volume

def get_risk_level_name(risk_level):
    """Get risk level name"""
    if risk_level == "1":
        return "Low Risk"
    elif risk_level == "2":
        return "Mid Risk"
    else:
        return "High Risk"

def get_expected_movements(risk_level):
    """Get expected price movements for risk level"""
    if risk_level == "1":
        return "1-2% daily movements"
    elif risk_level == "2":
        return "2-4% daily movements"
    else:
        return "5%+ daily movements"

def get_stock_types(risk_level):
    """Get stock types for risk level"""
    if risk_level == "1":
        return "Large cap, stable stocks"
    elif risk_level == "2":
        return "Mid cap, balanced stocks"
    else:
        return "Small cap, volatile stocks"

def get_volatility_range(risk_level):
    """Get volatility range for risk level"""
    if risk_level == "1":
        return "0-3% daily range"
    elif risk_level == "2":
        return "2-6% daily range"
    else:
        return "4%+ daily range"

def get_risk_reward_profile(risk_level):
    """Get risk-reward profile for risk level"""
    if risk_level == "1":
        return "Conservative, steady gains"
    elif risk_level == "2":
        return "Balanced risk-reward"
    else:
        return "Aggressive, high potential"

def get_focus_recommendations(risk_level):
    """Get focus recommendations for risk level"""
    if risk_level == "1":
        return "Stable large caps for steady growth"
    elif risk_level == "2":
        return "Mid cap stocks for balanced opportunities"
    else:
        return "Volatile small caps for high returns"

def get_risk_considerations(risk_level):
    """Get risk considerations for risk level"""
    if risk_level == "1":
        return "Lower risk but also lower returns, suitable for conservative traders"
    elif risk_level == "2":
        return "Balanced risk with moderate returns, suitable for most traders"
    else:
        return "High risk with potential for high returns, suitable for aggressive traders only"
