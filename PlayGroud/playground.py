import datetime
import math
import os
import sys
import pkgutil

for i in pkgutil.walk_packages():
    print(i.name)
print(datetime.datetime.now().strftime("%mm%dd%Yy_%H_%M "))

class TestClass:
    def __init__(self):
        self.s = ""

    def sayHi(self):
        print("hi")

def function(Class: TestClass):
    if not os.path.isdir(os.path.join("", "./inputfiles/")):
        os.mkdir(os.path.join("","./inputfiles/"))
        print(os.path.join(sys.argv[0], "./inputfiles/"))
    if not os.path.isdir("./outputfiles/"):
        os.mkdir("./outputfiles/")
    if not os.path.isdir("./tempobuffer/"):
        os.mkdir("./tempobuffer/")
    if not os.path.isdir("./mapreduce_mods /"):
        os.mkdir("./mapreduce_mods /")

function(TestClass)