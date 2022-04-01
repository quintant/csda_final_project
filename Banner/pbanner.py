from colorama import Fore, Back
import Banner.gold_bar as gold_bar
from random import choice
import Banner.multi as multi


def display_banner(random=False):
    """
    Displays a random banner ASCII image.
    """
    options = [
        gold_bar.display,
        multi.display,
    ]
    img = choice(options)
    img()
    display_name()


def display_name():
    """
    Displays the name of the program in ANSI text.
    """
    name = [
        f"{Back.BLACK+Fore.MAGENTA: >35} ▄▄▄· ▄• ▄▌.▄▄ · ▄▄▄▄▄▄▄▄ . ▄▄ • ",
        f"{Back.BLACK+Fore.BLUE: >35}▐█ ▀█ █▪██▌▐█ ▀. •██  ▀▄.▀·▐█ ▀ ▪",
        f"{Back.BLACK+Fore.LIGHTBLUE_EX: >35}▄█▀▀█ █▌▐█▌▄▀▀▀█▄ ▐█.▪▐▀▀▪▄▄█ ▀█▄",
        f"{Back.BLACK+Fore.CYAN: >35}▐█ ▪▐▌▐█▄█▌▐█▄▪▐█ ▐█▌·▐█▄▄▌▐█▄▪▐█",
        f"{Back.BLACK+Fore.LIGHTCYAN_EX: >35} ▀  ▀  ▀▀▀  ▀▀▀▀  ▀▀▀  ▀▀▀ ·▀▀▀▀ ",
    ]
    for line in name:
        print(line)
