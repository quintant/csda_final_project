from colorama import Fore
import Banner.pb_girl as pb_girl
import Banner.gold_bar as gold_bar
import Banner.crown as crown
from random import choice
import Banner.multi as multi


def display_banner(random=False):
    options = [
        # pb_girl.display,
        # gold_bar.display,
        # crown.display,
        multi.display,
    ]
    img = choice(options)
    img()
    display_name()


def display_name():
    name = [
        f"{Fore.CYAN: <35} ▄▄▄· ▄• ▄▌.▄▄ · ▄▄▄▄▄▄▄▄ . ▄▄ • ",
        f"{Fore.CYAN: <35}▐█ ▀█ █▪██▌▐█ ▀. •██  ▀▄.▀·▐█ ▀ ▪",
        f"{Fore.CYAN: <35}▄█▀▀█ █▌▐█▌▄▀▀▀█▄ ▐█.▪▐▀▀▪▄▄█ ▀█▄",
        f"{Fore.CYAN: <35}▐█ ▪▐▌▐█▄█▌▐█▄▪▐█ ▐█▌·▐█▄▄▌▐█▄▪▐█",
        f"{Fore.CYAN: <35} ▀  ▀  ▀▀▀  ▀▀▀▀  ▀▀▀  ▀▀▀ ·▀▀▀▀ ",
    ]
    for line in name:
        print(line)
