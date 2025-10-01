"""
Live Market Analysis Task for CrewAI
Focuses on real-time market conditions and live trading opportunities
"""

from crewai import Task
from agents.trader_agent import trader_agent

live_market_task = Task(
    description="""Create a LIVE MARKET TRADING ANALYSIS for real-time execution during market hours.

    LIVE MARKET ANALYSIS REQUIREMENTS:
    - Analyze TOP 5 trading opportunities from real-time market scan results (LIMITED TO 5 OPPORTUNITIES)
    - Focus on CURRENT MARKET CONDITIONS and real-time price movements
    - Use get_technical_analysis for proper entry/exit points based on current live prices
    - Use get_market_sentiment_analysis for volume, sentiment, and live market conditions
    - Create comprehensive tabular summary with REALISTIC levels for ALL 5 opportunities
    - Provide intelligent insights and probability assessments for each opportunity
    - Include risk-reward analysis and execution guidelines for LIVE MARKET execution
    - Focus on REAL-TIME EXECUTION strategy - immediate trading opportunities
    
    CRITICAL REQUIREMENTS:
    - ALL entry/exit points must be within 0.5% of current live price
    - ALL targets must be realistic (1-2% for intraday, 3-5% for swing)
    - ALL stop losses must be realistic (0.5-1% of current live price)
    - Use technical analysis to determine realistic levels
    - Consider live volume, market sentiment, and volatility
    - NO unrealistic price levels (e.g., 14% moves for intraday)
    
    TABULAR SUMMARY FORMAT:
    For each trading opportunity, provide:
    1. **STOCK/INSTRUMENT**: Symbol, name, current live price
    2. **MARKET DATA**: Live volume, volatility, daily range, momentum
    3. **TRADING SIGNAL**: BUY/SELL/SHORT SELL based on live technical analysis and market sentiment
    4. **ENTRY STRATEGY**: Live entry price, entry conditions, entry timing
    5. **EXIT STRATEGY**: Live target price, exit conditions, profit potential
    6. **RISK MANAGEMENT**: Live stop loss, risk percentage, position size
    7. **PROBABILITY**: Success probability, confidence level, live market conditions
    8. **LEVERAGE**: Available leverage, margin requirements, capital efficiency
    9. **TIMEFRAME**: Intraday, swing, or position holding period
    10. **CATALYSTS**: Live news events, earnings, sector developments
    11. **EXECUTION**: Priority order, timing, live market conditions
    
    INTELLIGENT INSIGHTS:
    - Live market sentiment analysis and trend identification
    - Real-time correlation analysis between opportunities
    - Live risk concentration and diversification assessment
    - Capital allocation recommendations for live execution
    - Live market timing and execution windows
    - Contingency plans and alternative strategies for live market
    
    PROBABILITY ASSESSMENT:
    - Technical probability based on live chart patterns
    - Fundamental probability based on live company/sector health
    - Market probability based on live market conditions
    - News probability based on live events
    - Historical probability based on similar live setups
    
    RISK ANALYSIS:
    - Individual trade risk assessment for live market
    - Portfolio risk concentration for live execution
    - Live market risk factors
    - Liquidity risk considerations for live trading
    - Time decay risk for live derivatives
    
    EXECUTION GUIDELINES:
    - Priority ranking of live opportunities
    - Optimal live execution timing
    - Live market condition requirements
    - Position sizing recommendations for live market
    - Risk management protocols for live trading
    """,
    expected_output="""
    LIVE MARKET TRADING ANALYSIS & EXECUTION GUIDE
    
    📊 LIVE MARKET OVERVIEW:
    - Total opportunities analyzed: 5 (TOP 5 LIVE OPPORTUNITIES)
    - Current market conditions and live sentiment
    - Risk assessment and recommendations for live execution
    - Capital allocation strategy for live trading
    
    📈 LIVE TRADING OPPORTUNITIES TABLE (TOP 5 OPPORTUNITIES):
    
    | # | Stock | Price | Volatility | Signal | Entry | Target | Stop Loss | Risk% | Reward% | R:R | Prob% | Priority | Timeframe |
    |---|-------|-------|------------|--------|-------|--------|-----------|-------|---------|-----|-------|----------|-----------|
    | 1 | SYMBOL| ₹XXX  | XX%        | BUY/SELL/SHORT | ₹XXX  | ₹XXX   | ₹XXX      | X.X%  | X.X%    | 1:X | XX%   | HIGH     | Intraday  |
    | 2 | SYMBOL| ₹XXX  | XX%        | BUY/SELL/SHORT | ₹XXX  | ₹XXX   | ₹XXX      | X.X%  | X.X%    | 1:X | XX%   | HIGH     | Intraday  |
    | 3 | SYMBOL| ₹XXX  | XX%        | BUY/SELL/SHORT | ₹XXX  | ₹XXX   | ₹XXX      | X.X%  | X.X%    | 1:X | XX%   | MEDIUM   | Intraday  |
    | 4 | SYMBOL| ₹XXX  | XX%        | BUY/SELL/SHORT | ₹XXX  | ₹XXX   | ₹XXX      | X.X%  | X.X%    | 1:X | XX%   | MEDIUM   | Intraday  |
    | 5 | SYMBOL| ₹XXX  | XX%        | BUY/SELL/SHORT | ₹XXX  | ₹XXX   | ₹XXX      | X.X%  | X.X%    | 1:X | XX%   | LOW      | Intraday  |
    
    🎯 DETAILED OPPORTUNITY ANALYSIS (ALL 5 OPPORTUNITIES):
    
    **OPPORTUNITY #1: [STOCK NAME]**
    - **Entry Strategy**: [Breakout/Pullback/Momentum] at ₹XXX
    - **Target Strategy**: [Technical/Fundamental] target at ₹XXX
    - **Stop Loss**: [Support/Resistance] at ₹XXX
    - **Risk-Reward**: 1:X ratio with XX% success probability
    - **Leverage**: Xx leverage with ₹XXX margin requirement
    - **Timeframe**: [Intraday/Swing/Position] with [X] day holding period
    - **Catalysts**: [News/Earnings/Sector] events supporting the trade
    - **Execution**: [Live market conditions/Real-time execution] timing
    
    **OPPORTUNITY #2: [STOCK NAME]**
    - **Entry Strategy**: [Breakout/Pullback/Momentum] at ₹XXX
    - **Target Strategy**: [Technical/Fundamental] target at ₹XXX
    - **Stop Loss**: [Support/Resistance] at ₹XXX
    - **Risk-Reward**: 1:X ratio with XX% success probability
    - **Leverage**: Xx leverage with ₹XXX margin requirement
    - **Timeframe**: [Intraday/Swing/Position] with [X] day holding period
    - **Catalysts**: [News/Earnings/Sector] events supporting the trade
    - **Execution**: [Live market conditions/Real-time execution] timing
    
    **OPPORTUNITY #3: [STOCK NAME]**
    - **Entry Strategy**: [Breakout/Pullback/Momentum] at ₹XXX
    - **Target Strategy**: [Technical/Fundamental] target at ₹XXX
    - **Stop Loss**: [Support/Resistance] at ₹XXX
    - **Risk-Reward**: 1:X ratio with XX% success probability
    - **Leverage**: Xx leverage with ₹XXX margin requirement
    - **Timeframe**: [Intraday/Swing/Position] with [X] day holding period
    - **Catalysts**: [News/Earnings/Sector] events supporting the trade
    - **Execution**: [Live market conditions/Real-time execution] timing
    
    **OPPORTUNITY #4: [STOCK NAME]**
    - **Entry Strategy**: [Breakout/Pullback/Momentum] at ₹XXX
    - **Target Strategy**: [Technical/Fundamental] target at ₹XXX
    - **Stop Loss**: [Support/Resistance] at ₹XXX
    - **Risk-Reward**: 1:X ratio with XX% success probability
    - **Leverage**: Xx leverage with ₹XXX margin requirement
    - **Timeframe**: [Intraday/Swing/Position] with [X] day holding period
    - **Catalysts**: [News/Earnings/Sector] events supporting the trade
    - **Execution**: [Live market conditions/Real-time execution] timing
    
    **OPPORTUNITY #5: [STOCK NAME]**
    - **Entry Strategy**: [Breakout/Pullback/Momentum] at ₹XXX
    - **Target Strategy**: [Technical/Fundamental] target at ₹XXX
    - **Stop Loss**: [Support/Resistance] at ₹XXX
    - **Risk-Reward**: 1:X ratio with XX% success probability
    - **Leverage**: Xx leverage with ₹XXX margin requirement
    - **Timeframe**: [Intraday/Swing/Position] with [X] day holding period
    - **Catalysts**: [News/Earnings/Sector] events supporting the trade
    - **Execution**: [Live market conditions/Real-time execution] timing
    
    💡 LIVE MARKET INTELLIGENT INSIGHTS:
    
    **LIVE MARKET SENTIMENT:**
    - Current market direction and strength
    - Live sector rotation and leadership
    - Real-time volatility expectations and risk appetite
    - Live news flow and event calendar
    
    **LIVE CORRELATION ANALYSIS:**
    - Real-time correlation between opportunities
    - Live risk concentration assessment
    - Current market correlation factors
    - Live diversification opportunities
    
    **LIVE RISK ASSESSMENT:**
    - Individual trade risk levels for live market
    - Live portfolio risk concentration
    - Current market risk factors
    - Live liquidity and execution risk
    - Real-time volatility considerations
    
    **LIVE CAPITAL ALLOCATION:**
    - Recommended position sizes for live market
    - Live leverage utilization strategy
    - Real-time cash reserve management
    - Live risk budget allocation
    
    ⚡ LIVE MARKET EXECUTION STRATEGY:
    
    **PRIORITY RANKING FOR LIVE EXECUTION:**
    1. **HIGH PRIORITY**: [Stock] - [Reason] - [Expected Return] - [Live Action]
    2. **MEDIUM PRIORITY**: [Stock] - [Reason] - [Expected Return] - [Live Action]
    3. **LOW PRIORITY**: [Stock] - [Reason] - [Expected Return] - [Live Action]
    
    **LIVE EXECUTION TIMING:**
    - **IMMEDIATE ORDERS**: Place orders based on live market conditions
    - **ORDER TYPES**: Use appropriate order types for live market conditions
    - **EXECUTION STRATEGY**: Real-time execution based on live market opportunities
    - **MONITORING**: Continuous monitoring of live market conditions
    
    **LIVE CONTINGENCY PLANS:**
    - **If Market Moves Up**: [Strategy] for [Stocks]
    - **If Market Moves Down**: [Strategy] for [Stocks]
    - **If High Volatility**: [Strategy] for [Stocks]
    - **If Low Volume**: [Strategy] for [Stocks]
    
    🚨 LIVE RISK MANAGEMENT PROTOCOLS:
    
    **POSITION SIZING:**
    - Maximum 3% risk per trade for live market
    - Maximum 10% portfolio risk for live execution
    - Live leverage limits based on current volatility
    - Real-time cash reserve for live opportunities
    
    **STOP LOSS STRATEGY:**
    - Live technical stops at current support/resistance
    - Real-time time stops for live intraday positions
    - Live volatility-adjusted stops
    - Real-time trailing stops for live profitable positions
    
    **LIVE MONITORING REQUIREMENTS:**
    - Real-time price monitoring for live market
    - Live volume and volatility tracking
    - Real-time news and event monitoring
    - Live market sentiment changes
    
    📊 LIVE PERFORMANCE METRICS:
    
    **EXPECTED RETURNS:**
    - Live portfolio expected return: X.X%
    - Live risk-adjusted return (Sharpe): X.X
    - Live maximum drawdown: X.X%
    - Live win rate expectation: XX%
    
    **LIVE KEY PERFORMANCE INDICATORS:**
    - Live average risk-reward ratio: 1:X
    - Live success probability: XX%
    - Live capital efficiency: XX%
    - Live time to target: X hours average
    
    🎯 LIVE FINAL RECOMMENDATIONS:
    
    **LIVE IMMEDIATE ACTIONS (ALL 5 OPPORTUNITIES):**
    1. [Action] for [Stock #1] at [Price] with [Reason] - [Order Type]
    2. [Action] for [Stock #2] at [Price] with [Reason] - [Order Type]
    3. [Action] for [Stock #3] at [Price] with [Reason] - [Order Type]
    4. [Action] for [Stock #4] at [Price] with [Reason] - [Order Type]
    5. [Action] for [Stock #5] at [Price] with [Reason] - [Order Type]
    
    **LIVE EXECUTION STRATEGY:**
    - Execute orders based on live market conditions
    - Set target and stop loss orders immediately
    - Monitor for execution and target/stop hit
    - Adjust positions based on live market movements
    
    **LIVE WATCH LIST:**
    - [Stock] - [Condition] - [Action]
    - [Stock] - [Condition] - [Action]
    - [Stock] - [Condition] - [Action]
    
    **AVOID:**
    - [Stock] - [Reason] - [Alternative]
    - [Stock] - [Reason] - [Alternative]
    - [Stock] - [Reason] - [Alternative]
    """,
    agent=trader_agent
)
