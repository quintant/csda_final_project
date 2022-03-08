from colorama import Fore

def print_usage() -> None:
    """Print usage
    """
    print("Broken arguments.")
    print(f"{Fore.RED}Git gud")
    print("Usage:")
    print("Required:")
    print("\t -i Input filename")
    print("Optional:")
    print("\t -o Output filename")