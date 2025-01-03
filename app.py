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
from linebot.models import ImagemapSendMessage, ImagemapArea

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
    elif user_message == "推薦餐廳":
    # 設置 Imagemap 圖片的背景圖片和尺寸
        imagemap_message = ImagemapSendMessage(
        base_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSfFL8eu5sGhg-oIFeV0oxCYN3mBjwJXvClQ&s',  # 替換成您的圖片 URL
        alt_text='推薦餐廳',
        base_size={'width': 1040, 'height': 1040},  # 圖片的尺寸
        actions=[
            # 日式料理區域
            ImagemapArea(
                x=0, y=0, width=520, height=520,
                action=URIAction(uri='https://www.google.com/maps/place/%E7%84%BC%E8%82%89%E3%82%B9%E3%83%9E%E3%82%A4%E3%83%AB%EF%BC%88%E7%87%92%E8%82%89Smile%EF%BC%89+%E5%8F%B0%E4%B8%AD%E6%B2%99%E9%B9%BF%E5%BA%97/@24.2270639,120.55503,3066m/data=!3m1!1e3!4m10!1m2!2m1!1z6Z2c5a6c5aSn5a246ZmE6L-R55qE5pel5byP6aSQ5buz!3m6!1s0x3469150008947725:0xf0ce0689f53ec07f!8m2!3d24.2270639!4d120.5732944!15sCiHpnZzlrpzlpKflrbjpmYTov5HnmoTml6XlvI_ppJDlu7NaKiIo6Z2cIOWunCDlpKflrbgg6ZmE6L-RIOeahCDml6Ug5byPIOmkkOW7s5IBE3lha2luaWt1X3Jlc3RhdXJhbnTgAQA!16s%2Fg%2F11smn96vdv?entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D')  # 替換成日式餐廳的 URL
            ),
            # 西式料理區域
            ImagemapArea(
                x=520, y=0, width=520, height=520,
                action=URIAction(uri='https://www.google.com/maps/place/%E5%B8%83%E6%B4%9B%E6%80%9D%E5%BB%9APURO+taverna/@24.2271008,120.55503,3066m/data=!3m1!1e3!4m16!1m8!2m7!1z6Z2c5a6c5aSn5a246ZmE6L-R55qE6KW_5byP6aSQ5buz!3m5!2z6Z2c5a6c5aSn5a24!3s0x346915ab3fd07acf:0x8bea4967097a54a3!4m2!1d120.5771913!2d24.2258027!3m6!1s0x346914f07cd2ac11:0x421eeb129436037c!8m2!3d24.2306584!4d120.5651496!15sCiHpnZzlrpzlpKflrbjpmYTov5HnmoTopb_lvI_ppJDlu7NaKSIn6Z2cIOWunCDlpKflrbgg6ZmE6L-RIOeahCDopb_lvI8g6aSQ5buzkgESaXRhbGlhbl9yZXN0YXVyYW50mgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVVJYZGpWVU9VVm5FQUXgAQD6AQQIABAb!16s%2Fg%2F11b6z2k_t8?entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D')  # 替換成西式餐廳的 URL
            ),
            # 中式料理區域
            ImagemapArea(
                x=0, y=520, width=520, height=520,
                action=URIAction(uri='https://www.google.com/maps/place/%E9%A6%99%E6%B8%AF%E4%B9%9D%E9%BE%8D%E5%9F%8E%E5%B0%8F%E5%90%83%E5%BA%97/@24.2271377,120.55503,3066m/data=!3m1!1e3!4m16!1m8!2m7!1z6Z2c5a6c5aSn5a246ZmE6L-R55qE5Lit5byP6aSQ5buz!3m5!2z6Z2c5a6c5aSn5a24!3s0x346915ab3fd07acf:0x8bea4967097a54a3!4m2!1d120.5771913!2d24.2258027!3m6!1s0x346915aa99db7be5:0x5b7f8df2489c80f6!8m2!3d24.2279181!4d120.5746839!15sCiHpnZzlrpzlpKflrbjpmYTov5HnmoTkuK3lvI_ppJDlu7NaKSIn6Z2cIOWunCDlpKflrbgg6ZmE6L-RIOeahCDkuK3lvI8g6aSQ5buzkgEKcmVzdGF1cmFudOABAA!16s%2Fg%2F11dyww1c4c?entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D')  # 替換成中式餐廳的 URL
            ),
            # 法式料理區域
            ImagemapArea(
                x=520, y=520, width=520, height=520,
                action=URIAction(uri='https://www.google.com/maps/place/%E5%82%91%E7%90%86%E6%AD%90%E6%B3%95%E5%B0%8F%E9%A4%A8+since2004+%EF%BD%9C%E7%87%9F%E6%A5%AD%E4%B8%AD%E4%B8%8D%E6%96%B9%E4%BE%BF%E6%8E%A5%E8%81%BD%E9%9B%BB%E8%A9%B1%EF%BD%9C%E4%B8%8D%E6%98%AF%E8%A6%AA%E5%AD%90%E9%A4%90%E5%BB%B3%EF%BD%9C%E8%AB%8B%E5%96%84%E7%94%A8LINE%E5%92%8C%E7%B7%9A%E4%B8%8A%E9%A0%90%E7%B4%84%E7%B3%BB%E7%B5%B1%EF%BD%9C/@24.2271745,120.55503,3066m/data=!3m1!1e3!4m16!1m8!2m7!1z6Z2c5a6c5aSn5a246ZmE6L-R55qE5rOV5byP6aSQ5buz!3m5!2z6Z2c5a6c5aSn5a24!3s0x346915ab3fd07acf:0x8bea4967097a54a3!4m2!1d120.5771913!2d24.2258027!3m6!1s0x346915024217940d:0x8f3754b8a7965660!8m2!3d24.2299891!4d120.5663022!15sCiHpnZzlrpzlpKflrbjpmYTov5HnmoTms5XlvI_ppJDlu7NaKSIn6Z2cIOWunCDlpKflrbgg6ZmE6L-RIOeahCDms5XlvI8g6aSQ5buzkgEWY29udGluZW50YWxfcmVzdGF1cmFudOABAA!16s%2Fg%2F1tp8xshm?entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D')  # 替換成法式餐廳的 URL
            ),
        ]
        )
        reply_message = imagemap_message
    elif user_message == "推薦景點":
        # 設計 Carousel Template 顯示多個旅遊景點選項
        carousel_template = CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcQwcDKJPxHa0Ou3h56OMsfuCYROOGaw_2gOwPnvKMNgr80rwxV5VEvg30QbuWt_lwhJ0d6KWCp0Bd52pwnowLdSudRRkGWDCdeV68cd7A",  # 替換為景點的圖片 URL
                    title="景點1：日月潭",
                    text="點擊查看詳細資訊",
                    actions=[
                        URIAction(label="查看詳情", uri="https://www.sunmoonlake.gov.tw/zh-tw")  # 替換為景點的網站或導覽鏈接
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcRkApR-XG_Io16YNO2OeWK1hmZtv8FpgBkQr6HxD1NfSjfBFyxvwcDg0hCmGfT8Zk8_ROckhsw26LtUX0WyW1pRDKYMtjNRV8nzh2vNyQ",  # 替換為景點的圖片 URL
                    title="景點2：阿里山",
                    text="點擊查看詳細資訊",
                    actions=[
                        URIAction(label="查看詳情", uri="https://www.ali-nsa.net/")  # 替換為景點的網站或導覽鏈接
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://image-tc.galaxy.tf/wijpeg-19za0ro24q24b9b9ez8lz2e9x/taipei-101.jpg",  # 替換為景點的圖片 URL
                    title="景點3：台北101",
                    text="點擊查看詳細資訊",
                    actions=[
                        URIAction(label="查看詳情", uri="https://www.taipei-101.com.tw/tw/")  # 替換為景點的網站或導覽鏈接
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://lh3.googleusercontent.com/p/AF1QipOMMZ603bHExjiEb1abciOs9q4WeatKtakynx8o=s1360-w1360-h1020",  # 替換為景點的圖片 URL
                    title="景點4：墾丁",
                    text="點擊查看詳細資訊",
                    actions=[
                        URIAction(label="查看詳情", uri="https://www.ktnp.gov.tw/")  # 替換為景點的網站或導覽鏈接
                    ]
                )
            ]
        )

        reply_message = TemplateSendMessage(
            alt_text="推薦景點",
            template=carousel_template
        )

    else:
        reply_message = TextSendMessage(text="很抱歉，我目前無法理解這個內容。")
        
    line_bot_api.reply_message(event.reply_token, reply_message)


# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
