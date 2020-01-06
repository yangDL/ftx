# -*- coding: utf-8 -*-

import os

ABS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADB_PATH = os.path.join(ABS_PATH, 'Tools', 'adb.exe')
CONFIG_PATH = os.path.join(ABS_PATH, 'config')

DEVICE_ADDR = '127.0.0.1:7555' # MUMU virtual box

COMPONENTS = {
    "点击": "tap", 
    "滑动": "swipe", 
    "输入文字": "input",
    "输入账号": "username",
    "输入密码": "password"
}

STEPS = {
    "登录": "login", 
    "账号退出": "logout", 
    "发帖": "send"
}