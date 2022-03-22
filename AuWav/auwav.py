from random import Random, choice, randint, random, uniform
from typing import List, Tuple
import wave
import pyaudio
from Misc.sinewave import create_sine_func
from tqdm import tqdm, trange

from colorama import Fore


class AuWav:
    def __init__(self, filename: str, chunk_size: int = 1024) -> None:
        self.filename = filename
        self.fd = wave.open(self.filename, "rb")
        self.pyaudio = pyaudio.PyAudio()
        self.chunk_size = chunk_size
        self.stream = self.pyaudio.open(
            format=self.pyaudio.get_format_from_width(self.fd.getsampwidth()),
            channels=self.fd.getnchannels(),
            rate=self.fd.getframerate(),
            output=True,
        )

    def play(self) -> None:

        while data := self.fd.readframes(self.chunk_size):
            self.stream.write(data)

    @staticmethod
    def bitgen(data):
        for dat in data:
            for i in range(8):
                yield (dat >> i) & 0x1

    def read_all_bytes(self) -> List[int]:
        self.fd.setpos(0)
        print(f"{Fore.YELLOW}[*]{Fore.RESET} Loading data...")
        dat = []
        for _ in trange(self.fd.getnframes()):

            dat.append(int.from_bytes(self.fd.readframes(1), "big"))
        return dat

    def encode(self, data_toEncrypt: bytes, key: int) -> Tuple["AuWav", int]:
        out = wave.open("out.wav", "wb")
        out.setnchannels(self.fd.getnchannels())
        out.setcomptype(self.fd.getcomptype(), self.fd.getcompname())
        out.setframerate(self.fd.getframerate())
        out.setsampwidth(self.fd.getsampwidth())

        rand = Random(key)
        USED = []

        BYTES = self.read_all_bytes()
        genBits = 0
        print(f"{Fore.YELLOW}[!]{Fore.RESET} Encoding file.")
        for bit in tqdm(self.bitgen(data_toEncrypt), total=len(data_toEncrypt) * 8):
            genBits += 1

            idx = rand.randint(0, len(BYTES))
            while idx in USED:
                idx = rand.randint(0, len(BYTES))

            if len(USED) == 0:
                idx2 = rand.randint(0, len(BYTES))
                while idx2 == idx:
                    idx2 = rand.randint(0, len(BYTES))
            else:
                idx2 = rand.choice(USED)

            dat1 = BYTES[idx]
            dat2 = BYTES[idx2]

            USED.append(idx)
            USED.append(idx2)

            match (dat1 - dat2) % 2, bit:
                case (0, 0) | (1, 1):
                    continue

                case (1, 0) | (0, 1):
                    gx = 1
                    # Lessen the impact of modifying value.
                    if dat1 <= 0xFFFF // 2:
                        gx = +1
                    else:
                        gx = -1
                    BYTES[idx] = (dat1 + gx) % 0x10000

                case _:
                    print("FUCK there is a error.")
                    exit(-1)

        print(f"{Fore.YELLOW}[!]{Fore.RESET} Writing encoded file.")
        data_toWrite = b''
        for byt in tqdm(BYTES):
            xxx = byt.to_bytes(2, "big")
            data_toWrite += xxx
        out.writeframes(data_toWrite)

        return AuWav("out.wav"), genBits

    def decode(self, bits: int, key: int) -> str:
        BYTES = self.read_all_bytes()

        decrypted_data = b""

        rand = Random(key)
        USED = []

        byt = 0
        b_idx = 0
        print(f"{Fore.YELLOW}[!]{Fore.RESET} Decoding file.")
        for _ in trange(bits):

            idx = rand.randint(0, len(BYTES))
            while idx in USED:
                idx = rand.randint(0, len(BYTES))

            if len(USED) == 0:
                idx2 = rand.randint(0, len(BYTES))
                while idx2 == idx:
                    idx2 = rand.randint(0, len(BYTES))
            else:
                idx2 = rand.choice(USED)

            dat1 = BYTES[idx]
            dat2 = BYTES[idx2]

            USED.append(idx)
            USED.append(idx2)

            diff = (dat1 - dat2) % 2
            byt += diff << b_idx
            if b_idx == 7:
                decrypted_data += byt.to_bytes(1, "little")
                byt = 0
                b_idx = 0
            else:
                b_idx += 1
        try:
            return decrypted_data.decode("ascii")
        except UnicodeDecodeError:
            print(f"{Fore.CYAN}[SUGGESTION]{Fore.RESET} Possible wrong number of bits or data is in binary format.")
            return decrypted_data.decode('ansi')


    def close(self) -> None:
        """Closes everything gracefullys"""
        self.pyaudio.terminate()
