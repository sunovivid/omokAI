from multiprocessing import Process, Queue
import time

sentinel = -1

def creator(data, q):
    print('Creating data and putting it on the queue')
    for item in data:
        print('Entered')
        q.put(item)

def my_consumer(q):

    while True:
        data = q.get()
        print(f'data found to be processed: {data}')
        processed = data * 2
        print(processed)

        if data is sentinel:
            break

def timer(sleep_time, timeout_queue):
    time.sleep(sleep_time)
    timeout_queue.put(-1)

def some_hard_task(timeout_queue):
    sum = 0
    for i in range(100000):
        print(i, sum)
        if timeout_queue. == -1:
            return i, sum
        sum += i

if __name__ == '__main__':
    q = Queue()
    timeout_queue = Queue()
    # data = [5, 10, 13, -1]
    # process_one = Process(target=creator, args=(data,q))
    # process_two = Process(target=my_consumer, args=(q,))
    process_task = Process(target=some_hard_task, args=(timeout_queue,))
    process_timer = Process(target=timer, args=(5,timeout_queue))
    # process_one.start()
    # process_two.start()
    process_timer.start()
    process_task.start()

    # q.close()
    # q.join_thread()
    timeout_queue.close()
    timeout_queue.join_thread()

    # process_one.join()
    # process_two.join()
    process_timer.join()
    process_task.join()