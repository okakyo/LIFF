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
    PostbackAction,URIAction,LocationAction,ImageMessage,ImageSendMessage
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
YOUR_API_KEYID=os.environ['YOUR_API_KEYID']

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

wanna_eat='たこ焼き'

#データを取得して、URLを返還する。その後、


#食べ物の情報をとってくる函数（ぐるなびAPI）
#引数　　　fName：食べ物の名前
#　　　　　fLat ：現在地の緯度
#　　　　　fLon ：現在地の経度
#return値 レストラン情報
def getFoodsInfo(fName,fLat,fLon):
  url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"

  params={}
  params["keyid"] = YOUR_API_KEYID
  params["freeword"]  = fName
  params["latitude"]  = fLat
  params["longitude"]  = fLon

  #range=検索範囲の半径の大きさ(1~5)　10件以上見つかる最小の大きさを求める
  for i in range(1,6):
    params["range"]  = i
    result = requests.get(url, params)
    if(countHit(result.json())>=10):
      break

  print("range：%d" % i)
  return result.json() 

#ヒット件数を求める函数．レスポンスがエラー時の処理も行う．
#引数　　　restInfo：ぐるなびAPIが返したレストラン情報
#return値 ヒット件数
def countHit(restInfo): 
  return restInfo.get('total_hit_count', 0)

#取得結果を表示する
#引数　　　restInfo：ぐるなびAPIが返したレストラン情報
#return値 void

def printFoodsInfo(restInfo):
  hitCnt=countHit(restInfo)
  Address=[],Name=[]
  for i in range(hitCnt):
    if i==4:
        break
    if(restInfo['rest'][i]['address']):
      Address.append(restInfo['rest'][i]['address'])
      Name.append(restInfo['rest'][i]['name'])
  return Address,Name

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

@handler.add(MessageAction,message=LocationAction)
def handle_location(event):
    global wanna_eat 
    lat=event.message.latitude
    lon=event.message.longitude
    
    questions=['たこ焼き','串カツ','お好み焼き','肉まん']
    items=[QuickReplyButton(action=PostbackAction(label=f"{question}",data=f"{question}")) for question in questions]
    orders=TextSendMessage(text="どれにする？",quick_reply=QuickReply(items=items))
    line_bot_api.reply_message(event.reply_token,messages=orders)
    
    data=getFoodsInfo(wanna_eat,lat,lon)
    Address,Name=printFoodsInfo(data)
    carousel_template = CarouselTemplate(columns=[
        CarouselColumn(text='場所：f{address}', title='f{name}', actions=[
            PostbackAction(label='ありがとう。', data='ありがとう。')
        ]) for place,name in zip(Address,Name)])
    template_message = TemplateSendMessage(
        alt_text='Carousel alt text', template=carousel_template)
    line_bot_api.push_message(event.source.user_id,template_message)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    questions=['お店','作り方','お土産','アメちゃん']
    if(event.message.text=='おばちゃーん'):
        items=[QuickReplyButton(action=PostbackAction(label=f"{question}",data=f"{question}")) for question in questions]
        orders=TextSendMessage(text="どないしたん？",quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token,messages=orders)

    elif(event.message.text=='リスト'):
         buttons_template = ButtonsTemplate(
            title='My buttons sample',text='Hello, my buttons',thumbnail_image_url="https://denx.jp/wp-content/uploads/2018/04/cropped-DENXバナー2-1-1.png",actions=[
                URIAction(label='ホームページ', uri='https://denx.jp')
            ])
         template_message = TemplateSendMessage(alt_text='DENXサイト', template=buttons_template)
         line_bot_api.reply_message(event.reply_token, template_message)

# 以下の handler は、改良してより短く記述すべき。
@handler.add(PostbackEvent)
def hander_postback(event):
    global wanna_eat

    text=event.postback.data
    if text=='アメちゃん':
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(
            original_content_url='https://1.bp.blogspot.com/-ZELov-QvHaU/UVWMfIiV3bI/AAAAAAAAPIM/xxWcxLdHrwk/s1600/candy.png',
            preview_image_url='https://1.bp.blogspot.com/-ZELov-QvHaU/UVWMfIiV3bI/AAAAAAAAPIM/xxWcxLdHrwk/s1600/candy.png'
        ))
    elif text=='お土産':
        survenier=ButtonsTemplate(
             text='お土産ならここやな', actions=[
                URIAction(label='お土産', uri='line://app/1598486025-lMb5nvo4'),
            ])
        line_bot_api.reply_message(event.reply_token,TemplateSendMessage(alt_text='お土産',template=survenier))
    elif text=='作り方':
        how_to_make=ButtonsTemplate(
             text='このホームページ通りにやったらできるで。\nしらんけど。', actions=[
                URIAction(label='作り方', uri='https://cookpad.com/'),
            ])
        line_bot_api.reply_message(event.reply_token,TemplateSendMessage(alt_text='作り方',template=how_to_make))
    
    elif text=='お店':
        #検索ボットを利用
        restaurant=ButtonsTemplate(
             text='今の場所から近いお店伝えるで。ええか？', actions=[
                LocationAction(label='お願い'),
            ])
        template_message=TemplateSendMessage(alt_text='位置情報送信しますか？',template=restaurant)
        line_bot_api.reply_message(event.reply_token,template_message)
        #データの取得方法を探す。
    elif text=='串カツ':
        wanna_eat='串カツ'
    elif text=='肉まん':
        wanna_eat='肉まん'
    elif text=='お好み焼き':
        wanna_eat='お好み焼き'
    elif text=='たこ焼き':
        wanna_eat='たこ焼き'
    elif text=='ありがとう':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='おおきに'))               

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)