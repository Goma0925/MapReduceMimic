from typing import Callable
import threading
from random import randint

global_lock = threading.Lock()

class Worker:
    def __init__(self, worker_id):
        self.result = []
        self.worker_id = worker_id

    def work(self, call_back_func):
        for i in range(10):
            self.result.append(randint(1, 100))
        result = self.result
        worker_id = self.worker_id
        global_lock.acquire()
        call_back_func(worker_id, result)
        global_lock.release()

class MyThread(threading.Thread):
    def __init__(self, name, sleep_time):
        threading.Thread.__init__(self)
        self.name = name
        self.sleep_time = sleep_time


    def run(self):
        for i in range(10):
            print(self.name + ': ' + str(i))
            time.sleep(self.sleep_time)


class Master:
    def __init__(self):
        self.data = {}
        self.threads = []

    def _update_data(self, worker_id, arr):
        self.data[worker_id] = arr
        print("Worker-" + str(worker_id) + " is updating data")
        if len(self.data) == 5:
            self._after_all_threads_are_done()

    def _after_all_threads_are_done(self):
        print("THREADS DONE")
        for key in self.data:
            print(key, end=": ")
            print(self.data[key])

    def start_thread(self, num):
        for i in range(num):
            w = Worker("ID-" + str(i))
            t = threading.Thread(target=w.work, args=[self._update_data])
            t.start()




class Test:
    def __init__(self):
        self.call_back = None

    def set_func(self, func: Callable[[str], str]):
        self.call_back = func

    def call_back(self, param):
        self.call_back()

def sayHi(param):
    print("HIii" + param)
    return "HIii" + param


m = Master()
m.start_thread(5)
print(m.data)
