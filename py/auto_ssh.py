#!/usr/bin/env python
# encoding:utf8

import os

def parse_sshconfig():
    ret = {}
    ssh_config_file = os.path.join(os.path.expanduser('~'), '.ssh', 'config')
    with file(ssh_config_file, 'r') as fb:
        has_begin = False
        tmp = []
        for line in fb:
            # 遇到空行
            # 1. 如果有标志正在处理一个块，那么视为该配置块的结束
            # 2. 否则继续往下走
            line = line.strip()
            if not line:
                if has_begin:
                    has_begin = False
                    print tmp
                    ret[tmp[0][1]] = dict(tmp)
                    tmp = []
                continue
            if line.startswith('#'): continue
            li = line.split()
            if li[0].lower() == 'host':
                has_begin = True
            if has_begin:
                tmp.append((li[0], li[1]))
    return ret

if __name__ == "__main__":
    parse_sshconfig()

