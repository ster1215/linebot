# -*- coding: utf-8 -*-

# 載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
from datetime import datetime

from linebot.models import ButtonsTemplate, URIAction

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('Elcb3MWRQlkmjPXfemxIwokzayw967zWj8T+HJ18cH8ILmLzv8mGRR/AtCJegJbvXtAhlGcH+wlF3mhuf8S8c1GpvGkYDMkkrEQAh5sddChykuVXQ65FMYfrgV6mEpKS1NLszG9ES6jIdJY0N7tv9QdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('24920053ef16fd0f2f061a901242e764')

# 初始化推播訊息
def send_initial_message():
    try:
        current_time = datetime.now().strftime('%Y/%m/%d %H:%M')
        line_bot_api.push_message('U4506b76b7f2cbbf6b7807141df770a3c',TextSendMessage(text=f'您好，目前時間是 {current_time} ，請問需要什麼服務呢?'))
    except Exception as e:
        app.logger.error(f"Push message failed: {e}")

send_initial_message()

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'

# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()

    if user_message == "天氣":
        reply_message = TextSendMessage(text="請稍等，我幫您查詢天氣資訊！")
    elif re.match('告訴我秘密', user_message):
        reply_message = TextSendMessage(
            text='請點選您想去的國家',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="日本", text="Japan")),
                QuickReplyButton(action=MessageAction(label="台灣", text="Taiwan")),
                QuickReplyButton(action=MessageAction(label="新加坡", text="Singapore")),
                QuickReplyButton(action=MessageAction(label="韓國", text="Korea")),
                QuickReplyButton(action=MessageAction(label="中國", text="China")),
                QuickReplyButton(action=MessageAction(label="美國", text="US"))
            ])
        )
    elif user_message == "心情好":
        reply_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002734'  # 高興的貼圖
        )
    elif user_message == "心情不好":
        reply_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002735'  # 傷心的貼圖
        )
    elif user_message == "找學校":
        # 回傳餐廳的位置
        reply_message = LocationSendMessage(
            title='靜宜大學',
            address='433台中市沙鹿區台灣大道七段200號',
            latitude=24.2281419,  # 假設位置的緯度
            longitude=120.5801225  # 假設位置的經度
        )
    elif user_message == "找景點":
        # 回傳景點的位置
        reply_message = LocationSendMessage(
            title='主顧聖母堂',
            address='433台中市沙鹿區台灣大道七段200號',
            latitude=24.2281419,  # 假設位置的緯度
            longitude=120.5801225  # 假設位置的經度
        )
    elif user_message == "熱門音樂":
        # 回傳熱門音樂
        buttons_template = ButtonsTemplate(
        title='熱門音樂',
        text='點擊觀看熱門音樂！',
        actions=[
            URIAction(label='觀看 YouTube', uri='https://www.youtube.com/watch?v=K4DyBUG242c&ab_channel=NoCopyrightSounds')
        ]
        )
        reply_message = TemplateSendMessage(alt_text='熱門音樂', template=buttons_template)
    elif user_message == "放鬆音樂":
        # 回傳放鬆音樂
        buttons_template = ButtonsTemplate(
        title='放鬆音樂',
        text='點擊觀看放鬆音樂！',
        actions=[
            URIAction(label='觀看 YouTube', uri='https://www.youtube.com/watch?v=tcHJodG5hX8&ab_channel=NoCopyrightSounds')
        ]
    )
        reply_message = TemplateSendMessage(alt_text='放鬆音樂', template=buttons_template)
    elif user_message == "今天是我的生日":
        # 回傳生日祝福圖片
        reply_message = [
            ImageSendMessage(
                original_content_url='https://cdn.pixabay.com/photo/2024/01/26/15/32/birthday-8534158_1280.png',  # 替換為您要發送的生日祝福圖片的 URL
                preview_image_url='https://cdn.pixabay.com/photo/2024/01/26/15/32/birthday-8534158_1280.png'  # 生日圖片的預覽圖
            ),
            TextSendMessage(text="生日快樂！祝你有個美好的一年！🎉")
        ]
    else:
        reply_message = TextSendMessage(text="很抱歉，我目前無法理解這個內容。")
        
    line_bot_api.reply_message(event.reply_token, reply_message)


# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
