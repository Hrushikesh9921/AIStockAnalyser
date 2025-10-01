"""
Aggressive Trading Task for CrewAI
Provides aggressive trading strategies for higher returns
"""

from crewai import Task
from agents.trader_agent import trader_agent

aggressive_trading_task = Task(
    description="""Use the market scan results to provide AGGRESSIVE trading strategies for higher returns while keeping risk controlled.

    AGGRESSIVE TRADING REQUIREMENTS:
    - Receive market scan results from Market Scanner Agent
    - Focus on top 3-5 opportunities identified
    - Provide aggressive but REALISTIC strategies
    - Use technical analysis for realistic entry/exit points
    - Target realistic returns (1-2% for intraday, 3-5% for swing)
    - Use proper risk management with realistic constraints
    
    CRITICAL REALISTIC CONSTRAINTS:
    - ALL entry points must be within 0.5% of current price
    - ALL targets must be realistic (1-2% for intraday, 3-5% for swing)
    - ALL stop losses must be realistic (0.5-1% of current price)
    - Use technical analysis to determine realistic levels
    - Consider current market conditions and volatility
    - NO unrealistic price levels (e.g., 14% moves for intraday)
    
    STRATEGY TYPES:
    1. AGGRESSIVE INTRADAY STRATEGIES:
       - Target 2-3% moves for 4-6% returns (2x leverage)
       - Use tight stop losses (0.5-1% vs 1-2% conservative)
       - Focus on momentum and breakout strategies
       - Quick entry/exit for maximum efficiency
    
    2. AGGRESSIVE F&O STRATEGIES:
       - Use maximum available leverage (3-5x)
       - Target 1-2% moves for 3-6% returns
       - Focus on high-probability setups
       - Use options for higher leverage
    
    3. BANK NIFTY AGGRESSIVE STRATEGIES:
       - Monthly expiry derivatives focus
       - Target 1-2% moves for 4-8% returns
       - Use futures and options combinations
       - Focus on banking sector opportunities
    
    RISK MANAGEMENT:
    - Position sizing: 2-3% risk per trade (vs 1% conservative)
    - Stop losses: Tight but realistic
    - Time management: Quick exits for intraday
    - Volatility management: Reduce size in high volatility
    - Correlation risk: Avoid correlated positions
    
    SUCCESS FACTORS:
    - Strong directional bias
    - High volume confirmation
    - News catalyst support
    - Technical breakout confirmation
    - Market sentiment alignment
    - Quick execution and exit
    """,
    expected_output="""
    AGGRESSIVE TRADING STRATEGIES FOR HIGHER RETURNS:
    
    📊 MARKET ANALYSIS:
    - Analysis of top opportunities from market scan
    - Risk assessment for each opportunity
    - Market conditions and sentiment
    
    🎯 AGGRESSIVE INTRADAY STRATEGIES:
    - Top 3 intraday opportunities with aggressive targets
    - Entry/exit levels with tight stop losses
    - Risk-reward ratios and profit potential
    - Time frames and execution guidelines
    
    📈 AGGRESSIVE F&O STRATEGIES:
    - Futures strategies with maximum leverage
    - Options strategies for higher returns
    - Bank Nifty monthly expiry opportunities
    - Risk management for leveraged positions
    
    💡 AGGRESSIVE TECHNIQUES:
    - Momentum trading strategies
    - Breakout trading techniques
    - News and event trading
    - Sector rotation strategies
    
    ⚠️ RISK MANAGEMENT:
    - Position sizing guidelines
    - Stop loss strategies
    - Time management rules
    - Volatility considerations
    - Correlation risk management
    
    🚀 EXECUTION PLAN:
    - Priority order for opportunities
    - Entry timing and execution
    - Exit strategies and profit booking
    - Risk monitoring and adjustment
    """,
    agent=trader_agent
)
