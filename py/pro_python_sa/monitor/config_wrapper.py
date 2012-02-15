#-*- encoding:utf-8 -*-

from ConfigParser import SafeConfigParser

class ConfigManager(object):

    class Section:
        def __init__(self, name, parser):
            self.__dict__['name'] = name
            self.__dict__['parser'] = parser

        def __setattr__(self, option, value):
            self.__dict__[option] = str(value)
            self.parser.set(self.name, option, str(value))

    def __init__(self, file_name):
        self.parser = SafeConfigParser()
        self.parser.read(file_name)
        self.file_name = file_name

        for section in self.parser.sections():
            setattr(self, section, self.Section(section, self.parser))
            for option in self.parser.options(section):
                setattr(getattr(self, section), option, self.parser.get(section, option))

    def __getattr__(self, section):
        self.parser.add_section(section)
        setattr(self, section, self.Section(section, self.parser))
        return getattr(self, section)

    def save_config(self):
        with file(self.file_name, 'w') as fb:
            self.parser.write(fb)

