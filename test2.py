from dotenv import load_dotenv
import finnhub
import os

load_dotenv()

finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

print(finnhub_client.symbol_lookup('APPLE INC'))
