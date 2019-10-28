
import os
import sys
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('4M7OKL3bDlZC/dRpKMyXvp3DhGT2e3HBDO+lBDzbRkkHBG166ljOXMIldXImFp7OLuSqjAvA9FLAmMbdH0AqVMbcp0gtqTmq7ecdeOcuRJ4Omp3JYGpPDl1HH/tLr+Z8i5uj7I4xYRqjOl1w4aEnNgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d43ba340b3cb8752365fb2101ff77ebf')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Don't Know")) #TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
