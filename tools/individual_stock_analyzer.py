"""
Individual Stock Analyzer Tool
Processes each stock individually and stores results
"""

from crewai.tools import tool
from tools.trading_data_manager import trading_manager
from tools.technical_analysis_tool import get_technical_analysis, get_market_sentiment_analysis
import json

@tool("Individual Stock Analyzer Tool")
def analyze_individual_stock(symbol: str, current_price: float):
    """
    Analyze a single stock and store the results for later combination.
    
    Parameters:
        symbol (str): Stock symbol (e.g., 'TITAN', 'RELIANCE')
        current_price (float): Current price of the stock
    
    Returns:
        str: Analysis result for the stock
    """
    
    try:
        # Get technical analysis
        tech_analysis = get_technical_analysis.func(symbol, current_price)
        
        # Get market sentiment analysis  
        sentiment_analysis = get_market_sentiment_analysis.func(symbol, current_price)
        
        # Parse the analysis results
        tech_data = parse_analysis_result(tech_analysis)
        sentiment_data = parse_analysis_result(sentiment_analysis)
        
        # Combine analysis
        combined_analysis = {
            'signal': tech_data.get('primary_strategy', 'BUY'),
            'entry_price': tech_data.get('entry_price', current_price),
            'target_price': tech_data.get('target_price', current_price * 1.02),
            'stop_price': tech_data.get('stop_price', current_price * 0.99),
            'risk_percent': tech_data.get('risk_percent', 1.0),
            'reward_percent': tech_data.get('reward_percent', 2.0),
            'probability': sentiment_data.get('confidence', 70),
            'priority': determine_priority(tech_data, sentiment_data),
            'summary': f"{symbol} analysis: {tech_data.get('primary_strategy', 'BUY')} signal with {sentiment_data.get('confidence', 70)}% confidence"
        }
        
        # Store in trading manager
        trading_manager.add_stock_analysis(symbol, current_price, combined_analysis)
        
        return f"✅ {symbol} analysis completed and stored. Signal: {combined_analysis['signal']}, Confidence: {combined_analysis['probability']}%"
        
    except Exception as e:
        return f"❌ Error analyzing {symbol}: {str(e)}"

def parse_analysis_result(analysis_text: str) -> dict:
    """Parse analysis result text into structured data"""
    result = {}
    
    try:
        # Extract key information from analysis text
        lines = analysis_text.split('\n')
        for line in lines:
            if 'Signal:' in line or 'Strategy:' in line:
                if 'BUY' in line.upper():
                    result['primary_strategy'] = 'BUY'
                elif 'SELL' in line.upper():
                    result['primary_strategy'] = 'SELL'
                elif 'SHORT' in line.upper():
                    result['primary_strategy'] = 'SHORT SELL'
            
            if 'Entry:' in line or 'Entry Price:' in line:
                # Extract price from line
                import re
                price_match = re.search(r'₹?(\d+\.?\d*)', line)
                if price_match:
                    result['entry_price'] = float(price_match.group(1))
            
            if 'Target:' in line or 'Target Price:' in line:
                import re
                price_match = re.search(r'₹?(\d+\.?\d*)', line)
                if price_match:
                    result['target_price'] = float(price_match.group(1))
            
            if 'Stop:' in line or 'Stop Loss:' in line:
                import re
                price_match = re.search(r'₹?(\d+\.?\d*)', line)
                if price_match:
                    result['stop_price'] = float(price_match.group(1))
            
            if 'Confidence:' in line or 'Probability:' in line:
                import re
                conf_match = re.search(r'(\d+)%', line)
                if conf_match:
                    result['confidence'] = int(conf_match.group(1))
    
    except Exception as e:
        print(f"Error parsing analysis: {e}")
    
    return result

def determine_priority(tech_data: dict, sentiment_data: dict) -> str:
    """Determine priority based on analysis"""
    confidence = sentiment_data.get('confidence', 70)
    signal = tech_data.get('primary_strategy', 'BUY')
    
    if confidence >= 80 and signal in ['BUY', 'SELL']:
        return 'HIGH'
    elif confidence >= 60:
        return 'MEDIUM'
    else:
        return 'LOW'

@tool("Trading Summary Generator Tool")
def generate_trading_summary():
    """
    Generate final trading summary from all stored analyses.
    
    Returns:
        str: Complete trading summary with table
    """
    
    try:
        # Create summary table
        table = trading_manager.create_summary_table()
        
        # Get analysis summary
        analysis_summary = trading_manager.get_analysis_summary()
        
        # Combine into final output
        final_output = f"""
📈 TRADING OPPORTUNITIES TABLE (5 OPPORTUNITIES):

{table}

💡 ANALYSIS SUMMARY:
{analysis_summary}

🎯 EXECUTION STRATEGY:
- Place orders at market open (9:15 AM)
- Use LIMIT orders for precise entry points
- Set target and stop loss orders immediately
- Monitor for execution and target/stop hit
"""
        
        return final_output
        
    except Exception as e:
        return f"❌ Error generating summary: {str(e)}"
