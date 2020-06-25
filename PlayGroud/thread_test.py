import threading
from random import randint


def worker():
    """thread worker function"""
    print('Worker')

# class Mapper:
#     def __init__(self, name):
#         self.name = name
#         self.items = []
#
#     def map(self):
#         for i in range(10):
#             self.items.append(randint(100, 200))

# from mappers import Mapper
import importlib.machinery
# Mapper = importlib.machinery.SourceFileLoader('Mapper', 'mappers/Mapper.py').load_module()
module = importlib.machinery.SourceFileLoader('Module', './Module.py').load_module()
p = module.Person()
p.sayHi()

mappers = []
threads = []
for i in range(5):
    mapper = Mapper.Mapper(i)
    mappers.append(mapper)
    t = threading.Thread(target=mapper.map())
    threads.append(t)
    t.start()

    print("Done mapping")
for m in mappers:
    print(m.name)
    print("RESULT: ", end="")
    print(m.result)
    print("-------------------")