from crewai import Task
from agents.analyst_agent import analyst_agent

get_stock_analysis = Task(
    description="""Analyse the recent performance of the Indian stock : {stock}. Use Zerodha as PRIMARY data source with Yahoo Finance as optional supplementary information:
    
    PRIMARY DATA SOURCE: Zerodha Kite Connect
    1. get_zerodha_stock_data - For real-time Indian market data, live prices, volume, trading patterns
    2. get_zerodha_historical_data - For Indian market historical trends, patterns, and technical analysis
    3. get_zerodha_futures_data - For futures analysis and leverage opportunities
    4. get_zerodha_options_chain - For options analysis and volatility insights
    5. get_zerodha_derivatives_strategy - For advanced derivatives strategies
    
    SECONDARY DATA SOURCE: Yahoo Finance (Optional)
    6. get_stock_price - Use only for additional fundamental analysis (P/E, market cap, financial ratios)
    
    ANALYSIS REQUIREMENTS:
    - START with Zerodha data for comprehensive Indian market analysis
    - Use Zerodha real-time data for current market conditions and trading patterns
    - Analyze historical trends using Zerodha historical data for past week, month, quarter, year
    - Analyze derivatives (futures and options) for advanced trading strategies
    - Use Yahoo Finance ONLY for supplementary fundamental analysis if needed
    - Focus on Indian market dynamics, NSE/BSE trading patterns, and local market sentiment
    - Include derivatives trading opportunities for sophisticated investors
    
    Provide how the Indian stock is performing today using Zerodha data and highlight observations.
    Predict stock movement based on Indian market parameters, technical analysis, and trends.
    Provide entry and exit values for profitable trades with realistic profit percentages and risk assessment.
    Include derivatives trading strategies (futures and options) for advanced traders.
    """,
    expected_output="""
    A comprehensive Indian market analysis using Zerodha as primary data source:
    
    📊 ZERODHA PRIMARY ANALYSIS:
    - Real-time Indian market data: Current price, volume, trading patterns
    - Historical trends and patterns from Zerodha historical data
    - Indian market sentiment and local trading dynamics
    - NSE/BSE specific market conditions
    
    📈 CURRENT INDIAN MARKET STATUS:
    - Current stock price from Zerodha real-time data
    - Daily price change and percentage in Indian market context
    - Volume analysis specific to Indian trading patterns
    - Real-time vs historical price comparison using Zerodha data
    
    🔍 TECHNICAL ANALYSIS (Zerodha Focus):
    - Immediate trends and observations from Indian market data
    - Indian market sentiment and local trading patterns
    - Historical pattern analysis using Zerodha historical data
    - Support and resistance levels based on Indian market data
    
    💡 TRADING RECOMMENDATIONS (Indian Market Focus):
    - Entry and exit points based on Zerodha data analysis
    - Risk assessment using Indian market conditions
    - Profit targets with realistic expectations for Indian markets
    - Supplementary Yahoo Finance data (if used) for additional context
    """,
    agent=analyst_agent

)