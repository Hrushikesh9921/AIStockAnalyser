"""
Trading Summary Task for CrewAI
Provides intelligent summary and insights for trading decisions
"""

from crewai import Task
from agents.summarizer_agent import summarizer_agent

trading_summary_task = Task(
    description="""Create a simple trading table with exactly 5 opportunities.

    REQUIREMENTS:
    - Extract the 5 stocks from market scan results
    - Create a simple table with: Stock, Price, Signal, Entry, Target, Stop Loss, Risk%, Reward%, Prob%, Priority
    - Focus on HIGH VOLATILITY stocks that can move 5%+ daily
    - Use realistic entry/exit points for volatile stocks
    - Keep output BRIEF and ACTIONABLE
    
    FORMAT:
    | # | Stock | Price | Signal | Entry | Target | Stop Loss | Risk% | Reward% | Prob% | Priority |
    |---|-------|-------|--------|-------|--------|-----------|-------|---------|-------|----------|
    | 1 | IDFCFIRSTB | ₹70 | BUY | ₹71 | ₹74 | ₹68 | 2.9% | 4.3% | 75% | HIGH |
    | 2 | ADANIPORTS | ₹1404 | BUY | ₹1415 | ₹1474 | ₹1390 | 1.8% | 4.2% | 70% | HIGH |
    | 3 | ADANIENT | ₹2510 | BUY | ₹2530 | ₹2636 | ₹2485 | 1.8% | 4.2% | 65% | MEDIUM |
    | 4 | ADANIGREEN | ₹1034 | BUY | ₹1045 | ₹1096 | ₹1025 | 1.9% | 4.9% | 70% | MEDIUM |
    | 5 | ADANIPOWER | ₹147 | BUY | ₹149 | ₹156 | ₹145 | 2.7% | 4.8% | 60% | LOW |
    
    CRITICAL: Show exactly 5 trades in this exact table format.
    
    CRITICAL REQUIREMENTS:
    - ALL entry/exit points must be within 0.5% of current price
    - ALL targets must be realistic (1-2% for intraday, 3-5% for swing)
    - ALL stop losses must be realistic (0.5-1% of current price)
    - Use technical analysis to determine realistic levels
    - Consider volume, market sentiment, and volatility
    - NO unrealistic price levels (e.g., 14% moves for intraday)
    
    TABULAR SUMMARY FORMAT (MANDATORY):
    You MUST provide a clean table with exactly 5 opportunities in this format:
    
    | # | Stock | Price | Volatility | Signal | Entry | Target | Stop Loss | Risk% | Reward% | R:R | Prob% | Priority | Timeframe |
    |---|-------|-------|------------|--------|-------|--------|-----------|-------|---------|-----|-------|----------|-----------|
    | 1 | SYMBOL| ₹XXX  | XX%        | BUY/SELL/SHORT | ₹XXX  | ₹XXX   | ₹XXX      | X.X%  | X.X%    | 1:X | XX%   | HIGH     | Intraday  |
    | 2 | SYMBOL| ₹XXX  | XX%        | BUY/SELL/SHORT | ₹XXX  | ₹XXX   | ₹XXX      | X.X%  | X.X%    | 1:X | XX%   | HIGH     | Intraday  |
    | 3 | SYMBOL| ₹XXX  | XX%        | BUY/SELL/SHORT | ₹XXX  | ₹XXX   | ₹XXX      | X.X%  | X.X%    | 1:X | XX%   | MEDIUM   | Intraday  |
    | 4 | SYMBOL| ₹XXX  | XX%        | BUY/SELL/SHORT | ₹XXX  | ₹XXX   | ₹XXX      | X.X%  | X.X%    | 1:X | XX%   | MEDIUM   | Intraday  |
    | 5 | SYMBOL| ₹XXX  | XX%        | BUY/SELL/SHORT | ₹XXX  | ₹XXX   | ₹XXX      | X.X%  | X.X%    | 1:X | XX%   | LOW      | Intraday  |
    
    For each trading opportunity, provide:
    1. **STOCK/INSTRUMENT**: Symbol, name, current price
    2. **MARKET DATA**: Volume, volatility, daily range, momentum
    3. **TRADING SIGNAL**: BUY/SELL/SHORT SELL based on technical analysis and market sentiment
    4. **ENTRY STRATEGY**: Entry price, entry conditions, entry timing
    5. **EXIT STRATEGY**: Target price, exit conditions, profit potential
    6. **RISK MANAGEMENT**: Stop loss, risk percentage, position size
    7. **PROBABILITY**: Success probability, confidence level, market conditions
    8. **LEVERAGE**: Available leverage, margin requirements, capital efficiency
    9. **TIMEFRAME**: Intraday, swing, or position holding period
    10. **CATALYSTS**: News events, earnings, sector developments
    11. **EXECUTION**: Priority order, timing, market conditions
    
    INTELLIGENT INSIGHTS:
    - Market sentiment analysis and trend identification
    - Correlation analysis between opportunities
    - Risk concentration and diversification assessment
    - Capital allocation recommendations
    - Market timing and execution windows
    - Contingency plans and alternative strategies
    
    PROBABILITY ASSESSMENT:
    - Technical probability based on chart patterns
    - Fundamental probability based on company/sector health
    - Market probability based on overall market conditions
    - News probability based on upcoming events
    - Historical probability based on similar setups
    
    RISK ANALYSIS:
    - Individual trade risk assessment
    - Portfolio risk concentration
    - Market risk factors
    - Liquidity risk considerations
    - Time decay risk for derivatives
    
    EXECUTION GUIDELINES:
    - Priority ranking of opportunities
    - Optimal execution timing
    - Market condition requirements
    - Position sizing recommendations
    - Risk management protocols
    """,
    expected_output="""
    📈 TRADING OPPORTUNITIES TABLE (5 OPPORTUNITIES):
    
    | # | Stock | Price | Signal | Entry | Target | Stop Loss | Risk% | Reward% | Prob% | Priority |
    |---|-------|-------|--------|-------|--------|-----------|-------|---------|-------|----------|
    | 1 | ADANIPORTS | ₹1404 | BUY/SELL | ₹1415 | ₹1474  | ₹1390    | 1.8%  | 4.2%    | 70%   | HIGH     |
    | 2 | ADANIENT | ₹2510 | BUY/SELL | ₹2530 | ₹2636  | ₹2485    | 1.8%  | 4.2%    | 65%   | HIGH     |
    | 3 | JSWSTEEL | ₹850 | BUY/SELL | ₹860 | ₹900   | ₹840     | 1.2%  | 4.7%    | 70%   | MEDIUM   |
    | 4 | TATASTEEL | ₹167 | BUY/SELL | ₹169 | ₹175   | ₹165     | 2.4%  | 4.8%    | 65%   | MEDIUM   |
    | 5 | HINDALCO | ₹450 | BUY/SELL | ₹455 | ₹470   | ₹445     | 2.2%  | 4.4%    | 60%   | LOW      |
    
    💡 ANALYSIS SUMMARY:
    - All 5 stocks analyzed individually with technical and sentiment analysis
    - Realistic entry/exit points within 0.5% of current price
    - Risk-reward ratios optimized for intraday trading
    - Priority ranking based on confidence and market conditions
    
    🎯 EXECUTION STRATEGY:
    - Place orders at market open (9:15 AM)
    - Use LIMIT orders for precise entry points
    - Set target and stop loss orders immediately
    - Monitor for execution and target/stop hit
    """,
    agent=summarizer_agent
)