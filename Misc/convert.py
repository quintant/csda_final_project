import os
import sys
from pydub import AudioSegment
from colorama import Fore

def convert(filename:str) -> str:
    """Convert audio/video file to a wav file.

    Args:
        filename (str): Takes in the filename of av-file

    Returns:
        str: Returns name of wav file.
    """
    
    

    if not os.path.exists(filename):
        print(f"{Fore.RED}[ERROR]:{Fore.RESET} The file you provided does not seem to exist.")
        exit(-1)
    gc = filename.split('.')
    name, f_type = ".".join(gc[:-1]), gc[-1]
    new_name = name + ".wav"
    if f_type != 'wav':
        new_audio_file = AudioSegment.from_file(filename)

        new_audio_file.export(new_name, format='wav')

    return new_name
                                                           

if __name__ == "__main__":
    from colorama import init
    # from ..Banner.banner import display_banner
    # display_banner()
    init(autoreset=True)
    filename = sys.argv[1]

    convert(filename)