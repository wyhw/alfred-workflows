# -*- coding: utf-8 -*-
import alfred
alfred.setDefaultEncodingUTF8()

import subprocess
from AppKit import NSPasteboard, NSArray

#! 地址在传递参数中均使用base64编码 防止出错 
from base64 import b64decode

# 拷贝到剪切板
def copyToClipboard():
    try:
        word = b64decode(alfred.argv(2))
        pb = NSPasteboard.generalPasteboard()
        pb.clearContents()
        a = NSArray.arrayWithObject_(word)
        pb.writeObjects_(a)
        alfred.exit('已拷贝地址到剪切板')
    except Exception, e:
        alfred.log(e)
        alfred.exit('出错啦')

# 打开地址
def openURL():
    try:
        page = b64decode(alfred.argv(2))
        subprocess.check_output('open "{}"'.format(page), shell=True)
    except Exception, e:
        alfred.log(e)
        alfred.exit('出错啦')

def downloadWithDS():
    try:
        link = b64decode(alfred.argv(2))
        alfred.query('ds create {}'.format(link))
    except Exception, e:
        alfred.log(e)
        alfred.exit('出错啦')

def main():
    cmds = {
        'open-url'          : lambda: openURL(),
        'copy-to-clipboard' : lambda: copyToClipboard(),
        'download-with-ds'  : lambda: downloadWithDS()
    }
    cmd = alfred.argv(1)
    if not cmd or cmd.lower() not in cmds.keys():
        alfred.exit('出错啦')
    cmds[cmd]();

if __name__ == '__main__':
    main()