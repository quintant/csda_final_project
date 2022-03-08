

from glob import glob
from random import choice, randint
from colorama import Fore


def display():
    g = glob('Banner/multi/*')
    fname = g[randint(0, len(g)-1)]
    with open(fname) as f:
        for line in f.readlines():
            print(Fore.YELLOW+ line, end='')
    print()