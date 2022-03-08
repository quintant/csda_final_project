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
        out.setframerate(44100 * 2)
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
            o = int(1 if sin>0 else 0) & 0xFFFF # Square wave
            # o = round(sin) % 0xFFFF # Sine wave
            p = o.to_bytes(out.getsampwidth(), "big")
            out.writeframes(p)
        return AuWav("out.wav")

    def close(self) -> None:
        """Closes everything gracefullys"""
        self.pyaudio.terminate()
