import yfinance as yf
from crewai.tools import tool

def transform_stock_data(info):
    """
    Transforms stock data from JSON format to individual variables.
    
    Parameters:
        info (dict): Stock information dictionary from yfinance
    
    Returns:
        dict: Dictionary containing all transformed stock data
    """
    
    # Transform all the specified key values
    transformed_data = {
        # Basic Price Information
        "current_price": info.get("regularMarketPrice"),
        "previous_close": info.get("previousClose"),
        "open_price": info.get("open"),
        "day_low": info.get("dayLow"),
        "day_high": info.get("dayHigh"),
        
        # Financial Metrics
        "beta": info.get("beta"),
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "debt_to_equity": info.get("debtToEquity"),
        "revenue_per_share": info.get("revenuePerShare"),
        
        # Volume Information
        "volume": info.get("volume"),
        "average_volume": info.get("averageVolume"),
        "average_volume_10days": info.get("averageVolume10days"),
        "average_daily_volume_3month": info.get("averageDailyVolume3Month"),
        
        # Bid/Ask Information
        "bid": info.get("bid"),
        "ask": info.get("ask"),
        "bid_size": info.get("bidSize"),
        "ask_size": info.get("askSize"),
        
        # Market Cap and Shares
        "market_cap": info.get("marketCap"),
        "float_shares": info.get("floatShares"),
        "shares_outstanding": info.get("sharesOutstanding"),
        
        # Price Ranges
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "all_time_high": info.get("allTimeHigh"),
        "all_time_low": info.get("allTimeLow"),
        "fifty_day_average": info.get("fiftyDayAverage"),
        "two_hundred_day_average": info.get("twoHundredDayAverage"),
        
        # Target Prices and Recommendations
        "target_high_price": info.get("targetHighPrice"),
        "target_low_price": info.get("targetLowPrice"),
        "target_mean_price": info.get("targetMeanPrice"),
        "target_median_price": info.get("targetMedianPrice"),
        "recommendation_mean": info.get("recommendationMean"),
        
        # Currency
        "currency": info.get("currency", "INR")
    }
    
    return transformed_data

