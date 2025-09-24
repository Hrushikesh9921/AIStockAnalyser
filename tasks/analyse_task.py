from crewai import Task
from agents.analyst_agent import analyst_agent

get_stock_analysis = Task(
    description="""Analyse the recent performance of the stock : {stock}. Use the live stock information tool to receive 
    stock related information current price, trading volume, sentiments, resistance and other market data. 
    Analyse the market news, deals happening in market etc.
    Provide how the stock is performing today and highlight any observations from the data.
    Predict the stock movement based on multiple market parameters, technical analysis, trends etc and Provide entry and 
    exit values for profitable trade for different profit percentages along with corresponding risks and possible losses.
    """,
    expected_output="""
    A clear bullet pointed summary of : 
    - current stock price
    - Daily price change and percentage
    - Volume and Volatility
    - Immediate trends and observations
    - Market sentiments
    """,
    agent=analyst_agent

)