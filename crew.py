from crewai import Crew
from tasks.market_scan_task import market_scan_task
from tasks.aggressive_trading_task import aggressive_trading_task
from tasks.trading_summary_task import trading_summary_task
from tasks.live_market_task import live_market_task
from agents.market_scanner_agent import market_scanner_agent
from agents.analyst_agent import analyst_agent
from agents.trader_agent import trader_agent
from agents.summarizer_agent import summarizer_agent

# Pre/Post Market Crew - Focus on previous day close analysis
pre_post_market_crew = Crew(
    agents=[market_scanner_agent, analyst_agent, trader_agent, summarizer_agent],
    tasks=[market_scan_task, aggressive_trading_task, trading_summary_task],
    verbose=False
)

# Live Market Crew - Focus on real-time analysis
live_market_crew = Crew(
    agents=[market_scanner_agent, analyst_agent, trader_agent, summarizer_agent],
    tasks=[market_scan_task, aggressive_trading_task, live_market_task],
    verbose=False
)

# Default crew (for backward compatibility)
stock_crew = pre_post_market_crew