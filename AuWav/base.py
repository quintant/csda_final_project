


from abc import ABC
from typing import Tuple
import wave


class AuBase(ABC):
    """
    Base class for the encyption and decryption of audio files.
    """
    def __init__(self, input_filename:str, output_filename:str='out.wav') -> None:
        super().__init__()
        self.filename = input_filename
        self.out_file = output_filename
        

    def encode(self, data_toEncrypt: bytes, key: int) -> Tuple["AuBase", int]:
        raise NotImplementedError

    def decode(self, bits: int, key: int) -> str:
        raise NotImplementedError