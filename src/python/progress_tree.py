import psutil
import os

config = {}

def get_tree(pid):
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
        if x == pid:
            #import pdb;pdb.set_trace()
            p = psutil.Process(x)
            while p.cmdline() != ['/usr/bin/zsh']:
                pp = p
                px = p.ppid()
                p = psutil.Process(px)
            break
    targetList = [pp.pid]
    find = True
    while find:
        find = False
        for x in ps:
            try:
                p = psutil.Process(x)
                ppid = p.ppid()
                pid = p.pid
            except:
                continue
            if ppid in targetList and pid not in targetList:
                targetList.append(pid)
                find = True    
    return targetList


def Xtest_get_tree():
    '''
    对获取进程树进行测试，方法为：
    1. 运行测试程序，测试程序没有具体功能，主要为创建一整个进程树，并将其中某个叶子节点的名命与其它区分开
    2. 寻找这个特别命名的节点（测试中尽量不碰触危险功能）
    3. 搜索到根，从根开始得到整个树，返回

    # Args:
        N/A
    # Return:
        该功能是否正常工作，正常为True，否则为False
    '''
    tree = None
    # 找到目标节点
    os.popen("python3 alwayson.py")
    targetLeaf = ["python3", "alwayson.py"]
    ps = psutil.pids()
    for x in ps:
        try:
            p = psutil.Process(x)
            pid = p.pid
            cmd = p.cmdline()
        except:
            continue
        if cmd == targetLeaf:
            tree = get_tree(pid)
            break
    if tree is not None:
        return True


if __name__ == "__main__":
    if Xtest_get_tree():
        print("PASS, get_tree function")