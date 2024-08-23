from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi
from linebot.models import TextSendMessage, TextMessage, MessageEvent
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot import WebhookHandler
import finnhub
import os

app = Flask(__name__)

load_dotenv()

# Initialize Finnhub API client
finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

# Initialize LINE bot API
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# Lookup Stock Symbol
def lookup_symbol(query):
    try:
        result = finnhub_client.symbol_lookup(query)
        if result['count'] > 0:
            return result['result'][0]['displaySymbol']
        else:
            return None
    except Exception as e:
        print("Error during symbol lookup:", e)
        return None

# Api function
def get_realtime_stock_price(symbol):
    try:
        actual_symbol = lookup_symbol(symbol)
        print("Actual Symbol:", actual_symbol)
        if not actual_symbol:
            return f"No symbol found for {symbol}"
        
        quote = finnhub_client.quote(actual_symbol)
        return f"{actual_symbol}\nCurrent: {quote['c']} USD\nOpen: {quote['o']} USD\nHigh: {quote['h']} USD\nLowest: {quote['l']} USD\nsPrev-Close: {quote['pc']} USD"
    except Exception as e:
        return f"韭菜就乖乖等著被割"
        # return f"Error: {str(e)}"

# Domain root
@app.route('/')
def home():
    return 'Hello, there!'

# Post Api
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text.strip().upper()

    if message_text.startswith("US "):
        stock_symbol = message_text[3:].strip()
        stock_price_info = get_realtime_stock_price(stock_symbol)
        try:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=stock_price_info)
            )
        except LineBotApiError as e:
            app.logger.error(f"Error sending reply: {e}")
