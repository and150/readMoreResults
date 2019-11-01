from datescompare import *

class test_item:
    def __init__(self, *args):
        self.args = args

        self.well = args[0]   # well name
        self.start = args[1]  # test start time
        self.stop = args[2]   # test stop time
        self.wt = args[3]     # well test number

    def print_item(self):
        for x in self.args:
            print(f'{x}', end= " ")
        print()

class test_items:
    def __init__(self):
        self.items_list = []

    def get_items_list(self, filename, SDAT):
        lines = [line.rstrip('\n') for line in open(filename)]
        for x in lines:
            if len(x) > 0:
                words = x.split()
                self.items_list.append(test_item( words[0],
                    date2days(words[1] + " " + words[2], SDAT),
                    date2days(words[3] + " " + words[4], SDAT),
                    words[5] ))
