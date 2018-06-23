import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError,
)
from linebot.models import *

app = Flask(__name__)

# 環境変数読み込み
line_channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
line_channel_secret = os.environ['LINE_CHANNEL_SECRET']

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)


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

def is_connection_check(event):
    check_uid = 'Udeadbeefdeadbeefdeadbeefdeadbeef'
    check_tokens = [
        '00000000000000000000000000000000',
        'ffffffffffffffffffffffffffffffff',
    ]
    if event.source.type == 'user':
        if event.source.user_id == check_uid:
            return True
    if event.reply_token in check_tokens:
        return True
    return False

@handler.default()
def default(event):
    print(event)
    # line_bot_api.reply_message(event.reply_token, text=event)

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if is_connection_check(event):
        return

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    print(event)
    # line_bot_api.reply_message(event.reply_token, text=event)

@handler.add(MessageEvent, message=VideoMessage)
def handle_video_message(event):
    print(event)
    # line_bot_api.reply_message(event.reply_token, text=event)

@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    print(event)
    # line_bot_api.reply_message(event.reply_token, text=event)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    print(event)
    # line_bot_api.reply_message(event.reply_token, text=event)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    if is_connection_check(event):
        return
    print(event)
    # line_bot_api.reply_message(event.reply_token, text=event)

@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    print(event)
    # line_bot_api.reply_message(event.reply_token, text=event)

@handler.add(FollowEvent)
def handle_follow_event(event):
    print(event)
    
    profile = line_bot_api.get_profile(event.source.user_id)

    print(profile.display_name)
    print(profile.user_id)
    print(profile.picture_url)
    print(profile.status_message)

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text='Welcome'))
    # reply_msgs.append(TextSendMessage(text=str(event)))
    reply_msgs.append(TextSendMessage(text=profile.display_name))
    reply_msgs.append(TextSendMessage(text=profile.user_id))
    if profile.picture_url:
        reply_msgs.append(TextSendMessage(text=profile.picture_url))
    if profile.status_message:
        reply_msgs.append(TextSendMessage(text=profile.status_message))

    line_bot_api.reply_message(event.reply_token, reply_msgs)

@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    print(event)

def get_member_profile(event, uid):
    if event.source.type == 'group':
        gid = event.source.group_id
        return line_bot_api.get_group_member_profile(gid, uid)
    if event.source.type == 'room':
        rid = event.source.room_id
        return line_bot_api.get_room_member_profile(rid, uid)

def get_member_ids(event):
    if event.source.type == 'group':
        gid = event.source.group_id
        return line_bot_api.get_group_member_ids(gid)
    if event.source.type == 'room':
        rid = event.source.room_id
        return line_bot_api.get_room_member_ids(rid)

@handler.add(JoinEvent)
def handle_join_event(event):
    print(event)
    # line_bot_api.reply_message(event.reply_token, text=event)

    uids = get_member_ids(event)
    

@handler.add(LeaveEvent)
def handle_leave_event(event):
    print(event)

@handler.add(PostbackEvent)
def handle_postback_event(event):
    print(event)
    # line_bot_api.reply_message(event.reply_token, text=event)

@handler.add(BeaconEvent)
def handle_beacon_event(event):
    print(event)
    # line_bot_api.reply_message(event.reply_token, text=event)


if __name__ == "__main__":
    app.run()
