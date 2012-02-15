# -*- encoding:utf-8 -*-

import sys, os, time, atexit

from signal import SIGTERM

class Daemon:
    """ A generic daemon class """

    def __init__(self, pidfile, stdin="/dev/null", stdout="/dev/null", stderr="/dev/null"):
        self.stdin = stdin
        self.stderr = stderr
        self.stdout = stdout
        self.pidfile = pidfile

    def daemonize(self):
        """ do the UNIX double-fork magic """

        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            print >> sys.stderr, "fork #1 failed: %d (%s)\n" % (e.errno, e.strerror)
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")

        #  setsid runs a program in a new session.
        # make you're the leader of the process group
        os.setsid()

        os.umask(0)

        # do the second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            print >> sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, "r")
        so = file(self.stdout, "a+")
        # make stderr unbuffered
        se = file(self.stderr, "a+", 0)

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w') as fb:
            fb.write(pid)

    def delpid(self):
        os.unlink(self.pidfile)

    def start(self):
        """ Start the daemon """

        # Check for a pidfile to see if the daemon already runs
        pid = self._get_pid()

        if pid is not None:
            message = "pidfile %s already exist. Daemon already running?\n"
            print >> sys.stderr, message
            sys.exit(1)

        # start the daemon
        self.daemonize()
        self.run()

    def _get_pid(self):
        pid = None
        if os.path.exists(self.pidfile):
            with open(self.pidfile, 'r') as fb:
                pid = int(fb.read().strip())
        return pid

    def stop(self):
        """ Stop the daemon """
        pid = self._get_pid()

        if pid is None:
            message = "pidfile %s does not exist. Daemon not running?\n"
            print >> sys.stderr, message % self.pidfile
            return

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, e:
            err = str(e)
            if err.find("No such process") > 0:
                if os.path.exist(self.pidfile):
                    os.unlink(self.pidfile)
                else:
                    print err
                    sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        """ Override this method """

class Test(Daemon):
    def __init__(self, pidfile):
        Daemon.__init__(self, pidfile)

    def run(self):
        while 1:
            time.sleep(10)

def test():
    d = Test('/tmp/test.pid')
    d.start()

test()


