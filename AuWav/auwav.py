#!/usr/bin/env python3

from random import Random
from typing import List
import wave
import sys
from tqdm import tqdm, trange

from colorama import Fore


class AuWav:
    """
    Class that does LSB steganography (encoding and decoding) with randomness.
    See the encode and decode methods for more details.
    """

    def __init__(self, filename: str, out_filename: str = "out.wav") -> None:
        self.filename = filename
        self.out_filename = out_filename
        try:
            self.fd = wave.open(self.filename, "rb")
        except Exception as e:
            raise TypeError(f"{self.filename} is not a valid .wav file") from e

    @staticmethod
    def bitgen(data):
        """
        Generates all bits from data.

        Args:
            data (bytes): the data stream to convert to a bit stream
        Yields:
            int: the next bit in the data stream
        """
        for dat in data:
            for i in range(8):
                yield (dat >> i) & 0x1

    def read_all_bytes(self) -> List[int]:
        """
        Reads all the bytes from the audio file into a list.

        Args:
            None
        Returns:
            int list: the audio stream bytes from self.fd
        """
        self.fd.setpos(0)
        print(f"{Fore.YELLOW}[*]{Fore.RESET} Loading data...")
        dat = []
        for _ in trange(self.fd.getnframes()):
            dat.append(int.from_bytes(self.fd.readframes(1), "big"))
        return dat

    def encode(self, data_filename: str, key: int) -> int:
        """
        Encodes (hides) data with key. The resulting .wav file is stored at
        self.out_filename.

        Args:
            data_filename (str): path to the data file to encode
            key (int): the key used to initialize a pseudo-random number generator
        Returns:
            int: the number of bits encoded
        """
        with open(data_filename, "rb") as f:
            data_toEncrypt = f.read()
        # Need to create a new file to write to wich has the same properties as the original file.
        out = wave.open(self.out_filename, "wb")
        out.setnchannels(self.fd.getnchannels())
        out.setcomptype(self.fd.getcomptype(), self.fd.getcompname())
        out.setframerate(self.fd.getframerate())
        # Sample size is just how many bytes each integer is.
        SAMP_SIZE = self.fd.getsampwidth()
        out.setsampwidth(SAMP_SIZE)

        # Need to create a random class which will be used to generate
        # pseudo-random numbers based on the key.
        rand = Random(key)
        # List to keep track of useed indices.
        USED = []
        # List to keep track of the data to be encrypted.
        BYTES = self.read_all_bytes()
        # A variable to keep track of how many bits have been encoded.
        genBits = 0

        print(f"{Fore.YELLOW}[!]{Fore.RESET} Encoding file.")
        for bit in tqdm(self.bitgen(data_toEncrypt), total=len(data_toEncrypt) * 8):
            genBits += 1

            # Generate a random index.
            idx = rand.randint(0, len(BYTES) - 1)
            # Make sure we don't use the same index twice.
            while idx in USED:
                idx = rand.randint(0, len(BYTES) - 1)

            if len(USED) == 0:
                # If it's the first bit, we need to generate a second index.
                idx2 = rand.randint(0, len(BYTES) - 1)
                while idx2 == idx:
                    idx2 = rand.randint(0, len(BYTES) - 1)
            else:
                # If it's not the first bit, we need to use a random index from the list of used indices.
                idx2 = rand.choice(USED)

            # Get the bytes at the selected indices.
            dat1 = BYTES[idx]
            dat2 = BYTES[idx2]

            # Mark the indices as used.
            USED.append(idx)
            USED.append(idx2)

            # Check if we need to change the bytes to encode the bit.
            match (dat1 - dat2) % 2, bit:
                # The bits match, so we don't need to change the data.
                case (0, 0) | (1, 1):
                    continue

                # The bits don't match, so we need to change the data.
                case (1, 0) | (0, 1):
                    gx = 1
                    # Lessen the impact of modifying value.
                    if dat1 < 0xFFFF // 2:
                        gx = +1
                    else:
                        gx = -1
                    # Change the data so the bits match.
                    BYTES[idx] = (dat1 + gx) % 0x10000

                # This should not happen in any case.
                case _:
                    print(
                        "Hmm, some patternmatching error there is. :/\n\t- YOda (2022)"
                    )
                    sys.exit(-1)

        print(f"{Fore.YELLOW}[!]{Fore.RESET} Writing encoded file {self.out_filename}.")
        data_toWrite = b""
        # Writing the data in chunks gives a better performance.
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

        print(f"{Fore.CYAN}[!]{Fore.RESET}: Encoded {genBits} bits")

        return genBits

    def decode(self, bits: int, key: int) -> bytes:
        """
        Decodes data with key.

        Args:
            bits (int): the number of bits to decode
            key (int): the key used to initialize a pseudo-random number generator
        Returns:
            str: the decoded string (if utf-8 data)
            bytes: the decoded bytes (if not utf-8 data)
        """
        # List to keep track of the data to be decoded.
        BYTES = self.read_all_bytes()

        # Decrypted data.
        decoded_data = b""

        # Need to create a random class which will be used to generate
        # psuedo-random numbers based on the key. Has to be the same key that
        # was used to encode the data, otherwise the decoding will fail.
        rand = Random(key)

        # List to keep track of used indices.
        USED = []

        # A temp variable to keep track of decoded bits.
        byt = 0
        # How many bits have been decoded and stored in byt.
        b_idx = 0

        print(f"{Fore.YELLOW}[!]{Fore.RESET} Decoding file.")
        for _ in trange(bits):

            # Generate the indexing in the same way as in encode.
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

            # Extract the bits from the data.
            diff = (dat1 - dat2) % 2
            byt += diff << b_idx
            # When we've extracted 8 bits, we can store that byte in the decoded data.
            if b_idx == 7:
                decoded_data += byt.to_bytes(1, "little")
                byt = 0
                b_idx = 0
            else:
                b_idx += 1
        try:
            # If the data in text format we display it in text format.
            return decoded_data.decode("utf-8")
        except UnicodeDecodeError:
            # If the data in binary format we display it in binary format.
            print(
                f"\n{Fore.CYAN}[SUGGESTION]{Fore.RESET} Possible wrong number of bits or wrong key (or data is in binary format)."
            )
            return decoded_data
