#!/usr/bin/env python
#coding:utf-8

'''
定时上报 WAN 口地址
'''
import sys
import re
import socket, struct
import urllib
import base64
import urllib2

from subprocess import Popen, PIPE

# 调用shell命令 curl ifconfig.me
def _get_wan_ip():
    cmd = 'curl ifconfig.me'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if stderr:
        print >> sys.stderr, stderr
        return ''
    ret = stdout.read().strip()
    return ret

def get_wan_ip():
    pat = re.compile('(\d+\.\d+\.\d+\.\d+)')
    url = 'http://checkip.dyndns.org/'
    response = urllib2.urlopen(url)
    html = response.read()
    if pat.search(html):
        return pat.search(html).group(0)
    else:
        return ''

get_wan_ip()


def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

    return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

def report():
    gateway_map = {'192.168.0.50': 2,
                   '192.168.0.1' : 1,
                   }
    wan_ip = get_wan_ip()
    print wan_ip
    gateway = get_default_gateway_linux()
    if not (wan_ip and gateway):
        print >> sys.stderr, "Could not get default gateway or wan_ip"
        sys.exit(1)

    url = 'http://stat.cdcn86.com/api/api.php?'
    query = {'c': gateway_map[gateway],
             'd': wan_ip}

    params = urllib.urlencode(query)
    print params
    signed = {'m': base64.encodestring(params)}
    url_args = urllib.urlencode(signed)

    req = urllib2.Request(url + url_args)
    response = urllib2.urlopen(req)
    print response.read()


if __name__ == "__main__":
    report()




