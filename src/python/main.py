import psutil
import time

config = {}

while(True):
    print("new round check...")
    ps = psutil.pids()
    for x in ps:
        try:
            p = psutil.Process(x)
            # who own the process and how much can this one use?
            if not p.username() in config:
                print(p.username())
                config[p.username()] = 50
            
            availble = config[p.username()]
            if p.memory_percent() > availble:
                print(config)
                print("process %d take too large memory, ownner %s, path %s ,ready to kill"%(x, p.username(), p.exe()))
                p.kill()
        except:
            continue
    tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("check end, stop. time %s\n------------------------------"%tm)
    time.sleep(10)