@tool("Live stock information tool")
def get_stock_price(stock_symbol: str):
    """
    💡 Retrieves comprehensive stock information for a given stock symbol using Yahoo Finance.
    
    Parameters:
        stock_symbol (str): The ticker symbol of the stock (e.g., AAPL, TSLA, MSFT).
    
    Returns:
        str: A comprehensive summary of all stock data including price, volume, financial metrics, etc.
    """
    
    stock = yf.Ticker(stock_symbol)
    info = stock.info
    
    # Transform the data using our transformation function
    transformed_data = transform_stock_data(info)
    
    # Extract all values
    current_price = transformed_data["current_price"]
    previous_close = transformed_data["previous_close"]
    open_price = transformed_data["open_price"]
    day_low = transformed_data["day_low"]
    day_high = transformed_data["day_high"]
    beta = transformed_data["beta"]
    trailing_pe = transformed_data["trailing_pe"]
    forward_pe = transformed_data["forward_pe"]
    debt_to_equity = transformed_data["debt_to_equity"]
    revenue_per_share = transformed_data["revenue_per_share"]
    volume = transformed_data["volume"]
    average_volume = transformed_data["average_volume"]
    average_volume_10days = transformed_data["average_volume_10days"]
    average_daily_volume_3month = transformed_data["average_daily_volume_3month"]
    bid = transformed_data["bid"]
    ask = transformed_data["ask"]
    bid_size = transformed_data["bid_size"]
    ask_size = transformed_data["ask_size"]
    market_cap = transformed_data["market_cap"]
    float_shares = transformed_data["float_shares"]
    shares_outstanding = transformed_data["shares_outstanding"]
    fifty_two_week_low = transformed_data["fifty_two_week_low"]
    fifty_two_week_high = transformed_data["fifty_two_week_high"]
    all_time_high = transformed_data["all_time_high"]
    all_time_low = transformed_data["all_time_low"]
    fifty_day_average = transformed_data["fifty_day_average"]
    two_hundred_day_average = transformed_data["two_hundred_day_average"]
    currency = transformed_data["currency"]
    target_high_price = transformed_data["target_high_price"]
    target_low_price = transformed_data["target_low_price"]
    target_mean_price = transformed_data["target_mean_price"]
    target_median_price = transformed_data["target_median_price"]
    recommendation_mean = transformed_data["recommendation_mean"]
    
    # Additional data for change calculations
    change = info.get("regularMarketChange")
    change_percent = info.get("regularMarketChangePercent")
    
    if current_price is None:
        return f"Could not fetch price for {stock_symbol}. Please check the symbol."
    
    # Format large numbers for better readability
    def format_number(num):
        if num is None:
            return "N/A"
        if isinstance(num, (int, float)) and num >= 1e9:
            return f"{num/1e9:.2f}B"
        elif isinstance(num, (int, float)) and num >= 1e6:
            return f"{num/1e6:.2f}M"
        elif isinstance(num, (int, float)) and num >= 1e3:
            return f"{num/1e3:.2f}K"
        else:
            return f"{num:,}" if isinstance(num, (int, float)) else str(num)
    
    return (
        f"=== COMPREHENSIVE STOCK ANALYSIS: {stock_symbol.upper()} ===\n\n"
        
        f"📊 BASIC PRICE INFORMATION:\n"
        f"• Current Price: {current_price} {currency}\n"
        f"• Previous Close: {previous_close} {currency}\n"
        f"• Open Price: {open_price} {currency}\n"
        f"• Day Low: {day_low} {currency}\n"
        f"• Day High: {day_high} {currency}\n"
        f"• Daily Change: {change} {currency}\n"
        f"• Daily Change %: {change_percent}%\n\n"
        
        f"📈 FINANCIAL METRICS:\n"
        f"• Beta: {beta}\n"
        f"• Trailing P/E: {trailing_pe}\n"
        f"• Forward P/E: {forward_pe}\n"
        f"• Debt to Equity: {debt_to_equity}\n"
        f"• Revenue per Share: {revenue_per_share} {currency}\n\n"
        
        f"📊 VOLUME INFORMATION:\n"
        f"• Current Volume: {format_number(volume)}\n"
        f"• Average Volume: {format_number(average_volume)}\n"
        f"• Average Volume (10 days): {format_number(average_volume_10days)}\n"
        f"• Average Daily Volume (3 months): {format_number(average_daily_volume_3month)}\n\n"
        
        f"💰 BID/ASK INFORMATION:\n"
        f"• Bid: {bid} {currency}\n"
        f"• Ask: {ask} {currency}\n"
        f"• Bid Size: {bid_size}\n"
        f"• Ask Size: {ask_size}\n\n"
        
        f"🏢 MARKET CAP & SHARES:\n"
        f"• Market Cap: {format_number(market_cap)} {currency}\n"
        f"• Float Shares: {format_number(float_shares)}\n"
        f"• Shares Outstanding: {format_number(shares_outstanding)}\n\n"
        
        f"📅 PRICE RANGES:\n"
        f"• 52-Week Low: {fifty_two_week_low} {currency}\n"
        f"• 52-Week High: {fifty_two_week_high} {currency}\n"
        f"• All-Time High: {all_time_high} {currency}\n"
        f"• All-Time Low: {all_time_low} {currency}\n"
        f"• 50-Day Average: {fifty_day_average} {currency}\n"
        f"• 200-Day Average: {two_hundred_day_average} {currency}\n\n"
        
        f"🎯 ANALYST TARGETS:\n"
        f"• Target High Price: {target_high_price} {currency}\n"
        f"• Target Low Price: {target_low_price} {currency}\n"
        f"• Target Mean Price: {target_mean_price} {currency}\n"
        f"• Target Median Price: {target_median_price} {currency}\n"
        f"• Recommendation Mean: {recommendation_mean}\n\n"
        
        f"💱 Currency: {currency}\n"
    )


def get_transformed_stock_data(stock_symbol: str):
    """
    Gets stock data and returns it in the transformed format with individual variables.
    
    Parameters:
        stock_symbol (str): The ticker symbol of the stock
    
    Returns:
        dict: Dictionary with all transformed stock data variables
    """
    stock = yf.Ticker(stock_symbol)
    info = stock.info
    return transform_stock_data(info)
