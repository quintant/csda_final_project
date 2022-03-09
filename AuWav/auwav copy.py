from random import randint, random, uniform
import wave
import numpy as np
import pyaudio
from Misc.sinewave import create_sine_func


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
            yield (dat>>0) &0x1
            yield (dat>>1) &0x1
            yield (dat>>2) &0x1
            yield (dat>>3) &0x1
            yield (dat>>4) &0x1
            yield (dat>>5) &0x1
            yield (dat>>6) &0x1
            yield (dat>>7) &0x1

    def encode(self, data_toEncrypt:bytes) -> "AuWav":
        out = wave.open("out.wav", "wb")
        out.setnchannels(self.fd.getnchannels())
        out.setcomptype(self.fd.getcomptype(), self.fd.getcompname())
        out.setframerate(self.fd.getframerate())
        out.setsampwidth(self.fd.getsampwidth())
        self.fd.setpos(0)
        B_LEFT = self.fd.getnframes()
        for bit in self.bitgen(data_toEncrypt):
            dat1 = self.fd.readframes(1)
            dat2 = self.fd.readframes(1)
            dat1i = int.from_bytes(dat1, 'big')
            dat2i = int.from_bytes(dat2, 'big')

            match (dat1i - dat2i) %2, bit:
                case (0, 0)|(1,1):
                    b1 = dat1i
                    b2 = dat2i

                case (1, 0) | (0, 1):
                    b1 = dat1i
                    b2 = dat2i
                    # b1 = (b1 + 1) % 0xffff
                    if 0<= b2+1 <= 0xffff//2:
                        dix = 1
                    else:
                        dix = -1
                    b2 = (b2 + dix) % 0xffff

                case _:
                    print("FUCK there is a error.")                   
                    exit(-1)

            # o = (c + g) % 0xFFFF
            b1b = b1.to_bytes(2, 'big')
            b2b = b2.to_bytes(2, 'big')
            B_LEFT -= 2

            out.writeframes(b1b)
            out.writeframes(b2b)

        if B_LEFT:
            data_left = self.fd.readframes(B_LEFT)
            out.writeframes(data_left)
        return AuWav("out.wav")


    def decode(self, bytes_of_data) -> str:
        decrypted_data = b""
        self.fd.setpos(0)
        tmp = ''
        for _ in range(bytes_of_data):
            dat0 =[int.from_bytes(x, 'big') for x in [self.fd.readframes(1), self.fd.readframes(1)]]
            dat1 =[int.from_bytes(x, 'big') for x in [self.fd.readframes(1), self.fd.readframes(1)]]
            dat2 =[int.from_bytes(x, 'big') for x in [self.fd.readframes(1), self.fd.readframes(1)]]
            dat3 =[int.from_bytes(x, 'big') for x in [self.fd.readframes(1), self.fd.readframes(1)]]
            dat4 =[int.from_bytes(x, 'big') for x in [self.fd.readframes(1), self.fd.readframes(1)]]
            dat5 =[int.from_bytes(x, 'big') for x in [self.fd.readframes(1), self.fd.readframes(1)]]
            dat6 =[int.from_bytes(x, 'big') for x in [self.fd.readframes(1), self.fd.readframes(1)]]
            dat7 =[int.from_bytes(x, 'big') for x in [self.fd.readframes(1), self.fd.readframes(1)]]
            
            d0 = (dat0[1] - dat0[0]) %2
            d1 = (dat1[1] - dat1[0]) %2
            d2 = (dat2[1] - dat2[0]) %2
            d3 = (dat3[1] - dat3[0]) %2
            d4 = (dat4[1] - dat4[0]) %2
            d5 = (dat5[1] - dat5[0]) %2
            d6 = (dat6[1] - dat6[0]) %2
            d7 = (dat7[1] - dat7[0]) %2
            # print(f'y {d0}')
            # print(f'y {d1}')
            # print(f'y {d2}')
            # print(f'y {d3}')
            # print(f'y {d4}')
            # print(f'y {d5}')
            # print(f'y {d6}')
            # print(f'y {d7}')
            # byt = (d0<<7) | (d1<<6) | (d2<<5) | (d3<<4) | (d4<<3) | (d5<<2) | (d6<<1) | (d7<<0)
            byt = (d0<<0) + (d1<<1) + (d2<<2) + (d3<<3) + (d4<<4) + (d5<<5) + (d6<<6) + (d7<<7)
            byt = byt.to_bytes(1, 'little')
            
            # print(f"{byt=}")
            decrypted_data += byt
            # decrypted_data += chr(byt)

        return decrypted_data.decode('ascii')


    def close(self) -> None:
        """Closes everything gracefullys"""
        self.pyaudio.terminate()
