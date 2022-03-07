from getopt import GetoptError, getopt
from sys import argv
from colorama import Fore, init
init(autoreset=True)


def main(argv) -> None:
    """Start of the program

    Args:
        args (list): List of arguments passed to the program
    """
    try:
        opts, args = getopt(argv, "i:o")
    except GetoptError:
        print("Broken arguments.")
        print(f"{Fore.RED}Git gud")
        print("Usage:")
        print("Required:")
        print("\t -i Input filename")
        print("Optional:")
        print("\t -o Output filename")


if __name__ == "__main__":
    main(argv[1:])
