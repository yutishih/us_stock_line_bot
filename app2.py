import finnhub

# 初始化 Finnhub API 客户端
api_key = 'cr3cjj9r01qk9rv5cuk0cr3cjj9r01qk9rv5cukg'
finnhub_client = finnhub.Client(api_key=api_key)

def get_realtime_stock_price(symbol):
    try:
        quote = finnhub_client.quote(symbol)
        return {
            "Current Price": quote['c'],
            "Open Price": quote['o'],
            "High Price": quote['h'],
            "Low Price": quote['l'],
            "Previous Close": quote['pc']
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    stock_symbol = input("Input US Stock Quote: ")
    stock_price = get_realtime_stock_price(stock_symbol)
    print("Realtime Quote:", stock_price)
