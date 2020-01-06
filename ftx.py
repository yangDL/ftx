# -*- coding: utf-8 -*-
import sys
import random
import time
import argparse
import logging
from common import debug, config, robot

logging.basicConfig(level = logging.INFO, format = '%(asctime)s %(name)s %(levelname)s:%(message)s')
log = logging.getLogger('FTX.robot')
log.setLevel(logging.INFO)

def main():
    log.info('激活窗口并按 CONTROL + C 组合键退出')
    debug.dump_device_info()
    cpt = config.Component()
    components = cpt.load()
    step = config.Step()
    steps = step.load()
    task = robot.Task(components, steps)
    tasks = task.gen_tasks()
    robot_man = robot.Robot(tasks)
    robot_man.run()
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        adb.run('kill-server')
        log.info('谢谢使用')
        exit(0)
