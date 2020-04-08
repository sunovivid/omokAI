import multiprocessing
import time

def bar():
    for i in range(100):
        print("Tick")
        time.sleep(1)

if __name__ == '__main__':
    p = multiprocessing.Process(target=bar)
    p.start()

    p.join(10)

    if p.is_alive():
        print("running.. let's kill it..")
        p.terminate()
        p.join()