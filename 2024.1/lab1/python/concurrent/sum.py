import os, os.path
import threading
import sys

mutex = threading.Semaphore(1)
count = len(os.listdir('../../dataset/'))
semaphore = threading.Semaphore(count//2)
res = 0

def sum_thread(start, end):
    global res
    for i in range(start, end):
        mutex.acquire()
        res += do_sum("../../dataset/" + "file." + str(i + 1))
        mutex.release()


def do_sum(path):
    _sum = 0
    with open(path, 'rb',buffering=0) as f:
        byte = f.read(1)
        while byte:
            semaphore.acquire()
            _sum += int.from_bytes(byte, byteorder='big', signed=False)
            byte = f.read(1)
            semaphore.release()    
        return _sum

if __name__ == "__main__":
    # res = [0] * num_threads
    threads = []
    
    for i in range(10):
        t = threading.Thread(target =sum_thread, args=(0,
            10))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(res)