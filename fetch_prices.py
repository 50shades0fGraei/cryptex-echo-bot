import yfinance as yf
from datetime import datetime

def get_price(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    return ticker.history(period="1d")["Close"].iloc[-1]

def fetch_historical_prices(symbol: str, start_date: datetime, end_date: datetime = None) -> list:
    """Fetch historical price data using yfinance."""
    end_date = end_date or datetime.now()
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date)
    return df["Close"].tolist()
