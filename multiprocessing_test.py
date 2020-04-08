import multiprocessing
from pprint import pprint

def timer(procnum, return_dict):
    print(str(procnum)+' represent!')
    return_dict[procnum] = procnum

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []

    p = multiprocessing.Process(target=timer, args=(i,))
    jobs.append(p)
    p.start()

    for proc in jobs:
        proc.join()

    print(return_dict.values())