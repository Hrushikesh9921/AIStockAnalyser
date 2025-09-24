# AI Stock Analyser

A comprehensive AI-powered stock analysis system built with CrewAI that provides detailed financial analysis and trading recommendations.

## 🚀 Features

- **Comprehensive Stock Data**: Retrieves 35+ data points including price, volume, financial metrics, and analyst targets
- **AI-Powered Analysis**: Uses CrewAI agents for intelligent financial analysis
- **Trading Recommendations**: Provides detailed buy/sell/hold recommendations with entry/exit strategies
- **Multi-Market Support**: Works with Indian (NSE/BSE) and international stock markets
- **Real-time Data**: Live stock information using Yahoo Finance API

## 📊 Data Coverage

### Basic Price Information
- Current Price, Previous Close, Open Price
- Day Low/High, Daily Change & Percentage

### Financial Metrics
- Beta, Trailing P/E, Forward P/E
- Debt to Equity, Revenue per Share

### Volume & Market Data
- Current Volume, Average Volume (10 days, 3 months)
- Bid/Ask Information, Market Cap, Shares Outstanding

### Price Ranges
- 52-Week Low/High, All-Time High/Low
- 50-day & 200-day Moving Averages

### Analyst Targets
- Target High/Low/Mean/Median Prices
- Recommendation Mean

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hrushikesh9921/AIStockAnalyser.git
   cd AIStockAnalyser
   ```

2. **Create a virtual environment**
   ```bash
   conda create -n crew python=3.12
   conda activate crew
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## 🎯 Usage

### Basic Usage
```python
from main import run

# Analyze a stock
run("TATAMOTORS.NS")  # Indian stock
run("AAPL")           # US stock
run("TSLA")           # Tesla
```

### Using the Stock Tool Directly
```python
from tools.stock_rearch_tool import get_stock_price

# Get comprehensive stock data
result = get_stock_price("TATAMOTORS.NS")
print(result)
```

## 🏗️ Project Structure

```
AIStockAnalyser/
├── agents/                 # AI agents
│   ├── analyst_agent.py   # Financial market analyst
│   └── trader_agent.py    # Strategic stock trader
├── tasks/                 # CrewAI tasks
│   ├── analyse_task.py    # Stock analysis task
│   └── trade_task.py      # Trading decision task
├── tools/                 # Custom tools
│   └── stock_rearch_tool.py  # Stock data retrieval tool
├── crew.py               # CrewAI configuration
├── main.py               # Main application entry point
└── requirements.txt      # Python dependencies
```

## 🤖 AI Agents

### Senior Financial Market Analyst
- Analyzes stock performance and market trends
- Provides comprehensive financial insights
- Identifies key drivers and risk factors

### Senior Strategic Financial Stock Trader
- Makes strategic trading decisions
- Provides entry/exit strategies with risk management
- Offers multiple trading strategies with probability assessments

## 📈 Example Output

```
=== COMPREHENSIVE STOCK ANALYSIS: TATAMOTORS.NS ===

📊 BASIC PRICE INFORMATION:
• Current Price: 682.95 INR
• Previous Close: 701.35 INR
• Daily Change: -18.40 INR (-2.62%)

📈 FINANCIAL METRICS:
• Beta: 1.071
• Trailing P/E: 11.205086
• Forward P/E: 10.557156

🎯 ANALYST TARGETS:
• Target High Price: 1300.0 INR
• Target Low Price: 575.0 INR
• Recommendation Mean: 2.62963
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for AI analysis

### Stock Symbols
- Indian stocks: Use `.NS` suffix (e.g., `TATAMOTORS.NS`)
- US stocks: Use standard symbols (e.g., `AAPL`, `TSLA`)

## 📋 Requirements

- Python 3.12+
- OpenAI API key
- Internet connection for real-time data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This tool is for educational and research purposes only. It should not be considered as financial advice. Always do your own research and consult with financial professionals before making investment decisions.

## 🆘 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Built with ❤️ using CrewAI and Python**
