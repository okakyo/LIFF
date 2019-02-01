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
    LocationMessage,LocationSendMessage,BeaconEvent,
    VideoMessage,AudioMessage,ImageMessage,
    TemplateSendMessage,ButtonsTemplate,
    StickerMessage,StickerSendMessage,FollowEvent,UnfollowEvent,
    JoinEvent,LeaveEvent,CarouselTemplate,CarouselColumn,PostbackEvent

)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#データを取得して、URLを返還する。その後、
def AnswerText(text):
    url=['line://app/1598486025-dj85Dypj','b','line://app/1598486025-a8Axq2rw','line://app/1598486025-g0OAW9DM']
    # 0:質問用のURL、1: 入部登録用のURL 2:ホームページ用のURL
    answer=''
    if '入部' in text:
        answer+='こちらから登録をお願いします。\n{}\n'.format(url[1])
    if 'LIFF' in text:
        answer+='LIFFを起動します。\n{}\n'.format(url[0])
    if 'DENX' in text:
        answer+='DENXはこちら。\n{}\n'.format(url[3])
    if 'ホーム' in text:
        answer+='ホームページはこちらからお願いします。\n{}\n'.format(url[2])
    else:
        answer='すいません、お答えできません。'
    return answer


@app.route("/")
def hello_world():
    return render_template('index.html')

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
    text=event.message.text
    text=AnswerText(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)