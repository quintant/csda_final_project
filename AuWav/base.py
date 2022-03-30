


from abc import ABC
from typing import Tuple
import wave


class AuBase(ABC):
    def __init__(self, filename:str, ) -> None:
        super().__init__()
        self.filename = filename
        self.fd = wave.open(self.filename, "rb")

    def encode(self, data_toEncrypt: bytes, key: int) -> Tuple["AuBase", int]:
        raise NotImplementedError

    def decode(self, bits: int, key: int) -> str:
        raise NotImplementedError