from argparse import ArgumentParser, Namespace
from sys import argv
from colorama import Fore, init
from Banner import banner


init(autoreset=True)


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Parse arguments.")

    parser.add_argument(
        "-i", "--input", type=str, help="Input filename.", required=True
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output filename",
        required=False,
        default="out.wav",
    )

    # Mutually exclusive enc/dec
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", action="store_true")
    group.add_argument("-d", "--decrypt", action="store_true")

    return parser.parse_args()


def main(argv) -> None:
    """Start of the program

    Args:
        args (list): List of arguments passed to the program
    """
    banner.display_banner(False)


    args = parse_arguments()
    print(args)

    if args.e:
        pass
    else:
        pass



if __name__ == "__main__":
    main(argv[1:])
