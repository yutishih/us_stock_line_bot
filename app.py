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

# Api function
def get_realtime_stock_price(symbol):
    try:
        quote = finnhub_client.quote(symbol)
        return f"{symbol}\n Current: {quote['c']} USD\n Open: {quote['o']} USD\n High: {quote['h']} USD\n Lowest: {quote['l']} USD\n Prev-Close: {quote['pc']} USD"
    except Exception as e:
        return f"Error: {str(e)}"

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
