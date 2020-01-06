# -*- coding: utf-8 -*-

import os
import sys
import logging

from common.adb import ADB
from common.constant import DEVICE_ADDR

log = logging.getLogger('FTX.test')

def dump_device_info():
    """
    显示设备信息
    """
    adb = ADB()
    if not adb.is_device_ok():
        adb.connect_devices(DEVICE_ADDR)
        if not adb.is_device_ok():
            sys.exit(1)
    screen = adb.get_screen()
    log.info("********************")
    log.info("Screen: %s", screen)
    log.info("Density: %s", adb.test_density())
    log.info("Device: %s", adb.test_device_detail())
    log.info("Phone OS: %s", adb.test_device_os())
    log.info("Host OS: %s", sys.platform)
    log.info("Python: %s", sys.version.split()[0])
    log.info("********************")
    return screen
