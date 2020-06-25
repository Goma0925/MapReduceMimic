class Concrete:
    def method(self):
        print("Concrete running")


class Test:
    def __init__(self):
        self.attr = 0

    def run(self, obj):
        obj.method()

import importlib.machinery
import re

module_path = "/Users/Amon/Desktop/@Python_project/MapReduceMimic/PlayGroud/mappers/Mapper2.py"
module_name = module_path.split("/")[-1].rstrip(".py")
module_name = "Mapper2.py"
print(module_path)

module = importlib.machinery.SourceFileLoader(module_name, module_path).load_module()
m = module.Mapper("A")
m.sayHi()




# c = Concrete()
# t.run(c)