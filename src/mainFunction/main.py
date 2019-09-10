import psutil
import time
import json
from process_tree import get_tree
import os

#from src.mainFunction.process_tree import get_tree

def get_configuration():
    '''
    get pre-set mem space configuration for each user from configuration file, path configurations/user_resources.conf
    # Return
        (dict) memory space each user could occupy, unit kb
    '''
    units_translation = {"KB":1, "MB": 1024, "GB": 1048576}
    data = {}
    with open("src/configurations/user_resources.conf") as f:
        for lines in f:
            username, volumn, unit = lines.rstrip().split(' ')
            data[username] = int(volumn)*units_translation[unit]
    return data


def get_usage():
    '''
    get current memory usage for each user with psutil tool
    # Return
        (dict) process trees for each user and usage for each process
    '''
    configuration = get_configuration()
    # configuration["xxx"] = 10000, unit kb
    info = {}
    tree_info = {}
    usage = {}
    ps = psutil.pids()
    searched_node = []
    for x in ps:
        try:
            p = psutil.Process(x)
            username = p.username()
            mem_usage = p.memory_info().rss
            cpu_usage = p.cpu_percent()
            pid = int(x)
            usage[pid] = {"mem":mem_usage/1024, "cpu": cpu_usage}
            if not username in configuration:
                configuration[username] = configuration['*']
            if x in searched_node or int(configuration[username]) < 0 :
                continue
            if not username in tree_info:
                tree_info[username] = {}
                tree_info[username]["process_tree"] = []
                tree_info[username]["memory_max"] = configuration[username]
            prc_tree = get_tree(pid, username)
            searched_node.extend(prc_tree)
            tree_info[username]["process_tree"].append(prc_tree)
        except:
            if int(x) in usage:
                usage.pop(int(x))
            continue
    info["tree_info"] = tree_info
    info["usage"] = usage
    date = time.strftime("%Y-%m-%d.json_archieve", time.localtime())
    if os.path.exists("current.json"):
        os.system("echo >> src/archieves/%s && date >> src/archieves/%s && cat current.json >> src/archieves/%s"%(date, date, date))

    with open("current.json", "w+") as f:
        json.dump(info, f)
    return info

def main():
    info = get_usage()
    tree_info = info["tree_info"]
    usage = info["usage"]
    for user in tree_info:
        for tree in tree_info[user]["process_tree"]:
            mem = 0
            for x in tree:
                mem += usage[int(x)]["mem"]
            if mem > tree_info[user]["memory_max"]:
                #TODO: kill process
                for x in tree:
                    p = psutil.Process(x)
                    #p.kill()
                print(mem)
                print(tree)


def old_process():
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

if __name__=="__main__":
    #get_usage()
    main()