import os
import sys
import json
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_LINE_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_LINE_ACCESS_KEY')
#profile = line_bot_api.get_profile(user_id)

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
    profile = line_bot_api.get_profile(event.source.user_id)

    if(event.message.text[0] == "/"):
        user_input = event.message.text[1:]
        if(user_input == "nama"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=profile.display_name)) #TextSendMessage(text=event.message.text))
        elif(user_input == "gambar"):
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url = profile.picture_url,
                    preview_image_url = profile.picture_url))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)