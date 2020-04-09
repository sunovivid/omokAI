import os

from multiprocessing import Process, current_process

def doubler(number):

    result = number * 2
    proc = os.getpid()
    proc_name = current_process().name
    print(f"{number} doubled to {result} by process name: {proc_name}, id: {proc}")

if __name__ == '__main__':
    numbers = [5, 10, 15, 20, 25]
    procs = []

    for index, number in enumerate(numbers):
        proc = Process(target=doubler, args=(number,))
        procs.append(proc)
        proc.start()

    proc = Process(target=doubler, name='Test', args=(2,))
    proc.start()
    procs.append(proc)

    for proc in procs:
        proc.join()