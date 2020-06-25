from classes.MasterNode import MasterNode
from classes.tests.TestInputInterface import TestInputInterface
from classes.CLI import CLI

def main():
    command_line_interface = CLI()
    #command_line_interface = TestInputInterface()
    is_production = False
    ms = MasterNode(command_line_interface, is_production)
    ms.start()


if __name__ == '__main__':
    main()