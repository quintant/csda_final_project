from AuWav.auwav import AuWav
from colorama import Fore


def encode(au, filename, key) -> AuWav:
    """Wrappper for encoding a message in audio file.

    Args:
        au (AuWav): Audio file to hide the data inside.
        filename (str): Filename containing the data to hide.
        key (int): They decryptor key.

    Returns:
        AuWav: Audio file with the hidden data.
    """    
    with open(filename) as f:
        data = f.read()
        data = data.encode('ascii')
        n_au, bits = au.encode(data, key=key)
        print(f"{Fore.CYAN}[!]{Fore.RESET}: Encoded {bits} bits")
        return n_au


def decode(au: AuWav, bits:int, key:int) -> AuWav:
    """Wrappper for decoding a message.

    Args:
        au (AuWav): AuWav class which contains a hidden message.s
        bits (int): How many bits to decode.
        key (int): The decryptor key.

    Returns:
        str: Decoded data if the bits and key was correct.
    """    
    decoded_data = au.decode(bits, key=key)
    print(f"{Fore.MAGENTA}[DECODED]{Fore.RESET}:\n{decoded_data}")
    return decoded_data