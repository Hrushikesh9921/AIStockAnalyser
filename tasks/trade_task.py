from crewai import Task
from agents.trader_agent import trader_agent

trade_decision = Task(
    description="""Use live Indian market data for stock {stock} to provide REALISTIC trading recommendations using Zerodha as PRIMARY data source.

    PRIMARY DATA SOURCE: Zerodha Kite Connect
    1. get_zerodha_stock_data - For real-time Indian market conditions, live prices, volume
    2. get_zerodha_historical_data - For Indian market historical patterns and trends
    3. get_zerodha_futures_data - For futures trading opportunities and leverage analysis
    4. get_zerodha_options_chain - For options trading strategies and volatility analysis
    5. get_zerodha_derivatives_strategy - For advanced derivatives strategies
    
    SECONDARY DATA SOURCE: Yahoo Finance (Optional)
    6. get_stock_price - Use only for additional fundamental analysis if needed

    INDIAN MARKET TRADING CONSTRAINTS:
    - Large-cap Indian stocks (like Reliance) typically move 1-3% daily
    - Entry points must be within 2-3% of current price
    - Intraday targets: ±0.5-1.5% for large caps
    - Swing targets: ±2-5% for large caps
    - Consider Indian market liquidity and trading patterns
    - Risk-reward ratio should be at least 1:1

    ZERODHA PRIMARY ANALYSIS:
    - START with Zerodha real-time data for current Indian market conditions
    - Use Zerodha historical data for Indian market patterns and trends
    - Use Zerodha futures data for leverage opportunities and margin analysis
    - Use Zerodha options chain for volatility analysis and options strategies
    - Use Zerodha derivatives strategy for advanced trading approaches
    - Focus on NSE/BSE trading dynamics and Indian market sentiment
    - Use Yahoo Finance ONLY for supplementary fundamental analysis if needed
    - Analyze Indian market specific factors and local trading patterns

    Analyze:
    - Current price vs support/resistance levels (from Zerodha data)
    - Daily range and realistic movement potential for Indian markets
    - Volume trends and Indian market sentiment
    - Technical indicators with realistic expectations for Indian markets
    - Risk management principles specific to Indian trading

    Provide 3 realistic trading strategies for Indian markets:
    1. Intraday strategy (same day entry/exit) - Indian market focus
    2. Short-term swing strategy (2-5 days) - Indian market patterns
    3. Derivatives strategy (futures/options) - Advanced trading approach
    
    Each strategy must include realistic entry/exit points, stop losses, and profit targets based on Indian market conditions.
    For derivatives strategies, consider leverage, time decay, and volatility factors.
    """,
    expected_output="""
    COMPREHENSIVE INDIAN MARKET TRADING ANALYSIS (Zerodha Primary):
    
    📊 ZERODHA PRIMARY ANALYSIS:
    - Real-time Indian market data: Current price, volume, trading patterns
    - Historical trends and patterns from Zerodha historical data
    - Indian market sentiment and NSE/BSE trading dynamics
    - Local market conditions and trading patterns
    
    📈 INDIAN MARKET OVERVIEW:
    - Current stock price and daily change (from Zerodha data)
    - Volume analysis and Indian market sentiment
    - Key technical levels (support/resistance) from Indian market data
    - Realistic movement potential (1-3% for large caps) in Indian context
    - Historical pattern analysis using Zerodha historical data
    
    💡 TRADING RECOMMENDATION (Indian Market Focus):
    - Clear recommendation: BUY/SELL/HOLD based on Indian market conditions
    - Justification based on Zerodha data analysis
    - Indian market specific factors and trading patterns
    - Supplementary Yahoo Finance data (if used) for additional context
    
    🎯 STRATEGY 1 - INTRADAY TRADING (Indian Market):
    - Entry point (within 2-3% of current price)
    - Exit target (realistic ±0.5-1.5% for large caps)
    - Stop loss (risk management for Indian markets)
    - Expected profit/loss percentage
    - Probability of execution in Indian market conditions
    - Real-time Indian market conditions (Zerodha data)
    
    📈 STRATEGY 2 - SHORT-TERM SWING (Indian Market):
    - Entry point (realistic pullback or breakout for Indian markets)
    - Exit target (realistic ±2-5% for large caps)
    - Stop loss (risk management for Indian trading)
    - Time horizon (2-5 days)
    - Expected profit/loss percentage
    - Historical pattern validation (Zerodha historical data)
    
    ⚠️ RISK MANAGEMENT (Indian Market Focus):
    - Risk-reward ratio analysis for Indian markets
    - Indian market conditions consideration
    - NSE/BSE liquidity and execution factors
    - Indian market specific risk assessment using Zerodha data
    """,
    agent=trader_agent

)