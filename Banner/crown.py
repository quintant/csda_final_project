from colorama import Fore, init


def display():
    init(autoreset=True)
    dat = [
f"                                                                    ██████████                  ",
f"{Fore.YELLOW}                    ████         {Fore.RESET}                             ██████▒▒▒▒▒▒▒▒▒▒████  ████████    ",
f"{Fore.YELLOW}              ██████    ██       {Fore.RESET}                             ██▒▒▒▒▓▓▓▓██▒▒▒▒▒▒▒▒██░░██▒▒▒▒██  ",
f"{Fore.YELLOW}        ██████            ██     {Fore.RESET}                               ██████████▒▒▒▒▒▒▒▒▓▓██▒▒██▒▒▒▒██",
f"{Fore.YELLOW}  ██████                    ██   {Fore.RESET}                               ██░░░░░░██▒▒▒▒▒▒▓▓▓▓██▒▒██▒▒▓▓██",
f"{Fore.YELLOW}██                  ▓▓▓▓▓▓▓▓▓▓██ {Fore.RESET}                             ██░░░░░░▒▒██░░▒▒▒▒▓▓▓▓▒▒████▓▓▓▓██",
f"{Fore.YELLOW}██▓▓          ▓▓▓▓▓▓░░░░░░░░░░██ {Fore.RESET}                             ██░░░░██░░██▒▒▒▒▒▒░░▒▒▒▒██▓▓▓▓▓▓██",
f"{Fore.YELLOW}██░░▓▓  ▓▓▓▓▓▓░░░░░░░░░░░░░░░░██ {Fore.RESET}                           ██░░░░░░░░████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓██",
f"{Fore.YELLOW}██░░░░▓▓░░░░░░░░░░░░░░░░░░░░░░██ {Fore.RESET}                           ██▒▒▒▒░░░░░░██▒▒▓▓▓▓▓▓▓▓██  ██▓▓██  ",
f"{Fore.YELLOW}██░░░░░░░░░░░░░░░░░░░░░░██████   {Fore.RESET}                           ██░░░░░░░░░░██▒▒▓▓▓▓▓▓██    ██▓▓██  ",
f"{Fore.YELLOW}  ██░░░░░░░░░░░░░░██████         {Fore.RESET}                             ██░░░░░░░░██▓▓▓▓████        ██▓▓██",
f"{Fore.YELLOW}    ██░░░░░░██████               {Fore.RESET}                       ████  ██░░░░░░░░██████            ██▓▓██",
f"{Fore.YELLOW}      ██████                     {Fore.RESET}                     ██░░████░░░░░░████                    ████",
f"                                                    ██████░░██░░████░░░░██                      ",
f"                                                  ██░░░░░░▒▒░░██░░░░░░░░██                      ",
f"                                ░░░░              ██░░░░▒▒▒▒░░░░░░██░░░░██                      ",
f"                              ▓▓░░░░▒▒██          ██▒▒▒▒▒▒▒▒░░░░▒▒▓▓░░░░██                      ",
f"                            ██░░░░░░░░░░████        ██▒▒██▒▒▒▒▒▒▒▒██░░░░██                      ",
f"                            ██░░░░░░░░░░░░░░██      ██░░▒▒██████▒▒██░░░░██                      ",
f"                          ██░░░░░░██░░░░░░░░░░██  ██░░░░░░▒▒▒▒▒▒████░░░░██                      ",
f"                          ██░░░░██  ██░░░░░░░░░░██░░░░░░░░░░▒▒██  ██░░░░██                      ",
f"                        ██▒▒░░░░██    ██░░░░░░░░██▒▒░░░░░░▒▒▒▒██    ██░░▒▒██                    ",
f"                        ██░░░░██        ██░░░░░░██▒▒░░░░▒▒▒▒▒▒██    ██░░░░██                    ",
f"                      ██░░░░██            ▒▒░░░░██▒▒▒▒▒▒████████    ██░░░░▒▒                    ",
f"                      ██░░██                ████░░██▒▒██░░▒▒▒▒██      ██░░██                    ",
f"                    ██░░░░██    ████████▒▒██░░░░░░░░░░░░░░░░░░██      ██░░██                    ",
f"████              ██░░░░████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██      ██░░██                    ",
f"██░░████████████████████░░▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██      ██░░▒▒████████            ",
f"██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████████████░░░░░░░░░░██        ██░░░░▒▒▒▒░░██            ",
f"  ██░░░░░░░░░░██████████████████████              ██████████            ██████████              ",
f"    ████░░░░██                                                                                  ",
f"        ████                                                                                    ",
]
    for line in dat:
        # print(Fore.YELLOW + line)
        print(line)
