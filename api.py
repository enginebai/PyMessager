#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request

__author__ = 'enginebai'

API_ROOT = 'api/'
FB_WEBHOOK = 'fb_webhook'

app = Flask(__name__)


@app.route(API_ROOT + FB_WEBHOOK, methods=["GET"])
def fb_webhook():
    verification_code = 'I_AM_VERIFICIATION_CODE'
    verify_token = request.args.get('hub.verify_token')
    if verification_code == verify_token:
        return request.args.get('hub.challenge')
