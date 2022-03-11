from AuWav.auwav import AuWav
from colorama import Fore


def encode(au, filename, key) -> AuWav:
    with open(filename) as f:
        data = f.read()
        data = data.encode('ascii')
        n_au, bits = au.encode(data, key=key)
        print(f"{Fore.CYAN}[!]{Fore.RESET}: Encoded {bits} bits")
        return n_au


def decode(au, bits, key) -> AuWav:
    decoded_data = au.decode(bits, key=key)
    print(f"{Fore.CYAN}[DECODED]{Fore.RESET}: {decoded_data}")
    return decoded_data