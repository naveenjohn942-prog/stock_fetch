# import scrape
import historical_scrape

# fetcher = StockFetcher()
# fetcher.fetch_all_data("test.csv")

stock_fetcher = StockFetcher()
stock_fetcher.fetch_all_data("test.csv", "historical_stock_data.csv")