import psutil

class HostProperties(Plugin):

    def __init__(self, **kwargs):
        self.keywords = ['provider']
        print self.__class__.__name__, 'initializing ...'

    def _get_total_cores(self):
        c_cups = 0
        with open('/proc/cpuinfo') as fb:
            for line in fb:
                if line.startswith('processor'):
                    c_cups += 1
        return c_cups

    def generate(self, **kwargs):
        result = {'mem_phys_total': psutil.TOTAL_PHYMEM,
                  'mem_phys_avail': psutil.avail_phymem(),
                  'mem_phys_used': psutil.used_phymem(),
                  'mem_virt_total': psutil.total_virtmem(),
                  'mem_virt_avail': psutil.used_virtmem(),
                  'cpu_cores': self._get_total_core(),
                }

        return result
