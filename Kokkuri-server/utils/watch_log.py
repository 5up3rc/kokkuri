#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    utils.watch_log
    ~~~~~~~~~~~~~~~

    Watching rsyslog's log file.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/kokkuri
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import subprocess
import datetime
import threading
import time

from config import settings


class WatchLogFile(threading.Thread):
    """
    监控日志文件的变化
    并将读到的日志放到队列里去，交给分析模块进行处理
    """

    def __init__(self, target_queue=None):
        super(WatchLogFile, self).__init__()

        # 今天的日期
        self.today = datetime.date.today()

        # 获取日志格式
        self.log_file_template = settings.LOGFILE_FORMAT

        # 线程名字
        self.name = "{0}.log_watch_thread".format(self.today.strftime("%Y%m%d"))

        # tail进程的pid
        self.pid = None

        # 退出标志
        self._exit_flag = False

        # 目标队列
        self.target_queue = target_queue

    def stop_thread(self):
        self._exit_flag = True

    def set_target_queue(self, target_queue):
        self.target_queue = target_queue

    def update_time(self):
        """
        更新今天的日期
        :return:
        """
        self.today = datetime.date.today()

    def run(self):
        process = subprocess.Popen(
            "tail -f {0}".format(self.today.strftime(self.log_file_template)),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        self.pid = process.pid
        while not self._exit_flag:
            line = process.stdout.readline().strip()
            if line:
                # todo: do something...
                print(line)
            else:
                # 没有读取到内容
                time.sleep(1)
                # 检查是不是已经到明天了
                if datetime.date.today() != self.today:
                    self.update_time()
                    process.kill()
                    process = subprocess.Popen(
                        "tail -f {0}".format(self.today.strftime(self.log_file_template)),
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
                    )



