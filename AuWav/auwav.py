from random import Random
from typing import List, Tuple
import wave
from tqdm import tqdm, trange

from colorama import Fore

from AuWav.base import AuBase


class AuWav(AuBase):
    def __init__(self, filename: str, out_filename: str = "out.wav") -> None:
        super().__init__(filename, out_filename)
        self.fd = wave.open(self.filename, "rb")

    @staticmethod
    def bitgen(data):
        """Generates all bits from data."""
        for dat in data:
            for i in range(8):
                yield (dat >> i) & 0x1

    def read_all_bytes(self) -> List[int]:
        """Reads all bytes from file."""
        self.fd.setpos(0)
        print(f"{Fore.YELLOW}[*]{Fore.RESET} Loading data...")
        dat = []
        for _ in trange(self.fd.getnframes()):

            dat.append(int.from_bytes(self.fd.readframes(1), "big"))
        return dat

    def encode(self, data_toEncrypt: bytes, key: int) -> Tuple["AuWav", int]:
        """Encodes data with key."""
        out = wave.open(self.out_file, "wb")
        out.setnchannels(self.fd.getnchannels())
        out.setcomptype(self.fd.getcomptype(), self.fd.getcompname())
        out.setframerate(self.fd.getframerate())
        SAMP_SIZE = self.fd.getsampwidth()
        out.setsampwidth(SAMP_SIZE)

        rand = Random(key)
        USED = []

        BYTES = self.read_all_bytes()
        genBits = 0
        print(f"{Fore.YELLOW}[!]{Fore.RESET} Encoding file.")
        for bit in tqdm(self.bitgen(data_toEncrypt), total=len(data_toEncrypt) * 8):
            genBits += 1

            idx = rand.randint(0, len(BYTES) - 1)
            while idx in USED:
                idx = rand.randint(0, len(BYTES) - 1)

            if len(USED) == 0:
                idx2 = rand.randint(0, len(BYTES) - 1)
                while idx2 == idx:
                    idx2 = rand.randint(0, len(BYTES) - 1)
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
                    print(
                        "Hmm, some patternmatching error there is. :/\n\t- YOda (2022)"
                    )
                    exit(-1)

        print(f"{Fore.YELLOW}[!]{Fore.RESET} Writing encoded file.")
        data_toWrite = b""
        CHUCK_SIZE = 1024
        cnt = 0
        for byt in tqdm(BYTES):
            xxx = byt.to_bytes(SAMP_SIZE, "big")
            data_toWrite += xxx
            if cnt == CHUCK_SIZE:
                out.writeframes(data_toWrite)
                data_toWrite = b""
                cnt = 0
            cnt += 1
        out.writeframes(data_toWrite)

        return AuWav(self.out_file), genBits

    def decode(self, bits: int, key: int) -> str:
        """Decodes data with key."""
        BYTES = self.read_all_bytes()

        decrypted_data = b""

        rand = Random(key)
        USED = []

        byt = 0
        b_idx = 0
        print(f"{Fore.YELLOW}[!]{Fore.RESET} Decoding file.")
        for _ in trange(bits):

            idx = rand.randint(0, len(BYTES) - 1)
            while idx in USED:
                idx = rand.randint(0, len(BYTES) - 1)

            if len(USED) == 0:
                idx2 = rand.randint(0, len(BYTES) - 1)
                while idx2 == idx:
                    idx2 = rand.randint(0, len(BYTES) - 1)
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
            # return decrypted_data.decode("ascii")
            return decrypted_data.decode("utf-8")
        except UnicodeDecodeError:
            print(
                f"\n{Fore.CYAN}[SUGGESTION]{Fore.RESET} Possible wrong number of bits or data is in binary format."
            )
            return decrypted_data.decode("ansi")
