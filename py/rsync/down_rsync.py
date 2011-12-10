#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import sys

'''
对原来update_rsync.sh 的重写
原来的shell脚本对于处理目标路径实在是不友好

1. 支持单个文件之间的同步
2. 如果目标路径是目录，约定路径后加一反斜线
3. 支持全路径: /apps/dat/
'''

APPS_HOME = '/apps'
RSYNC_HOME = os.path.join(APPS_HOME, 'rsync')
RSYNC = os.path.join(RSYNC_HOME, 'bin/rsync')
RSYNC_PASSWORD = os.path.join(RSYNC_HOME, 'conf/rsync.password')

OPTS = '-avz --password-file=%s ' % RSYNC_PASSWORD

def parse_path(path):
    ''' 处理路径 '''
    # sep = '/'
    sep = os.sep
    if os.path.exists(path):
        if os.path.isfile(path):
            if path.endswith(sep):
                path = os.path.abspath(sep)
        if os.path.isdir(path):
            path = os.path.abspath(path) + sep
    return path

def main():
    if len(sys.argv) < 3:
        print 'Usage: %s IP FILE|DIRECTORY [OTHER_RSYNC_OPTS]' % sys.argv[0]
        sys.exit(-1)
    ip = sys.argv[1]
    src = sys.argv[2]
    if src.startswith(APPS_HOME):
        src = parse_path(src)
    else:
        src = parse_path(os.path.join(APPS_HOME, src))
    dst = 'rsync://fetip@:8730%s' % src
    extra_opts = ''
    if len(sys.argv) > 3:
        extra_opts += ' '.join(sys.argv[3:])

    dst = 'rsync://fetip@%s:8730%s' % (ip, src)
    global OPTS
    OPTS += extra_opts

    cmd = '%s %s %s %s' % (RSYNC, OPTS, dst, src)
    # print cmd
    os.system(cmd)

if __name__ == "__main__":
    main()


