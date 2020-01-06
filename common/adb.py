# -*- coding: utf-8 -*-
import os
import logging
import threading
import subprocess
from common import constant

log = logging.getLogger('FTX.adb')


class Singleton(object):
    
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if hasattr(cls, '_instance'):
                return cls._instance
            cls._instance = super().__new__(cls, *args, **kwargs)
            return cls._instance

class ADB(Singleton):

    def __init__(self):
        try:
            subprocess.Popen([constant.ADB_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.adb_path = constant.ADB_PATH
        except OSError:
            log.error("%s not found?", constant.ADB_PATH)
            log.error('请安装 ADB 及驱动并配置环境变量')
            exit(1)

    def run(self, args):
        if args[0] != self.adb_path:
            args = [self.adb_path] + args
        args = [str(arg) for arg in args]
        try:
            process = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
            info, err = process.communicate(timeout=30)
            ret = process.returncode
        except Exception as ex:
            log.exception(str(ex))
            return str(ex)
        if ret != 0:
            if err:
                return err.decode('utf-8')
            return ""
        return info.decode('utf-8').strip()

    def is_device_ok(self):
        log.info('检查设备是否连接...')
        args = [self.adb_path, 'devices']
        info = self.run(args).split('\n')
        if not info[0].lower().startswith('list of devices attached') or not info[1:]:
            log.error('未找到设备')
            log.info("\n".join(info))
            return False
        log.info("%s is connected", info[1].split()[0])
        return True

    def connect_devices(self, device):
        log.info('尝试连接设备...')
        args = [self.adb_path, 'connect', device]
        log.info(self.run(args))
        return

    def get_screen(self):
        cmd = ['shell', 'wm', 'size']
        output = self.run(cmd)
        return output.split(':')[-1].strip()

    def test_density(self):
        cmd = ['shell', 'wm', 'density']
        output = self.run(cmd)
        return output.split(':')[-1].strip()

    def test_device_detail(self):
        cmd = ['shell', 'getprop', 'ro.product.device']
        return self.run(cmd)

    def test_device_os(self):
        cmd = ['shell', 'getprop', 'ro.build.version.release']
        return self.run(cmd)

    def tap(self, pos):            
        args = ['shell', 'input', 'tap', pos[0], pos[1]]
        return self.run(args)

    def swipe(self, start, end, use_time):
        args = ['shell', 'input', 'swipe']
        args += [start[0], start[1], end[0], end[1], use_time]
        return self.run(args)

    def input_txt(self, pos, txt):
        self.tap(pos)
        args = ['shell', 'input', 'text', txt]
        return self.run(args)
