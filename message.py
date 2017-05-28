#!/usr/bin/python
# -*- coding: utf8 -*-
import json
from enum import Enum

import requests
import config

__author__ = "enginebai"

# send message fields
RECIPIENT_FIELD = "recipient"
MESSAGE_FIELD = "message"
ATTACHMENT_FIELD = "attachment"
TYPE_FIELD = "type"
TEMPLATE_TYPE_FIELD = "template_type"
TEXT_FIELD = "text"
TITLE_FIELD = "title"
SUBTITLE_FIELD = "subtitle"
IMAGE_FIELD = "image_url"
BUTTONS_FIELD = "buttons"
PAYLOAD_FIELD = "payload"
URL_FIELD = "url"
ELEMENTS_FIELD = "elements"
QUICK_REPLIES_FIELD = "quick_replies"
CONTENT_TYPE_FIELD = "content_type"

# received message fields
POSTBACK_FIELD = "postback"


class Recipient(Enum):
    PHONE_NUMBER = "phone_number"
    ID = "id"


class MessageType(Enum):
    TEXT = "text"
    ATTACHMENT = "attachment"


class AttachmentType(Enum):
    IMAGE = "image"
    TEMPLATE = "template"


class TemplateType(Enum):
    GENERIC = "generic"
    BUTTON = "button"
    RECEIPT = "receipt"


class ButtonType(Enum):
    WEB_URL = "web_url"
    POSTBACK = "postback"


class ContentType(Enum):
    TEXT = "text"
    LOCATION = "location"


class ActionButton:
    def __init__(self, button_type, title, url=None, payload=None):
        self.button_type = button_type
        self.title = title
        self.url = url
        self.payload = payload

    def to_dict(self):
        button_dict = dict()
        button_dict[TYPE_FIELD] = self.button_type.value
        button_dict[TITLE_FIELD] = self.title
        if self.url is not None:
            button_dict[URL_FIELD] = self.url
        if self.payload is not None:
            button_dict[PAYLOAD_FIELD] = self.payload
        return button_dict


class GenericElement:
    def __init__(self, title, subtitle, image_url, buttons):
        self.title = title
        self.subtitle = subtitle
        self.image_url = image_url
        self.buttons = buttons

    def to_dict(self):
        element_dict = dict()
        element_dict[TITLE_FIELD] = self.title
        element_dict[SUBTITLE_FIELD] = self.subtitle
        element_dict[IMAGE_FIELD] = self.image_url
        buttons = list(dict())
        for i in range(len(self.buttons)):
            buttons.append(self.buttons[i].to_dict())
        element_dict[BUTTONS_FIELD] = buttons
        return element_dict


class QuickReply:
    def __init__(self, title, payload, image_url=None, content_type=ContentType.TEXT):
        self.title = title
        self.payload = payload
        self.image_url = image_url
        self.content_type = content_type

    def to_dict(self):
        reply_dict = dict()
        reply_dict[CONTENT_TYPE_FIELD] = self.content_type.value
        reply_dict[TITLE_FIELD] = self.title
        reply_dict[PAYLOAD_FIELD] = self.payload
        if self.image_url is not None:
            reply_dict[IMAGE_FIELD] = self.image_url
        print(reply_dict)
        return reply_dict


class Messager(object):
    def __init__(self, access_token):
        self.access_token = access_token

    def subscribe_to_page(self):
        return requests.post("https://graph.facebook.com/v2.9/me/subscribed_apps?access_token={token}"
                             .format(token=self.access_token))

    def set_greeting_text(self, text):
        data = {"setting_type": "greeting", "greeting": {"text": text}}
        return requests.post("https://graph.facebook.com/v2.6/me/thread_settings?access_token={token}"
                             .format(token=self.access_token), headers={"Content-Type": "application/json"},
                             data=data)

    def set_get_started_button_payload(self, payload):
        data = {"setting_type": "call_to_actions", "thread_state": "new_thread",
                "call_to_actions": [{"payload": payload}]}
        return requests.post("https://graph.facebook.com/v2.6/me/thread_settings?access_token={token}"
                             .format(token=self.access_token), headers={"Content-Type": "application/json"},
                             data=data)

    def send_text(self, user_id, text):
        self._send({RECIPIENT_FIELD: self._build_recipient(user_id),
                    MESSAGE_FIELD: {MessageType.TEXT.value: text}})

    def send_image(self, user_id, image):
        self._send({RECIPIENT_FIELD: self._build_recipient(user_id),
                    MESSAGE_FIELD: {
                        ATTACHMENT_FIELD: {
                            TYPE_FIELD: AttachmentType.IMAGE.value,
                            PAYLOAD_FIELD: {
                                URL_FIELD: image
                            }
                        }
                    }})

    def send_buttons(self, user_id, title, button_list):
        buttons = list(dict())
        for i in range(len(button_list)):
            buttons.append(button_list[i].to_dict())

        self._send({RECIPIENT_FIELD: self._build_recipient(user_id),
                    MESSAGE_FIELD: {
                        ATTACHMENT_FIELD: {
                            TYPE_FIELD: AttachmentType.TEMPLATE.value,
                            PAYLOAD_FIELD: {
                                TEMPLATE_TYPE_FIELD: TemplateType.BUTTON.value,
                                TEXT_FIELD: title,
                                BUTTONS_FIELD: buttons
                            }
                        }
                    }})

    def send_generic(self, user_id, element_list):
        elements = list(dict())
        for i in range(len(element_list)):
            elements.append(element_list[i].to_dict())
        self._send({RECIPIENT_FIELD: self._build_recipient(user_id),
                    MESSAGE_FIELD: {
                        ATTACHMENT_FIELD: {
                            TYPE_FIELD: AttachmentType.TEMPLATE.value,
                            PAYLOAD_FIELD: {
                                TEMPLATE_TYPE_FIELD: TemplateType.GENERIC.value,
                                ELEMENTS_FIELD: elements
                            }
                        }
                    }})

    def send_quick_replies(self, user_id, title, reply_list):
        replies = list(dict())
        for r in reply_list:
            replies.append(r.to_dict())
        self._send({RECIPIENT_FIELD: self._build_recipient(user_id),
                    MESSAGE_FIELD: {
                        TEXT_FIELD: title,
                        QUICK_REPLIES_FIELD: replies
                    }})

    @staticmethod
    def _build_recipient(user_id):
        return {Recipient.ID.value: user_id}

    def _send(self, message_data):
        post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token={token}".format(
            token=self.access_token)
        response_message = json.dumps(message_data)
        print(response_message)
        req = requests.post(post_message_url,
                            headers={"Content-Type": "application/json"},
                            data=response_message)
        print("[{status}/{reason}/{text}] Reply to {recipient}: {content}".format(
            status=req.status_code,
            reason=req.reason,
            text=req.text,
            recipient=message_data[RECIPIENT_FIELD],
            content=message_data[MESSAGE_FIELD]))
        pass
