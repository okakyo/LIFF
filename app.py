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
    PostbackAction,URIAction,LocationAction
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#データを取得して、URLを返還する。その後、

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
    questions=['作り方','お店','お土産','飴ちゃん']
   
    if(event.message.text=='オーダー'):
        items=[QuickReplyButton(action=PostbackAction(label=f"{question}",data=f"{question}")) for question in questions]
        orders=TextSendMessage(text="何する？",quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token,messages=orders)

    elif(event.message.text=='リスト'):
         buttons_template = ButtonsTemplate(
            title='My buttons sample',text='Hello, my buttons',thumbnail_image_url="https://denx.jp/wp-content/uploads/2018/04/cropped-DENXバナー2-1-1.png",actions=[
                URIAction(label='ホームページ', uri='https://denx.jp')
            ])
         template_message = TemplateSendMessage(alt_text='DENXサイト', template=buttons_template)
         line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(PostbackEvent)
def hander_postback(event):
    text=event.postback.data
    if text=='飴ちゃん':
        line_bot_api.push_message(event.source.user_id,messages=ImageSendMessage(
            original_content_url='https://1.bp.blogspot.com/-ZELov-QvHaU/UVWMfIiV3bI/AAAAAAAAPIM/xxWcxLdHrwk/s1600/candy.png',
            preview_image_url='https://1.bp.blogspot.com/-ZELov-QvHaU/UVWMfIiV3bI/AAAAAAAAPIM/xxWcxLdHrwk/s1600/candy.png'
        ))
    elif text=='お土産':
        pass
    elif text=='作り方':
        pass
    elif text=='お店':
        pass

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)