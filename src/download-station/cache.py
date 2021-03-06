#!/usr/bin/env python
# -*- coding: utf-8 -*-
#! 强制默认编码为utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os, time

import alfred
from dslib import *
from ds import DSBase

TASKS_CACHE_EXPIRE      = 15    #! 不能太长
DSINFO_CACHE_EXPIRE     = 3600
DSCONFIG_CACHE_EXPIRE   = 3600

class DSCache(DSBase):
    def __init__(self):
        super(DSCache, self).__init__()
        if not self.isAccountInfoExists():
            alfred.exit()
        self.cmds = {
            'all'       : lambda: self.cacheAll(),
            'tasks'     : lambda: self.cacheTasks(),
            'info'      : lambda: self.cacheDSInfo(),
            'config'    : lambda: self.cacheDSConfig()
        }

    def run(self):
        cmd = alfred.argv(1)
        if not cmd:
            return
        try:
            delay = float(alfred.argv(2))
            time.sleep(delay)
        except:
           pass
        caching = '{}-caching'.format(cmd)
        # 检查caching
        if alfred.cache.get(caching):
            return
        alfred.cache.set(caching, True, 10)
        try:
            cmd = cmd.lower()
            if cmd in self.cmds.keys():
                self.cmds[cmd]()
        except Exception, e:
            pass
        alfred.cache.delete(caching)

    def cacheAll(self):
        for k, v in self.cmds.iteritems():
            if k != 'all':
                v()

    def cacheTasks(self):
        if alfred.cache.get('tasks'):
            return
        success, data = self.ds.fetchTaskList()
        if success:
            #? 有时 data会为None WHY?
            tasks = self.parseTasks(data['tasks'])
            if tasks:
                alfred.cache.set('tasks', tasks, TASKS_CACHE_EXPIRE)
        else:
            pass
            # print(data) #如果未授权 会出现错误: unknown url type: webapi/DownloadStation/task.cgi

    def cacheDSInfo(self):
        if alfred.cache.get('dsinfo'):
            return
        success, data = self.ds.fetchInfo()
        if success:
            alfred.cache.set('dsinfo', data, DSINFO_CACHE_EXPIRE)

    def cacheDSConfig(self):
        if alfred.cache.get('dsconfig'):
            return
        success, config = self.ds.fetchConfig()
        if not success:
            return
        success, schedule = self.ds.fetchSchedule()
        if not success:
            return
        data = config
        data.update({
            'schedule_enabled'          : schedule['enabled'],
            'schedule_emule_enabled'    : schedule['emule_enabled']
            })
        alfred.cache.set('dsconfig', data, DSCONFIG_CACHE_EXPIRE)

if __name__ == '__main__':
    DSCache().run()
    