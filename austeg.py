from argparse import ArgumentParser, Namespace
from sys import argv
from colorama import Fore, init
from AuWav import Spectrogrammer, AuWav
from Banner import display_banner
from DEncode.dencode import decode, encode
from Misc import better_hash


init(autoreset=True, convert=True)


def parse_arguments() -> Namespace:
    """Parses the arguments passed to the program"""
    parser = ArgumentParser(
        description="""
        Hides data inside of audio files.
        """
    )

    # Select which algorithm to use
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-lsb", help="Use LSB algorithm", action="store_true", dest="lsb", default=False
    )
    group.add_argument(
        "-spectro",
        help="Use Spectrogram algorithm",
        action="store_true",
        dest="spectro",
        default=False,
    )

    # Sometimes required args.
    parser.add_argument(
        "-i", "--input", type=str, help="Input filename.", required=False
    )
    parser.add_argument(
        "-k",
        "--key",
        # type=int,
        help="The key to decode a message from file",
        required=False,
    )
    parser.add_argument("--data", type=str, help="Data filename.", required=False)
    parser.add_argument(
        "-b", "--bits", type=int, help="The number of bits too decode", required=False
    )

    # Mutually exclusive enc/dec
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", action="store_true")
    group.add_argument("-d", "--decrypt", action="store_true")

    # Optional arguments
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output filename",
        required=False,
        default="out.wav",
    )

    return parser.parse_args(), parser


def main(argv) -> None:
    """Start of the program

    Args:
        args (list): List of arguments passed to the program
    """
    display_banner(False)

    args, parser = parse_arguments()
    # print(args)
    # au = AuWav(args.input)

    if args.lsb:
        if args.key is None:
            print(Fore.RED + "Key required for LSB algorithm")
            parser.print_help()
            exit(1)
        if args.input is None:
            print(f"{Fore.RED}[!!] Error: No input file specified")
            parser.print_help()
            exit(1)
        au = AuWav(args.input, args.output)
        if args.encrypt:
            if args.data is None:
                print(f"{Fore.RED}[!!] You need to provide some data to encode.")
                parser.print_help()
                exit(1)
            seed = better_hash(args.key)
            n_au = encode(
                au, args.data, seed
            )  # Use hash on the key so it can take strings and ints.
        else:
            if args.bits is None:
                print(
                    f"{Fore.RED}[!!] You need to specify how many bits to decode from the file."
                )
                parser.print_help()
                exit(1)
            seed = better_hash(args.key)
            decoded = decode(au, args.bits, seed)
    elif args.spectro:
        if args.encrypt:
            if args.data is None:
                print(f"{Fore.RED}[!!] You need to provide some data to encode.")
                parser.print_help()
                exit(1)
            au = Spectrogrammer(args.output)
            with open(args.data, "rb") as f:
                data = f.read()
                au.encode(data, args.output)
        else:
            au = Spectrogrammer(args.input)
            extracted = au.decode()
            print(f"{Fore.MAGENTA}[DECODED]{Fore.RESET}:\n{extracted.decode('utf8')}")


if __name__ == "__main__":
    main(argv[1:])
