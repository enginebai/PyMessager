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


class TemplatePayload(Enum):
    GENERIC = 'generic'
    BUTTON = 'button'
    RECEIPT = 'receipt'


class ButtonType(Enum):
    WEB_URL = 'web_url'
    POSTBACK = 'postback'


class SendMessage:

    def __init__(self, recipient_id):
        super().__init__()
        self.receipient_type = Recipient.ID
        self.receipient_value = recipient_id

    @classmethod
    def init_send_by_phone(cls, phone):
        return cls(Recipient.PHONE_NUMBER, phone)

    def format_recipient(self):
        return {(Recipient.ID.value
                 if self.receipient_type == Recipient.ID
                 else Recipient.PHONE_NUMBER.value): self.receipient_value
                }

    def send_text(self, text):
        return {RECIPIENT_FIELD: self.format_recipient(),
                MESSAGE_FIELD: {MessageType.TEXT.value: text}}

    def send_image(self, image):
        return {RECIPIENT_FIELD: self.format_recipient(),
                MESSAGE_FIELD: {
                    ATTACHMENT_FIELD: {
                        TYPE_FIELD: AttachmentType.IMAGE.value,
                        PAYLOAD_FIELD: {
                            URL_FIELD: image
                        }
                    }
                }}


def send_message(message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={token}'.format(token=config.FB_TOKEN)
    response_message = json.dumps(message)
    req = requests.post(post_message_url,
                        headers={"Content-Type": "application/json"},
                        data=response_message)
    print("[{status}] Reply to {recipient}: {content}".format(
        status=req.status_code, recipient=message[RECIPIENT_FIELD], content=message[MESSAGE_FIELD]))