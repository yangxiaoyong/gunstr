#!/usr/bin/env python
'''
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
    lo:    3900      64    0    0    0     0          0         0     3900      64    0    0    0     0       0          0
  eth0: 324167652  278161    0    0    0     0          0        25 12130650  144220    0    0    0     0       0          0
 wlan0:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
  ppp0: 314504540  224722    0    0    0     0          0         0  8909365  142320    0    0    0     0       0          0

'''
import sys
from time import sleep

class NoSuchNetworkInterface(Exception):
    pass

class NetDevice(object):
    def __init__(self, interface):
        self.interface = interface

    def get_rx_bytes(self):
        return float(self.status[0])

    def get_rx_packets(self):
        return float(self.status[1])

    def get_tx_bytes(self):
        return float(self.status[8])

    def get_tx_packets(self):
        return float(self.status[9])

    def read_proc(self):
        proc_net = '/proc/net/dev'
        has_interface = False
        with open(proc_net, 'rb') as fb:
            for line in fb:
                line = line.lstrip()
                if line.startswith(self.interface):
                    has_interface = True
                    self.status = line.split(self.interface + ':')[-1].split()
        if not has_interface:
            raise NoSuchNetworkInterface(self.interface)

    def get(self, name):
        self.read_proc()
        if hasattr(self, 'get_' + name):
            return getattr(self, 'get_' + name)()
        else:
            raise AttributeError('No such attribute get_%s' % name)


def output_interface_status(interface):

    netdev = NetDevice(interface)
    rx_bytes = netdev.get('rx_bytes')
    rx_packets = netdev.get('rx_packets')
    tx_bytes = netdev.get('tx_bytes')
    tx_packets = netdev.get('tx_packets')

    print '== %s ==' % interface
    print 'rx_bytes  : %s, (%.2f)MB ' % (rx_bytes, float(rx_bytes)/1024/1024)
    print 'rx_packets: %s' % rx_packets
    print 'tx_bytes  : %s, (%.2f)MB ' % (tx_bytes, float(tx_bytes)/1024/1024)
    print 'tx_packets: %s' % tx_packets

def calc_rate(interface, interval, attr):
    '''calc the current network rate'''
    netdev = NetDevice(interface)
    while 1:
        before = netdev.get(attr)
        sleep(interval)
        diff = netdev.get(attr) - before
        # rate = diff / interval
        print "Interface: %s, in %s seconds, %s rate is %.2f bytes" % (interface, interval, attr, diff)

def output_network_throught(interface, times=5, interval=1, unit='bytes'):
    '''only care about incomming and output traffics

    Output like this:

      Incoming     Output       Rate            sum_traffic
      111 bytes    222 bytes    200 bytes/sec   xxxx
      1 MiB        222 MiB

    '''

    unit_dict = {'bytes': 1,
                 'KiB': 1024,
                 'MiB': 1024 * 1024}
    format = lambda x: x + ' %s' % unit
    netdev = NetDevice(interface)
    print 'Traffic about %s, interval: %s seconds' % (interface, interval)
    print 'IncomingTraffic    OutTraffic    SumTraffic'
    while times > 0:
        times -= 1
        rx_bytes = netdev.get('rx_bytes')
        tx_bytes = netdev.get('tx_bytes')
        sleep(interval)
        rx = (netdev.get('rx_bytes') - rx_bytes) / unit_dict.get(unit, 1)
        tx = (netdev.get('tx_bytes') - tx_bytes) / unit_dict.get(unit, 1)
        sum_traffic = rx + tx
        output = map(format,
                     ['%.4f' % rx,  '%10.4f' % tx, '%10.4f' % sum_traffic])
        # print output
        print ''.join(output)

if __name__ == "__main__":
    # output_interface_status('eth0')
    # calc_rate('ppp0', 1, 'rx_bytes')
    # interface times interval [unit]
    interface = 'eth0'
    times = 5
    interval = 1
    unit = 'bytes'
    if len(sys.argv) >= 4:
        interface, times, interval = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
        if len(sys.argv) >= 5:
            unit = sys.argv[4]
        output_network_throught(interface, times, interval, unit)
    else:
        print 'Args not enough!'
        print 'Usage:',  sys.argv[0],  'interface_name[eth0|eth1] output_times[5|10] interval[1|5] [output_unit[bytes|KiB|MiB]]'
        sys.exit(1)


