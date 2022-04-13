#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
import sys
from typing import Tuple
from colorama import Fore, init
from AuWav import Spectrogrammer, AuWav
from Banner import display_banner
from Misc import better_hash


init(autoreset=True, convert=True)


def parse_arguments() -> Tuple[Namespace, ArgumentParser]:
    """Parses the arguments passed to the program.

    Args:
        None
    Returns:
        Namespace: holds the values of the parsed arguments
        ArgumentParser: The parser used to parse arguments
    """
    parser = ArgumentParser(
        description="""
        Hides data inside of audio files.
        """
    )

    # Select which algorithm to use. Must select exactly one algorithm.
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

    # Arguments that are sometimes required but difficult to express
    # requirements using argparse. These will be checked later.
    parser.add_argument(
        "-i", "--input", type=str, help="Input filename.", required=False
    )
    parser.add_argument(
        "-k",
        "--key",
        help="The key to decode a message from file",
        required=False,
    )
    parser.add_argument("--data", type=str, help="Data filename.", required=False)
    parser.add_argument(
        "-b", "--bits", type=int, help="The number of bits too decode", required=False
    )

    # Must either encode or decode but now both.
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encode", action="store_true")
    group.add_argument("-d", "--decode", action="store_true")

    # Optionally override output file.
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output filename",
        required=False,
        default="out.wav",
    )

    return parser.parse_args(), parser


def do_lsb(args: Namespace, parser: ArgumentParser) -> None:
    """Use the LSB algorithm to encode/decode data.

    Args:
        args (Namespace): holds the values of the algorithm's arguments
        parser (ArgumentParser): the parser used to parse the arguments
    Returns:
        None
    """
    # Make sure we have got the correct arguments to do lsb.
    if args.key is None:
        print(
            Fore.RED
            + "A key is required for the LSB algorithm. Please specify one using the --key flag."
        )
        sys.exit(1)
    if args.input is None:
        print(
            f"{Fore.RED}[!!] Error: No input file specified. Please specify one using the --input flag."
        )
        sys.exit(1)
    # Create a AuWav object with the arguments to be able to encode/decode data.
    au = AuWav(args.input, args.output)
    if args.encode:
        if args.data is None:
            print(
                f"{Fore.RED}[!!] Error: You need to provide some data to encode using the --data flag."
            )
            sys.exit(1)
        # Use hash on the key so it can take strings and ints.
        key = better_hash(args.key)
        au.encode(args.data, key=key)
    else:
        if args.bits is None:
            print(
                f"{Fore.RED}[!!] Error: You need to specify how many bits to decode from the file using the --bits flag."
            )
            sys.exit(1)
        # Use hash on the key so it can take strings and ints.
        key = better_hash(args.key)
        decoded_data = au.decode(args.bits, key=key)
        print(f"{Fore.MAGENTA}[DECODED]{Fore.RESET}:\n{decoded_data}")


def do_spectrogramming(args: Namespace, parser: ArgumentParser) -> None:
    """Use the Spectrogramming algorithm to encode/decode data.

    Args:
        args (Namespace): holds the values of the algorithm's arguments
        parser (ArgumentParser): the parser used to parse the arguments
    Returns:
        None
    """
    if args.encode:
        if args.data is None:
            print(
                f"{Fore.RED}[!!] Error: You need to provide some data to encode using the --data flag."
            )
            sys.exit(1)
        au = Spectrogrammer()
        au.encode(args.data, args.output)
    else:
        if args.input is None:
            print(
                f"{Fore.RED}[!!] Error: No input file specified. Please specify one using the --input flag."
            )
            sys.exit(1)
        au = Spectrogrammer()
        extracted = au.decode(args.input)
        print(f"{Fore.MAGENTA}[DECODED]{Fore.RESET}:\n{extracted.decode('utf8')}")


def main() -> None:
    """Start of the program

    Args:
        None
    Returns:
        None
    """
    display_banner(False)

    args, parser = parse_arguments()

    if args.lsb:
        do_lsb(args, parser)
    elif args.spectro:
        do_spectrogramming(args, parser)


if __name__ == "__main__":
    main()
