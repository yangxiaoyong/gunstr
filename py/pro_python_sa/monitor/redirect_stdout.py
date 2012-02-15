import subprocess
import os

f = os.open('output.txt', os.O_CREAT|os.O_WRONLY)
subprocess.Popen('date', stdout=f)
