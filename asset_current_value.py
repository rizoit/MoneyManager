import json
import os
from datetime import date
import yfinance as yf
from pathlib import Path

class AssetCurrentValue:
    """
    Fetches and caches comprehensive asset information including prices and metrics.
    Implements a local JSON cache to minimize API calls.
    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.date = date.today()
        self.cache_file = Path('asset_prices.json')
        self.current_price = self.fetch_current_price()
        
    def load_cache(self):
        """Loads the price cache from JSON file."""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            return {}
        except json.JSONDecodeError:
            return {}

    def save_cache(self, cache_data):
        """Saves the price cache to JSON file."""
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f, indent=4, default=str)

    def fetch_from_yfinance(self):
        """Fetches comprehensive information from Yahoo Finance."""
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            
            # Organize the data according to our template structure
            stock_data = {
                "last_updated": str(self.date),
                "basic_info": {
                    "symbol": info.get("symbol"),
                    "shortName": info.get("shortName"),
                    "longName": info.get("longName"),
                    "sector": info.get("sector"),
                    "industry": info.get("industry"),
                    "country": info.get("country"),
                    "currency": info.get("currency")
                },
                "price_data": {
                    "regularMarketPrice": info.get("regularMarketPrice"),
                    "regularMarketOpen": info.get("regularMarketOpen"),
                    "regularMarketDayHigh": info.get("regularMarketDayHigh"),
                    "regularMarketDayLow": info.get("regularMarketDayLow"),
                    "regularMarketVolume": info.get("regularMarketVolume"),
                    "regularMarketPreviousClose": info.get("regularMarketPreviousClose"),
                    "bid": info.get("bid"),
                    "ask": info.get("ask"),
                    "bidSize": info.get("bidSize"),
                    "askSize": info.get("askSize")
                },
                "financial_metrics": {
                    "marketCap": info.get("marketCap"),
                    "enterpriseValue": info.get("enterpriseValue"),
                    "trailingPE": info.get("trailingPE"),
                    "forwardPE": info.get("forwardPE"),
                    "priceToBook": info.get("priceToBook"),
                    "trailingEps": info.get("trailingEps"),
                    "forwardEps": info.get("forwardEps"),
                    "bookValue": info.get("bookValue")
                },
                "dividend_info": {
                    "dividendRate": info.get("dividendRate"),
                    "dividendYield": info.get("dividendYield"),
                    "exDividendDate": info.get("exDividendDate"),
                    "payoutRatio": info.get("payoutRatio")
                },
                "historical_performance": {
                    "52WeekChange": info.get("52WeekChange"),
                    "52WeekHigh": info.get("fiftyTwoWeekHigh"),
                    "52WeekLow": info.get("fiftyTwoWeekLow"),
                    "50DayAverage": info.get("fiftyDayAverage"),
                    "200DayAverage": info.get("twoHundredDayAverage")
                },
                "volatility_metrics": {
                    "beta": info.get("beta"),
                    "impliedVolatility": info.get("impliedVolatility")
                }
            }
            return stock_data
        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {str(e)}")
            return None

    def fetch_current_price(self):
        """
        Fetches the current price of the asset.
        First checks the local cache, then falls back to Yahoo Finance if needed.
        """
        cache = self.load_cache()
        
        # Check if we have today's data in cache
        if self.ticker in cache:
            cached_data = cache[self.ticker]
            if cached_data['last_updated'] == str(self.date):
                return cached_data['price_data']['regularMarketPrice']

        # If not in cache or outdated, fetch new data
        stock_data = self.fetch_from_yfinance()
        
        if stock_data is not None:
            # Update cache with new data
            cache[self.ticker] = stock_data
            self.save_cache(cache)
            return stock_data['price_data']['regularMarketPrice']
        
        # If fetch failed and we have old cached data, return that
        if self.ticker in cache:
            return cache[self.ticker]['price_data']['regularMarketPrice']
        
        # If all else fails, return None
        return None

    def get_current_price(self):
        """Returns the current price."""
        return self.current_price

    def get_full_info(self):
        """Returns the complete stored information for the ticker."""
        cache = self.load_cache()
        return cache.get(self.ticker)

    def update_database(self):
        """
        Forces an update of all information in the database.
        """
        stock_data = self.fetch_from_yfinance()
        if stock_data is not None:
            cache = self.load_cache()
            cache[self.ticker] = stock_data
            self.save_cache(cache)
            self.current_price = stock_data['price_data']['regularMarketPrice']
        return self.current_price