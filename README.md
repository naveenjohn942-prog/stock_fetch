# Fetching Stock Data using Zerodha Kite Connect

## Usage

1. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

2. **Set Up Environment**:
   - Edit the `.env` file in the project with your Kite Connect API credentials:

     ```
     API_KEY=your_api_key
     API_SECRET=your_api_secret
     REQUEST_TOKEN=your_request_token
     ```
     
3. **Symbols File**:
   - The file `symbols.csv` file is a list of stock symbol names, whose data you migh want to fetch.

4. **Run the Script**:
   ```sh
   python app.py
   ```
   This command will fetch and download historical data for the symbols listed in `symbols.csv` and save it to `stock_data.csv` in the same directory.

## Notes
- For large datasets or frequent requests, the API rate limits of Kite Connect may become a problem.

