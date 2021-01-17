"""
Object detection and image description on LINE bot
"""
from datetime import datetime, timezone, timedelta
import os
import re
import json
import requests
from flask import Flask, request, abort
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FlexSendMessage,
    ImageMessage,
)
from imgur_python import Imgur
from PIL import Image, ImageDraw, ImageFont
import time


LINE_SECRET = "339c696e22382f31a3a90bd8779034fe"
LINE_TOKEN = "kxKojuWYAbWG8CaGxCB/bQVj4F/LRQJoAZn0BILkiUdUAk82DtBrU4oTpLmW21iZRwNwXgmf6aQKiJWW06PquDqJhrYlcLGUr9JocLs1sBbaZ+MfotCnuKexBJZNtxhaZM1JHDIlmJXt7wXAvvWc9QdB04t89/1O/w1cDnyilFU="
LINE_BOT = LineBotApi(LINE_TOKEN)
HANDLER = WebhookHandler(LINE_SECRET)

app = Flask(__name__)

@app.route("/")
def hello():
    "hello world"
    return "Hello World!!!!!"

@app.route("/callback", methods=["POST"])
def callback():
    # X-Line-Signature: 數位簽章
    signature = request.headers["X-Line-Signature"]
    print(signature)
    body = request.get_data(as_text=True)
    print(body)
    try:
        HANDLER.handle(body, signature)
    except InvalidSignatureError:
        print("Check the channel secret/access token.")
        abort(400)
    return "OK"

#@HANDLER.add(MessageEvent, message=TextMessage)
#def handle_message(event):
#    url_dict = {
#      "TIBAME":"https://www.tibame.com/coursegoodjob/traffic_cli",
#     "HELP":"https://developers.line.biz/zh-hant/docs/messaging-api/"}
# 將要發出去的文字變成TextSendMessage
#    try:
#        url = url_dict[event.message.text.upper()]
#        message = TextSendMessage(text=url)
#    except:
#        message = TextSendMessage(text=event.message.text)
# 回覆訊息
#    LINE_BOT.reply_message(event.reply_token, message)
  
@HANDLER.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    Reply text message
    """
    json_file = {"TIBAME": "templates/detect_result.json", "HELP": "templates/carousel.json"}
    try:
        filename = json_file[event.message.text.upper()]
        with open(filename, "r") as f_r:
            bubble = json.load(f_r)
        f_r.close()
        LINE_BOT.reply_message(
            event.reply_token,
            [FlexSendMessage(alt_text="Information", contents=bubble)],
        )
    except:
        message = TextSendMessage(text=event.message.text)
        LINE_BOT.reply_message(event.reply_token, message)   
    
    
 
