#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from setuptools import setup

__author__ = "Engine Bai"

setup(
    name="PyMessager",
    version="1.0.1",
    packages=["pymessager", ],
    license='The MIT License (MIT) Copyright © 2017 Engine Bai.',
    description="A Python SDK and Flask API to develop Facebook Messenger application",
    long_description=open("README.md", "r").read(),
    author="Engine Bai",
    author_email="enginebai@gmail.com",
    url="https://github.com/enginebai/PyMessager",
    install_requires=[
        "requests"
    ],
)
