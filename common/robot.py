# -*- coding: utf-8 -*-
"""
调取配置文件和屏幕分辨率的代码
"""
import os
import re
import sys
import json
import time
import logging
from common.adb import ADB
from common import config, constant

log = logging.getLogger('FTX.robot')

class TaskErrorAttr(Exception):
    def __init__(self, desc):
        msg = "任务参数异常: {}".format(desc)
        super(TaskErrorAttr, self).__init__(msg)

class Robot(object):
    
    def __init__(self, tasks):
        self.adb = ADB()
        self.tasks = tasks
    
    def _is_x_y(self, data, desc=""):
        x, y = data
        if not x or not y:
            raise TaskErrorAttr(desc)
        return True
    
    def run(self):
        for task in self.tasks:
            if 'op' not in task:
                log.error("{}格式错误".format(task))
                continue

            if task['op'] not in constant.COMPONENTS:
                log.error("{} 不支持该操作".format(task['op']))
                continue
            desc = '' if 'desc' not in task or not task['desc'] else task['desc']
            if task['type'] == 'tap':
                self.tap(task['start'], desc=desc)
            elif task['type'] == 'swipe':
                use_time = 200 if 'use_time' not in task else task['use_time']
                self.swipe(task['start'], task['end'], use_time, desc)
            elif task['type'] in ['input', 'username', 'password']:
                self.input(task['start'], task['txt'])
            sleep = 0.2 if not task['sleep'] else task['sleep']
            time.sleep(sleep)
            continue                
            
    def tap(self, pos, desc):
        self._is_x_y(pos, desc)
        return self.adb.tap(pos)

    def swipe(self, start, end, use_time, desc):
        if not self._is_x_y(start, desc):
            return None
        if not self._is_x_y(end, desc):
            return None
        return self.adb.swipe(start, end, use_time)

    def input(self, pos, txt):
        return self.adb.input_txt(pos, txt)
        

class Task(object):
    
    def __init__(self, components, steps):
        self.components = components
        self.steps = steps
    
    def gen_tasks(self):
        tasks = []
        for step in self.steps:
            if step['name'] not in self.components:
                raise config.OpErrorType(step['name'])
            if step['type'] == 'login':
                tasks += self._gen_login_tasks(step)
        return tasks
    
    def _gen_login_tasks(self, step):
        tasks = []
        cpts = self.components[step['name']]
        for cpt in cpts:
            if cpt['type'] == "username":
                cpt['txt'] = step['username']
            elif cpt['type'] == 'password':
                cpt['txt'] = step['password']
            tasks.append(cpt)
        return tasks
            