from crewai import Task
from agents.trader_agent import trader_agent

trade_decision = Task(
    description="""Use Live market data and stock performance indicators for stock {stock} to make strategic trading decision.
    Assess any key factors such as current price,daily movement and change percentages, volume trends, recent momentum, 
    market sentiment, technical analysis, resistance in market etc.
    Predict the stock movement based on multiple market parameters, technical analysis, trends etc and Provide entry and 
    exit values for profitable trade for different profit percentages along with corresponding risks and possible losses.
    Based on your analysis recommend which trade to take and whether to **Buy** , **Sell** , **Short** or **Hold** the stock.
    Consider market pre-open conditions for decision making.
    You must Consider current bid / Ask information for building strategy and provide realistic strategy.
    Provide 2 different trade strategies for current day with profit percentages and risks and probability of execution.
    """,
    expected_output="""
    Bullet pointed summary of
    A clear and confident trading recommendation (BUY / SELL / HOLD) with entry / exit strategy for current day : 
    - current stock price
    - Daily price change and percentage
    - Volume and Volatility
    - Immediate trends and observations
    - Market sentiments
    - Entry / exit values with profit / loss percentage and probability to minimize loss and maximize gain
        -Trade strategy 1 : Long Term 
        -Trade strategy 2 : Short term for intraday trading
    - Justification for trading action based on technical signals, risk reward outlook.
    """,
    agent=trader_agent

)