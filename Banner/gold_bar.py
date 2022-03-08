from colorama import Fore, init


def display():
    init(autoreset=True)
    dat = [
        f"{Fore.YELLOW}                    ████        ",
        f"{Fore.YELLOW}              ██████    ██      ",
        f"{Fore.YELLOW}        ██████            ██    ",
        f"{Fore.YELLOW}  ██████                    ██  ",
        f"{Fore.YELLOW}██                  ▓▓▓▓▓▓▓▓▓▓██",
        f"{Fore.YELLOW}██▓▓          ▓▓▓▓▓▓░░░░░░░░░░██",
        f"{Fore.YELLOW}██░░▓▓  ▓▓▓▓▓▓░░░░░░░░░░░░░░░░██",
        f"{Fore.YELLOW}██░░░░▓▓░░░░░░░░░░░░░░░░░░░░░░██",
        f"{Fore.YELLOW}██░░░░░░░░░░░░░░░░░░░░░░██████  ",
        f"{Fore.YELLOW}  ██░░░░░░░░░░░░░░██████        ",
        f"{Fore.YELLOW}    ██░░░░░░██████              ",
        f"{Fore.YELLOW}      ██████                    ",
    ]
    for line in dat:
        print(line)
