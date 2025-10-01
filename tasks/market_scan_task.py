"""
Market Scan Task for CrewAI
Scans market for top opportunities
"""

from crewai import Task
from agents.market_scanner_agent import market_scanner_agent

market_scan_task = Task(
    description="""Scan the Indian market for the most profitable trading opportunities focusing on high-volume, high-volatility stocks and Bank Nifty derivatives.

    MARKET SCANNING REQUIREMENTS:
    - Use get_top_traded_stocks to identify top 10 most profitable opportunities
    - Use get_banknifty_derivatives to analyze Bank Nifty monthly expiry opportunities
    - Focus on stocks with high volume, high volatility, and strong momentum
    - Prioritize aggressive trading opportunities over conservative ones
    - Include both equity and derivatives opportunities
    
        SCANNING CRITERIA:
        - Market Cap: Mid-Cap (₹5,000-20,000 Cr) & Large-Cap (>₹20,000 Cr) only
        - Circuit Filter: Exclude stocks hitting upper/lower circuits
        - Volume: Stocks with volume spikes (2x+ average volume)
        - Volatility: Stocks with daily range >2% for intraday opportunities
        - Momentum: Stocks with strong price movements (>1% in either direction)
        - Liquidity: High liquidity for easy entry/exit
        - Bank Nifty: Monthly expiry derivatives analysis
    
    OPPORTUNITY IDENTIFICATION:
    - Intraday opportunities: Quick 1-3% profit potential
    - F&O opportunities: Leveraged positions for higher returns
    - Bank Nifty focus: Monthly expiry derivatives analysis
    - Risk-reward optimization: Higher returns with controlled risk
    
    HANDOFF REQUIREMENTS:
    - Provide detailed market scan results
    - Highlight top 3-5 opportunities with specific details
    - Include entry/exit levels for each opportunity
    - Provide risk assessment and profit potential
    - Focus on aggressive but calculated opportunities
    """,
    expected_output="""
    COMPREHENSIVE MARKET SCAN RESULTS:
    
    📊 MARKET OVERVIEW:
    - Total stocks analyzed
    - Top opportunities identified
    - Market sentiment and conditions
    
    🎯 TOP TRADING OPPORTUNITIES:
    - Top 3-5 stocks with highest profit potential
    - Specific entry/exit levels for each opportunity
    - Risk assessment and profit potential
    - Volume and volatility analysis
    
    📈 BANK NIFTY DERIVATIVES:
    - Monthly expiry analysis
    - Futures and options opportunities
    - Leverage and risk assessment
    - Time decay considerations
    
    💡 TRADING INSIGHTS:
    - Market sentiment analysis
    - Sector rotation opportunities
    - News and event catalysts
    - Risk management guidelines
    
    ⚠️ RISK CONSIDERATIONS:
    - Volatility assessment
    - Liquidity concerns
    - Market timing factors
    - Position sizing recommendations
    """,
    agent=market_scanner_agent
)
