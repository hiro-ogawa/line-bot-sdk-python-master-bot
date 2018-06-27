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
debug = os.environ.get('DEBUG', 'False') == 'True'

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

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text='Not impremented'))
    reply_msgs.append(TextSendMessage(text=str(event)))
    line_bot_api.reply_message(event.reply_token, reply_msgs)

def get_user_info_string_list(uid):
    l = []
    p = line_bot_api.get_profile(uid)
    l.append('profile:')
    l.append('display_name: {}'.format(p.display_name))
    l.append('user_id: {}'.format(p.user_id))
    if p.picture_url:
        l.append('picture_url: {}'.format(p.picture_url))
    if p.status_message:
        l.append('status_message: {}'.format(p.status_message))
    return l

def get_source_string(s):
    l = []
    l.append('source:')
    l.append('type: {}'.format(s.type))
    if s.type == 'group':
        l.append('group_id: {}'.format(s.group_id))
    elif s.type == 'room':
        l.append('room_id: {}'.format(s.room_id))
    l.append('user_info:')
    l.extend(get_user_info_string_list(s.user_id))

    ret = '\n'.join(l)
    return ret

def get_message_string(m):
    l = []
    l.append('message:')
    l.append('type: {}'.format(m.type))
    l.append('id: {}'.format(m.id))
    if m.type == 'text':
        l.append('text: {}'.format(m.text))
    if m.type == 'location':
        l.append('title: {}'.format(m.title))
        l.append('address: {}'.format(m.address))
        l.append('latitude: {}'.format(m.latitude))
        l.append('longitude: {}'.format(m.longitude))
    if m.type == 'sticker':
        l.append('package_id: {}'.format(m.package_id))
        l.append('sticker_id: {}'.format(m.sticker_id))
    if m.type == 'file':
        l.append('file_size: {}'.format(m.file_size))
        l.append('file_name: {}'.format(m.file_name))

    ret = '\n'.join(l)
    return ret

def get_message_event_string(e):
    l = [
        'type: {}'.format(e.type),
        'timestamp: {}'.format(e.timestamp),
        get_source_string(e.source),
        'reply_token: {}'.format(e.reply_token),
        get_message_string(e.message),
    ]
    ret = '\n'.join(l)
    return ret

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if is_connection_check(event):
        return

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text=get_message_event_string(event)))
    line_bot_api.reply_message(event.reply_token, reply_msgs)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    print(event)

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text=get_message_event_string(event)))
    line_bot_api.reply_message(event.reply_token, reply_msgs)

@handler.add(MessageEvent, message=VideoMessage)
def handle_video_message(event):
    print(event)

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text=get_message_event_string(event)))
    line_bot_api.reply_message(event.reply_token, reply_msgs)

@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    print(event)

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text=get_message_event_string(event)))
    line_bot_api.reply_message(event.reply_token, reply_msgs)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    print(event)

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text=get_message_event_string(event)))
    line_bot_api.reply_message(event.reply_token, reply_msgs)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    if is_connection_check(event):
        return
    print(event)

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text=get_message_event_string(event)))
    line_bot_api.reply_message(event.reply_token, reply_msgs)

@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    print(event)

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text=get_message_event_string(event)))
    line_bot_api.reply_message(event.reply_token, reply_msgs)

@handler.add(FollowEvent)
def handle_follow_event(event):
    print(event)

    l = [
        'type: {}'.format(event.type),
        'timestamp: {}'.format(event.timestamp),
        get_source_string(event.source),
        'reply_token: {}'.format(event.reply_token),
    ]
    msg = '\n'.join(l)

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text=msg))

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
    # 認証済アカウントである必要あり
    try:
        if event.source.type == 'group':
            gid = event.source.group_id
            return line_bot_api.get_group_member_ids(gid)
        if event.source.type == 'room':
            rid = event.source.room_id
            return line_bot_api.get_room_member_ids(rid)
    except LineBotApiError as e:
        print(e.status_code)
        print(e.error.message)
        print(e.error.details)
        return []

@handler.add(JoinEvent)
def handle_join_event(event):
    print(event)

    l = [
        'type: {}'.format(event.type),
        'timestamp: {}'.format(event.timestamp),
        get_source_string(event.source),
        'reply_token: {}'.format(event.reply_token),
    ]
    msg = '\n'.join(l)

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text=msg))

    line_bot_api.reply_message(event.reply_token, reply_msgs)

@handler.add(LeaveEvent)
def handle_leave_event(event):
    print(event)

@handler.add(PostbackEvent)
def handle_postback_event(event):
    print(event)

    l = [
        'type: {}'.format(event.type),
        'timestamp: {}'.format(event.timestamp),
        get_source_string(event.source),
        'reply_token: {}'.format(event.reply_token),
        'postback:',
        'postback.data: {}'.format(event.postback.data),
        'postback.params: {}'.format(event.postback.params),
    ]
    msg = '\n'.join(l)

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text=msg))

@handler.add(BeaconEvent)
def handle_beacon_event(event):
    print(event)

    l = [
        'type: {}'.format(event.type),
        'timestamp: {}'.format(event.timestamp),
        get_source_string(event.source),
        'reply_token: {}'.format(event.reply_token),
        'beacon:',
        'beacon.type: {}'.format(event.beacon.type),
        'beacon.hwid: {}'.format(event.beacon.hwid),
        'beacon.device_message: {}'.format(event.beacon.device_message),
    ]
    msg = '\n'.join(l)

    reply_msgs = []
    reply_msgs.append(TextSendMessage(text=msg))


if __name__ == "__main__":
    app.run(debug=debug)
