#!/usr/bin/python
# encoding: utf-8
import json
import csv

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

# config = configparser.ConfigParser()
# config.read("config.ini")

line_bot_api = LineBotApi('your_Channel access token')
handler = WebhookHandler('your_Channel_secret')

@app.route('/')
def index():
    return "<p>check status!</p>"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print event.message.text
    with open('./ans.csv','rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if event.message.text == row[0]:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text = row[1]))
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(debug=True)