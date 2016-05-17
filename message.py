#!/usr/bin/python
# -*- coding: utf8 -*-
import json
from enum import Enum

import requests
import config

__author__ = 'enginebai'

RECIPIENT_FIELD = 'recipient'
MESSAGE_FIELD = 'message'
ATTACHMENT_FIELD = 'attachment'
TYPE_FIELD = 'type'
TEMPLATE_TYPE_FIELD = 'template_type'
TEXT_FIELD = 'text'
TITLE_FIELD = 'title'
SUBTITLE_FIELD = 'subtitle'
BUTTONS_FIELD = 'buttons'
PAYLOAD_FIELD = 'payload'
URL_FIELD = 'url'


class Recipient(Enum):
    PHONE_NUMBER = 'phone_number'
    ID = 'id'


class MessageType(Enum):
    TEXT = 'text'
    ATTACHMENT = 'attachment'


class AttachmentType(Enum):
    IMAGE = 'image'
    TEMPLATE = 'template'


class TemplateType(Enum):
    GENERIC = 'generic'
    BUTTON = 'button'
    RECEIPT = 'receipt'


class ButtonType(Enum):
    WEB_URL = 'web_url'
    POSTBACK = 'postback'


class ActionButton:
    def __init__(self, button_type, title, url=None, payload=None):
        super().__init__()
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


class SendMessage:
    def __init__(self, recipient_id):
        super().__init__()
        self.receipient_type = Recipient.ID
        self.receipient_value = recipient_id
        self.message_data = None

    @classmethod
    def init_send_by_phone(cls, phone):
        return cls(Recipient.PHONE_NUMBER, phone)

    def build_recipient(self):
        return {(Recipient.ID.value
                 if self.receipient_type == Recipient.ID
                 else Recipient.PHONE_NUMBER.value): self.receipient_value
                }

    def build_text_message(self, text):
        self.message_data = {RECIPIENT_FIELD: self.build_recipient(),
                             MESSAGE_FIELD: {MessageType.TEXT.value: text}}

    def build_image_message(self, image):
        self.message_data = {RECIPIENT_FIELD: self.build_recipient(),
                             MESSAGE_FIELD: {
                                 ATTACHMENT_FIELD: {
                                     TYPE_FIELD: AttachmentType.IMAGE.value,
                                     PAYLOAD_FIELD: {
                                         URL_FIELD: image
                                     }
                                 }
                             }}

    def build_buttons_message(self, title, button_list):
        buttons = list(dict())
        for i in range(len(button_list)):
            buttons.append(button_list[i].to_dict())

        self.message_data = {RECIPIENT_FIELD: self.build_recipient(),
                             MESSAGE_FIELD: {
                                 ATTACHMENT_FIELD: {
                                     TYPE_FIELD: AttachmentType.TEMPLATE.value,
                                     PAYLOAD_FIELD: {
                                         TEMPLATE_TYPE_FIELD: TemplateType.BUTTON.value,
                                         TEXT_FIELD: title,
                                         BUTTONS_FIELD: buttons
                                     }
                                 }
                             }}

    def send_message(self):
        post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={token}'.format(
            token=config.FB_TOKEN)
        response_message = json.dumps(self.message_data)
        # print(response_message)
        req = requests.post(post_message_url,
                            headers={"Content-Type": "application/json"},
                            data=response_message)
        print("[{status}] Reply to {recipient}: {content}".format(
            status=req.status_code,
            recipient=self.message_data[RECIPIENT_FIELD],
            content=self.message_data[MESSAGE_FIELD]))
