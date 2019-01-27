from flask import Flask, request, abort,render_template
import os,json
import requests
from bs4 import BeautifulSoup
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

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#データを取得して、URLを返還する。その後、
def AnswerText(text):
    url=['','']
    # 0:質問用のURL、1: 入部登録用のURL 
    answer='スイマセン.こちらからは答えられません.'
    if '入部' and '質問' in text:
      answer='質問こちらから.'+url[0]+'<br>また,入会はこちらから登録をお願いします.'+url[1]
    elif '入部' in text:
        answer='こちらから登録をお願いします.'+ url[1]
    elif '質問' in text:
        answer='質問はこちらからお願いします。'+url[0]
    return answer


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/reserve")
def reserve():
    return render_template('reserve.html')
    
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text=event.MessageEvent.text
    text=AnswerText(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)