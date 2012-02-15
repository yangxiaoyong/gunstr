#-*- encoding:utf8 -*-
import xmlrpclib
import sqlite3
import tempfile
import tarfile
import shutil
import subprocess
import os

from datetime import datetime

import cherrpy
import multiprocessing

class TicketScheduler(multiprocessing.Process):
    '''The TicketScheduler class inserts probing tickets into the ticket queue'''
    def __init__(self, event):
        self.event = event
        self.con = sqlite3.connect('monitor.db')
        super(TicketScheduler, self).__init__()

    def run(self):
        try:
            while True:
                sql = ("SELECT hostprobe_id FROM probingschedule "
                      "WHERE (strftime('%s', 'now')/60) % probingschedule.probeinterval = 0;")
                self.event.wait()
                res = [r[0] for r in self.con.execute(sql)]
                for probe_id in res:
                    self.con.execute("INSERT INTO ticketqueue VALUES (NULL, ?, datetime('now'), 0",
                            (probe_id))
                self.con.commit()
        except KeyboardInterrupt:
            pass

class Root(object):
    @cherrpy.expose
    def cmd_store_probe_data(self, ticket, probe, tstamp):
        # probe - [ret_code, data_string]
        self.store_reading(ticket, probe, tstamp)
        return 'OK'

    @cherrpy.expose
    def cmd_get_new_monitor_url(self, host):
        '''Supplying a new server address'''
        port = cherrpy.config.get('server.socket_port')
        if not bool(port):
            port = 8080
        host = cherrpy.config.get('server.socket_host')
        if not bool(host):
            host = '127.0.0.1'
        server_url = 'http://%s:%s/xmlrpc/' % (host, str(port))
        con = sqlite3.connect('monitor.db')
        res = con.execute('''SELECT hostparams.value
                                FROM hostparams, host, systemparams
                                WHERE host.id = hostparms.host_id
                                  AND systemparams.name = 'monitor_url'
                                  AND hostparams.param_id = systemparams.id
                                  AND host.address = ?''', ((host,))
                                  ).fetchone()

        if not res:
            res = con.execute("SELECT value FROM systemparams"
                              "WHERE name = 'monitor_url'").fetchone()
        if res:
            server_url = res[0]
        return server_url

    @cherrpy.expose
    def cmd_get_sensor_code(self, sensor):
        '''Sending binary data via an XML-RPC link'''
        with open('%s/%s.tar.bz2' % (self.cm.sensor.source_dir, sensor), 'rb') as fb:
            return xmlrpclib.Binary(fb.read())

    @cherrpy.expose
    def healthcheck(self):
        '''Server Health check'''
        return 'OK'

    @cherrpy.expose
    def cmd_update_sensor_code(self, sensor):
        # get the new file
        proxy = xmlrpclib.ServerProxy(self.cm.monitor.url)
        tmp_dir = tempfile.mkdtemp(dir='.')
        dst_file = "%s/%s.tar.bz2" % (tmp_dir, sensor)
        with open(dst_file, 'wb') as f:
            f.write(proxy.cmd_get_sensor_code(sensor).data)
            f.close()
        # unpack it
        arch = tarfile.open(dst_file)
        arch.extractall(path=tmp_dir)
        arch.close()
        # check it
        cmd = ["%s/%s/%s" % (tmp_dir, sensor, self.cm.sensor.executable), "options"]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.communicate()
        if p.returncode != 0:
            # remove if fails
            shutil.rmtree(tmp_dir)
        else:
            # backup up the existing package
            sens_dir = "%s/%s" % (self.cm.sensor.path, sensor)
            bck_dir = "%s/%s_%s" % (self.cm.sensor.backup, sensor,
                    datetime.strftime(datetime.now(), "%Y-%m-%d%H:%M:%S"))

            try:
                shutil.move(sens_dir, bck_dir)
            except:
                pass
            os.remove(dst_file)
            # replace with new
            shutil.move("%s/%s" % (tmp_dir, sensor), sens_dir)
            os.rmdir(tmp_dir)
        return 'OK'

    def store_reading(self, ticket, probe, tstamp):
        con = sqlite3.connect('monitor.db')
        res = [r[0] for r in con.execute('SELECT hostprobe_id FROM ticketqueue WHERE id=?',
                (ticket, ))][0]
        if res:
            con.execute('DELETE FROM ticketqueue WHERE id=?', (ticket,))
            con.execute('INSERT INTO probereading VALUES (NULL, ?, ?, ?, ?)',
                    (res, str(tstamp), float(probe[1].strip()), int(probe[0])))
            con.commit()
        else:
            print 'Ticket does not exists: %s' % str(ticket)

class ParsePendingTicket(object):
    def a(self):
        sql = "SELECT id, hostprobe_id FROM ticketqueue WHERE dispatched = 0"
        pending_tickets = [r for r in self.con.execute(sql)]
        for (ticket_id, hostprobe_id) in pending_tickets:
            sql = """SELECT host.address, host.port, sensor.name, probe.parameter
                  FROM hostprobe, host, probe, sensor
                    WHERE hostprobe.id=?
                      AND hostprobe.host_id = host.id
                      AND hostprobe.probe_id = probe.id
                      AND probe.sensor_id = sensor.id
                      """
            res = [r for r in self.con.execute(sql, (hostprobe_id, ))][0]
            self._send_request(ticket_id, res[0], res[1], res[2], res[3])
            sql = "UPDATE ticketqueue SET dispatched=1 WHERE id=?"
            self.con.execute(sql, (ticket_id))
        self.con.commit()

    def _send_request(self, ticket, address, port, sensor, parameter_string=None):
        url = "http://%s:%s/xmlrpc/" % (address, port)
        proxy = xmlrpclib.ServerProxy(url, allow_none=True)
        if parameter_string:
            parameter = parameter_string.split(',')
        else:
            parameter = None
        print ticket
        print sensor
        print parameter
        res = proxy.cmd_submit_reading(ticket, sensor, parameter)
        return
