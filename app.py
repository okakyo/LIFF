from flask import Flask, request, abort,render_template
import os,json
import subprocess
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
    BeaconEvent,QuickReply,QuickReplyButton,
    TemplateSendMessage,ButtonsTemplate,
    CarouselTemplate,CarouselColumn,PostbackEvent,MessageAction,
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
    answer=''
    print(text)
    if text=='入部':
        answer+='こちらから登録をお願いします。\n{}\n'.format(url[1])
    elif text=='LIFF':
        answer+='LIFFを起動します。\n{}\n'.format(url[0])
    elif text=='DENX':
        answer+='DENXはこちら。\n{}\n'.format(url[3])
    elif text=='使い方':
        answer+='使い方はこちらで確認できます。\n{}\n'.format(url[2])
    else:
        answer='すいません、お答えできません。'
    print(answer)
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
    questions=['入部','LIFF','DENX','使い方']
    items=[QuickReplyButton(action=MessageAction(label=f"{question}",text=f"{question}")) for question in questions]
    orders=TextSendMessage(text="何かございますか？",quick_reply=QuickReply(items=items))
    line_bot_api.reply_message(
        event.reply_token,messages=orders)

@handler.add(PostbackEvent)
def hander_postback(event):
    pass

@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(event.reply_token,
    TextSendMessage(text='ビーコンを認知しました. hwid='+event.beacon.hwid))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)