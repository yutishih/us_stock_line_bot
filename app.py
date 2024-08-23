from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import finnhub

app = Flask(__name__)

# Initialize Finnhub API client
finnhub_client = finnhub.Client(api_key='cr3cjj9r01qk9rv5cuk0cr3cjj9r01qk9rv5cukg')

# LINE Channel Access Token & Channel Secret
line_bot_api = Configuration(access_token='8sS5BQ38SPvL1bTibV6aDggk2OQPtZyjHx71dZWhQr66C8EdnrCLVEwQ6tbzvclp9cyaA9K7H3kDaoDEYjcDCB8WTpjS1a4CUuSH0YEcV+GQgUR1O0I60dgho4e/PJe9yVhDNcA5Mudw6Y4HYMhZfwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4631c0fbbabdf5efeb70405d038f1a35')

# Api function
def get_realtime_stock_price(symbol):
    try:
        quote = finnhub_client.quote(symbol)
        return f"{symbol} Current price: {quote['c']} USD\n Open price: {quote['o']} USD\n High price: {quote['h']} USD\n Lowest price: {quote['l']} USD\n Previous Close: {quote['pc']} USD"
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

# Get client input
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    stock_symbol = event.message.text.strip().upper()

    stock_price_info = get_realtime_stock_price(stock_symbol)
    line_bot_api.reply_message( ReplyMessageRequest( reply_token=event.reply_token, messages=[TextMessage(text=stock_price_info)]))


if __name__ == "__main__":
    app.run()
