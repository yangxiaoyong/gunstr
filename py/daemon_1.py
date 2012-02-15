import sys, os
import time

def main():
    """ A demo daemon mani routine, write a datestam to
    /tmp/daemon-log every 10 seconds.
    """
    with open('/tmp/daemon-log', 'w') as fb:
        while 1:
            fb.write('%s\n' % time.ctime(time.time()))
            fb.flush()
            time.sleep(10)


if __name__ == "__main__":
    try:
        pid = os.fork()
        print "fork process with pid: %s" % pid
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        print >> sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # decouple from parent enviroment
    os.chdir("/")
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            print "Daemon PID %d" % pid
            sys.exit(0)
    except OSError, e:
        print >> sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # start daemon
    main()


