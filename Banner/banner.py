from colorama import Fore
import Banner.pb_girl as pb_girl
import Banner.gold_bar as gold_bar
import Banner.crown as crown
import Banner.ass as ass


def display_banner(random=False):
    # pb_girl.display()
    # gold_bar.display()
    crown.display()
    # ass.display()

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
