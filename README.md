# Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

# はじめに
LINEが公開しているpython用SDKの全ての機能を実装します。

https://github.com/line/line-bot-sdk-python

# API
## LineBotApi
- \_\_init\_\_
- reply_message
- push_message
- multicast
- get_profile
- get_group_member_profile
- get_room_member_profile
- get_group_member_ids
- get_room_member_ids
- get_message_content
- leave_group
- leave_room
- get_rich_menu
- create_rich_menu
- delete_rich_menu
- get_rich_menu_id_of_user
- link_rich_menu_to_user
- unlink_rich_menu_from_user
- get_rich_menu_image
- set_rich_menu_image
- get_rich_menu_list

## Error handling
- LineBotApiError

## Message objects
- TextSendMessage
- ImageSendMessage
- VideoSendMessage
- AudioSendMessage
- LocationSendMessage
- StickerSendMessage
- ImagemapSendMessage
- TemplateSendMessage
  - ButtonsTemplate
  - ConfirmTemplate
  - CarouselTemplate
  - ImageCarouselTemplate

# Webhook
## WebhookParser
- \_\_init\_\_
- parse

## WebhookHandler
- \_\_init\_\_
- handle
- add

## Webhook event object
- Event
  - MessageEvent
  - FollowEvent
  - UnfollowEvent
  - JoinEvent
  - LeaveEvent
  - PostbackEvent
  - BeaconEvent
- Source
  - SourceUser
  - SourceGroup
  - SourceRoom
- Message
  - TextMessage
  - ImageMessage
  - VideoMessage
  - AudioMessage
  - LocationMessage
  - StickerMessage
  - FileMessage
