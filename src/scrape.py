from kiteconnect import KiteConnect
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockFetcher:
    def __init__(self, api_key=None, api_secret=None, request_token=None, interval="day", from_date="2023-01-01"):
        load_dotenv()  

        self.api_key = api_key or os.getenv('API_KEY')
        self.api_secret = api_secret or os.getenv('API_SECRET')
        self.request_token = request_token or os.getenv('REQUEST_TOKEN')
        self.interval = interval
        self.from_date = from_date

        self.kite = KiteConnect(api_key=self.api_key)
        self.access_token = self._generate_access_token()
        self.kite.set_access_token(self.access_token)
        self.instrument_lookup = self._create_instrument_lookup()

        self.to_date = self._get_yesterday_date()

    def _generate_access_token(self):
        try:
            # Generate session to get the access token
            data = self.kite.generate_session(self.request_token, api_secret=self.api_secret)
            return data["access_token"]
        except Exception as e:
            logger.error(f"Error generating access token: {e}")
            raise

    def _get_yesterday_date(self):
        current_date = datetime.now()
        yesterday_date = current_date - timedelta(days=1)
        return yesterday_date.strftime("%Y-%m-%d")

    def _create_instrument_lookup(self):
        try:
            instruments = self.kite.instruments()
            return {instrument['tradingsymbol']: instrument['instrument_token'] for instrument in instruments if instrument['exchange'] == 'NSE'}
        except Exception as e:
            logger.error(f"Error fetching instruments: {e}")
            raise

    def fetch_historical_data(self, symbol):
        try:
            instrument_token = self.instrument_lookup.get(symbol)
            if instrument_token is None:
                raise ValueError(f"Instrument token not found for symbol: {symbol}")

            historical_data = self.kite.historical_data(instrument_token, self.from_date, self.to_date, self.interval)
            df = pd.DataFrame(historical_data)
            df['symbol'] = symbol
            df = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']]
            return df
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            raise

    def fetch_all_data(self, symbols_file, output_file="stock_data.csv"):
        try:
            symbols_df = pd.read_csv(symbols_file)
            symbols = symbols_df['symbol'].tolist()
            all_data = pd.DataFrame()

            for symbol in symbols:
                try:
                    df = self.fetch_historical_data(symbol)
                    all_data = pd.concat([all_data, df])
                except Exception as e:
                    logger.error(f"Error fetching data for {symbol}: {e}")

            all_data.to_csv(output_file, index=False)
            logger.info(f"Data successfully saved to {output_file}")
        except Exception as e:
            logger.error(f"Error processing symbols file: {e}")
            raise

if __name__ == "__main__":
    stock_fetcher = StockFetcher(
        api_key="your_api_key",
        api_secret="your_api_secret",
        request_token="your_request_token",
        interval="day",
        from_date="2023-01-01"
    )
    stock_fetcher.fetch_all_data("symbols.csv", "historical_stock_data.csv")
