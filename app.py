#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by BIGMAO
# Date：2016-10-15
# Time: 21:43

from flask import Flask
import time
app = Flask(__name__)

@app.route('/')
def index():
    time.sleep(10)
    return "Hello World!"

if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0", "80")