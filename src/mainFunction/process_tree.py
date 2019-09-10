import psutil
import os

config = {}

def get_tree(pid, user):
    '''
    根据给定的pid向上搜索到根部，再从根部搜索所有从根部创建出的进程
    # Args:
        pid: 给定节点的pid，可以是树中的任意节点
    # Return:
        targetList: 所有树中节点的pid按照广度搜索得到的结果
    '''
    ps = psutil.pids()
    pp = None
    for x in ps:
        if int(x) == int(pid):
            p = psutil.Process(x)
            while p.username() == user:
                pp = p
                px = p.ppid()
                p = psutil.Process(px)
            break
    targetList = [int(pp.pid)]
    find = True
    while find:
        find = False
        for x in ps:
            try:
                p = psutil.Process(x)
                ppid = p.ppid()
                pid = int(x)
            except:
                continue
            if ppid in targetList and pid not in targetList:
                targetList.append(pid)
                find = True    
    return targetList


