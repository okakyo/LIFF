from flask import Flask, request, abort,render_template
import requests 

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

line_bot_api = LineBotApi('5BVERrVLauQDqd89tFyf4Nz+/guwGgCpPXT52/LHjFYVsZBXs/BRKd6ZqiGcn+13/fXmJqWgqtYlBWP7Qw+2ltzfAyHIj1XnDLTIyUEXyG4+3wX/vN5NsoLVpPFYkY1r6Y5qj9zGcv7wvWZhAZXpqVGUYhWQfeY8sLGRXgo3xvw=')
handler = WebhookHandler('fa813b2f660166081a7f2e14f9292542')

@app.route('/')
def index():
    return render_template('Hello World!')
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()