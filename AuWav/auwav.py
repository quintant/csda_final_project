from ast import For
from random import Random, randint, random, uniform
from typing import List, Tuple
import wave
import numpy as np
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

    def fuck(self) -> "AuWav":
        out = wave.open("out.wav", "wb")
        out.setnchannels(self.fd.getnchannels())
        out.setcomptype(self.fd.getcomptype(), self.fd.getcompname())
        out.setframerate(self.fd.getframerate())
        out.setsampwidth(self.fd.getsampwidth())
        self.fd.setpos(0)
        for _ in range(self.fd.getnframes()):
            c_frame = self.fd.readframes(1)
            cHex = c_frame.hex()
            gHex = b"\xec\x01".hex()
            c = int(cHex, base=16)
            g = int(gHex, base=16)
            g = randint(0, 1)
            p = c_frame
            # if random() > 0.98:
            o = (c + g) % 0xFFFF
            p = o.to_bytes(2, "big")

            out.writeframes(p)
        return AuWav("out.wav")

    def write_sine(self) -> "AuWav":
        out = wave.open("out.wav", "wb")
        out.setnchannels(1)
        out.setcomptype("NONE", "Not compressed")
        out.setframerate(44100)
        out.setsampwidth(2)
        amp = 10
        # frq = 30
        # sine = create_sine_func(
        #     frequency=30, ampitude=amp, sample_freq=out.getframerate()
        # )

        frq = 50
        for cnt in range(out.getframerate() * 2):
            sine = create_sine_func(
                frequency=frq, ampitude=amp, sample_freq=out.getframerate()
            )
            frq += frq/out.getframerate()
            sin = sine(cnt)
            # o = int(1 if sin>0 else 0) & 0xFFFF # Square wave
            o = round(sin) % 0xFFFF # Sine wave
            print(o)
            p = o.to_bytes(out.getsampwidth(), "big")
            out.writeframes(p)
        return AuWav("out.wav")

    @staticmethod
    def bitgen(data):
        for dat in data:
            for i in range(8):
                yield (dat>>i) &0x1

    def read_all_bytes(self) -> List[int]:
        self.fd.setpos(0)
        return [int.from_bytes(self.fd.readframes(1), 'big') for _ in range(self.fd.getnframes())]

    def encode(self, data_toEncrypt:bytes, key:int) -> Tuple["AuWav", int]:
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
        for bit in tqdm(self.bitgen(data_toEncrypt), total=len(data_toEncrypt)*8):
            genBits += 1

            idx = rand.randint(0, len(BYTES))
            while idx in USED:
                idx = rand.randint(0, len(BYTES))

            # idx2 = (idx+1) % len(BYTES)
            idx2 = rand.randint(0, len(BYTES))
            while idx2 == idx:
                idx2 = rand.randint(0, len(BYTES))

            dat1 = BYTES[idx]
            dat2 = BYTES[idx2]

            USED.append(idx)
            USED.append(idx2)

            match (dat1 - dat2) %2, bit:
                case (0, 0)|(1,1):
                    continue

                case (1, 0)|(0, 1):
                    BYTES[idx] = (dat1+1) % 0x10000
                        
                case _:
                    print("FUCK there is a error.")                   
                    exit(-1)

            
        print(f"{Fore.YELLOW}[!]{Fore.RESET} Writing encoded file.")
        for byt in tqdm(BYTES):
            xxx = byt.to_bytes(2, 'big')
            out.writeframes(xxx)

        return AuWav("out.wav"), genBits


    def decode(self, bits:int, key:int) -> str:
        BYTES = self.read_all_bytes()

        decrypted_data = b""
        
        rand = Random(key)
        USED = []

        byt = 0
        b_idx = 0
        print(f"{Fore.CYAN}[!]{Fore.RESET} Decoding file.")
        for _ in trange(bits):
            idx = rand.randint(0, len(BYTES))
            while idx in USED:
                idx = rand.randint(0, len(BYTES))

            # idx2 = (idx+1) % len(BYTES)
            idx2 = rand.randint(0, len(BYTES))
            while idx2 == idx:
                idx2 = rand.randint(0, len(BYTES))

            dat1 = BYTES[idx]
            dat2 = BYTES[idx2]
            
            USED.append(idx)
            USED.append(idx2)

            diff = ((dat1 - dat2) % 2)
            byt += (diff << b_idx)
            if b_idx == 7:
                decrypted_data += byt.to_bytes(1, 'little')
                byt = 0
                b_idx = 0
            else:
                b_idx+=1

        # print(decrypted_data)
        return decrypted_data.decode('ascii')


    def close(self) -> None:
        """Closes everything gracefullys"""
        self.pyaudio.terminate()
