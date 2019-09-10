from src.python.progress_tree import get_tree
import psutil
import os

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