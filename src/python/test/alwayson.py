import time
import os

print("Here comes a tree with depth 3")

pids = []

for i in range(3):
    pid = os.fork()
    if pid:
        pids.append(pid)

for pid in pids:
    print(pid)
    if pid == 0:
        for i in range(10):
            #print("child process pid=%s, ppid=%s"%(os.getpid(), os.getppid()))
            time.sleep(3)
    else:
        for i in range(10):
            #print("parrent process pid=%s, ppid=%s"%(os.getpid(), os.getppid()))
            time.sleep(3)
