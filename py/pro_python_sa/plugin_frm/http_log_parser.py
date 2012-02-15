#!/usr/bin/env python
# coding:utf-8

import re
import os
import csv

from manager import Plugin, PluginManager

DIRECTIVE_MAP = {
        '%h': 'remote_host',
        '%l': 'remote_logname',
        '%u': 'remote_user',
        '%t': 'time_stamp',
        '%r': 'request_line',
        '%>s': 'status',
        '%b': 'response_size',
        '%{Referer}i': 'referer_url',
        '%{User-Agent}i': 'user_agent',
        }

class LogLineGenerator:

    def __init__(self, log_format=None, log_dir='logs'):
        # LogFormat '%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"{User-Agent}\" combined'
        if not log_format:
            self.format_string = '%h %l %u %t %r %>s %b %{Referer}i %{User-Agent}i'
        else:
            self.format_string = log_format
        self.log_dir = log_dir
        self.re_tsquote = re.compile(r'(\[|\])')
        self.field_list = []
        [self.field_list.append(DIRECTIVE_MAP[k]) for k in self.format_string.split()]

    def _quote_translator(self, file_name):
        '''将日志每行出现的 [] 字符转换为双引号 " '''

        with open(file_name) as fb:
            for line in fb:
                yield self.re_tsquote.sub('"', line)

    def _file_list(self):
        for fn in os.listdir(self.log_dir):
            fp = os.path.join(self.log_dir, fn)
            if os.path.isfile(fp):
                yield fp

    def get_loglines(self):
        for fn in self._file_list():
            reader = csv.DictReader(self._quote_translator(fn),
                                    fieldnames = self.field_list,
                                    delimiter = ' ',
                                    quotechar = '"')
            for line in reader:
                yield line

def simple_log():
    log_generator = LogLineGenerator()
    for log_line in log_generator.get_loglines():
        print "-" * 20
        for k, v in log_line.iteritems():
            print "%20s: %s" % (k, v)


def main():
    plugin_manager = PluginManager()
    log_generator = LogLineGenerator()
    for log_line in log_generator.get_loglines():
        plugin_manager.call_method('process', args=log_line)
    plugin_manager.call_method('report')

class CountHTTP200(Plugin):

    def __init__(self, **kwargs):
        self.keywords = ['counter']


if __name__ == "__main__":
    main()
