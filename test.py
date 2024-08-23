from dotenv import load_dotenv
import finnhub
import os

load_dotenv()

finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

def lookup_symbol(query):
    try:
        result = finnhub_client.symbol_lookup(query)
        if result['count'] > 0:
            # Print result to debug
            # print("Symbol Lookup Result:", result)
            # Only return the first symbol
            return result['result'][0]['displaySymbol']
        else:
            return None
    except Exception as e:
        print("Error during symbol lookup:", e)
        return None

def get_realtime_stock_price(symbol):
    try:
        actual_symbol = lookup_symbol(symbol)
        print("Actual Symbol:", actual_symbol)
        if not actual_symbol:
            return {"error": f"No symbol found for {symbol}"}
        
        quote = finnhub_client.quote(actual_symbol)
        return {
            "Symbol": actual_symbol,
            "Current Price": quote['c'],
            "Open Price": quote['o'],
            "High Price": quote['h'],
            "Low Price": quote['l'],
            "Previous Close": quote['pc']
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    stock_symbol = input("Input US Stock Quote or Company Name: ")
    stock_price = get_realtime_stock_price(stock_symbol)
    print("Realtime Quote:", stock_price)
