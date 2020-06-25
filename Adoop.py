import os, sys
from classes.MasterNode import MasterNode
from classes.tests.TestInputInterface import TestInputInterface
from classes.CLI import CLI

def main():
    # Init data file directories
    maindir = os.path.dirname(__file__)
    print("MAINDIR:", maindir)
    init_data_dirs(maindir)

    # Set up a master node
    is_production = True
    command_line_interface = CLI()
    ms = MasterNode(command_line_interface, is_production)
    ms.start()

def init_data_dirs(maindir):
    print("Checking if data storage directories exist...")
    print(os.path.join(maindir, "inputfiles/"))
    os.makedirs(os.path.join(maindir, "inputfiles/"), exist_ok=True)
    os.makedirs(os.path.join(maindir, "outputfiles/"), exist_ok=True)
    os.makedirs(os.path.join(maindir, ("tempobuffer")), exist_ok=True)
    os.makedirs(os.path.join(maindir, "mapreduce_mods/"), exist_ok=True)
    print("Done checking.")

if __name__ == '__main__':
    main()