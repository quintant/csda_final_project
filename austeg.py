from argparse import ArgumentParser, Namespace
from ast import arg
from sys import argv
from colorama import Fore, init
from AuWav.auwav import AuWav
from Banner import banner
from DEncode.dencode import decode, encode


init(autoreset=True, convert=True)


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        description="""
        Hides data inside of audio files.
        """)

    # Required arguments
    parser.add_argument(
        "-i", "--input", type=str, help="Input filename.", required=True
    )
    parser.add_argument(
        "-k",
        "--key",
        type=int,
        help="The key to decode a message from file",
        required=True,
    )

    # Mutually exclusive enc/dec
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", action="store_true")
    group.add_argument("-d", "--decrypt", action="store_true")

    # Optional arguments
    parser.add_argument("--data", type=str, help="Data filename.", required=False)
    parser.add_argument(
        "-b", "--bits", type=int, help="The number of bits too decode", required=False
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output filename",
        required=False,
        default="out.wav",
    )
    
    return parser.parse_args()


def main(argv) -> None:
    """Start of the program

    Args:
        args (list): List of arguments passed to the program
    """
    banner.display_banner(False)

    args = parse_arguments()
    # print(args)
    au = AuWav(args.input)
    if args.encrypt:
        if args.data is None:
            print(f"{Fore.RED}[!!] You need to provide some data to encode.")
            exit(1)
        n_au = encode(au, args.data, args.key)
    else:
        if args.bits is None:
            print(
                f"{Fore.RED}[!!] You need to specify how many bits to decode from the file."
            )
            exit(1)
        decoded = decode(au, args.bits, args.key)


if __name__ == "__main__":
    main(argv[1:])
