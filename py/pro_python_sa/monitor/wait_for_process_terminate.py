# waitting for the process to terminate

import subprocess
import time
from datetime import datetime

p = subprocess.Popen('sleep 10', shell=True)

while True:
    rc = p.poll()
    if rc is None:
        print "[%s] Process with PID: %d is still running ..." % (datetime.now(), p.pid)
        time.sleep(1)
        p.int()
    else:
        print "[%s] Process with PID: %d has terminated. Exit code: %d" % (datetime.now(), p.pid, rc)
        break
