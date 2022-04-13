#!/usr/bin/env python3

from base64 import b64decode, b64encode
import os
from typing import Dict
import numpy as np
import wavio
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
from colorama import Fore


# The IMG_SIZE and FONT_SIZE constants need to match. IMG_SIZE has to be large
# enough such that a character can be drawn in the image. The StringToCharImages
# class will check this for you but it assumes a monospace font.
IMG_SIZE = (31, 47)
FONT_SIZE = 50
# 44100 Hz is the default sample rate of wav files.
SAMPLE_RATE = 44100
# This combination of CHAR_DURATION and MIN_FREQ and MAX_FREQ is a good mix
# between being able to create the sound file fast, and being able to see/listen
# to the resulting spectrogram.
# How many seconds of sound to generate for each character.
CHAR_DURATION = 1
# The frequency range to draw characters in.
MIN_FREQ = 1000
MAX_FREQ = 5000


class Spectrogrammer:
    """
    A class that can:
    - write data to the spectrogram of an audio file,
    - extract text from the spectrogram of an audio file.
    See the encode and decode methods for more details.
    """

    class StringToCharImages:
        """
        A class that takes a string and converts each character of it into an image.
        """

        def __init__(
            self,
            text,
            font=ImageFont.truetype(
                # Becuase windows is stupid, we need to use a font that is pre-installed.
                "consola.ttf" if os.name == "nt" else "FiraCode-Regular.ttf",
                size=FONT_SIZE,
            ),  # Font is assumed to be monospace.
        ):
            self.text = text  # The text to convert to images.
            self.img_size = IMG_SIZE  # The size of each character as an image.
            self.font = font  # The font to use. Assumed to be monospace.
            if not text:
                raise ValueError("text must be non-empty.")
            if (
                font.getsize("A")[0] > self.img_size[0]
                or font.getsize("A")[1] > self.img_size[1]
            ):
                raise ValueError(
                    f"fontsize ({font.getsize('A')}) is too big for image ({self.img_size})"
                )

        def __iter__(self):
            """
            Yield each character in self.text as a binary image.

            Yields:
                PIL.Image.Image: the next character of self.text as an image.
            """
            for c in self.text:
                # Create an empty binary image.
                img = Image.new("1", self.img_size)
                # Draw the character on the image.
                d = ImageDraw.Draw(img)
                d.text((0, 0), c, fill="white", font=self.font)
                yield img

    def __init__(self):
        # Decompose IMG_SIZE.
        self.WIDTH, self.HEIGHT = IMG_SIZE
        # Each character will need CHAR_DURATION of audio.
        self.DURATION = CHAR_DURATION
        # To draw a character in the spectrogram, we process a column of the
        # character's image at a time. Calculate how much time each column
        # needs.
        self.DURATION_COL = self.DURATION / self.WIDTH
        # We limit the legal alphabet to base64. This allows us to hide binary
        # data without knowing how to track arbitrary bytes. It also makes it
        # easier to extract characters from a spectrogram as we know what to
        # look for.
        self.ALPHABET = (
            "ABCDEFGHIJKLMNOPQRSTUVWXUZabcdefghijklmnopqrstuvwxyz0123456789+/="
        )
        # A cache that stores how each character in our alphabet sounds.
        self.CHAR_LIBRARY = self._build_library(self.ALPHABET)

    def _build_library(self, alphabet) -> Dict[str, Image.Image]:
        """
        Precalculates how each character in alphabet sounds.

        Args:
            alphabet (str): a string defining which characters we will encode/decode.
        Returns:
            string -> PIL.Image.Image dict: a dictionary that takes a character
                and returns it as an image.
        """
        # Convert each character in our alphabet into an image.
        imger = self.StringToCharImages(alphabet)
        library = {}
        # Store how each character is as an image.
        print(f"{Fore.YELLOW}[!]{Fore.RESET} Generating alphabet cache")
        for c, img in tqdm(zip(alphabet, imger), total=len(alphabet)):
            library[c] = self.image_to_sound(img)
        return library

    def image_to_sound(self, img: Image.Image) -> np.ndarray:
        """
        Turns an image into an audio segment whose spectrogram contains the image.

        Args:
            img (PIL.Image.Image): the image to convert into sound
        Returns:
            np.ndarray (1d): the image as a audio byte stream
        """
        # Here we make an assumption. As this program is intended to write data
        # into the spectrogram of an audio file we really do not care about
        # depth in our image. To make the character in the image clearer we make
        # sure that the image is a binary image.
        img_array = np.array(img)
        img_array[img_array > 0] = 1
        # We will loop over the columns of the image but by default Python will
        # loop over rows. Transpose the image to simulate looping over columns.
        img_trans = np.transpose(img_array)

        # Convert each image column into an audio segment and combine the audio
        # segment to obtain an audio segment representing the whole image.
        audio_segment = np.hstack([self._column_to_sound(col) for col in img_trans])

        # We will be writing the audio segment as a wav file. Wav files use 16
        # bit audio samples. Normalize the audio segment to make sure that a)
        # values are actually 16 bit, b) the audio segment is not just a bunch
        # of low values.
        # Normalization code adapted from https://stackoverflow.com/a/1735122.
        # We need to make sure we do not divide by 0.
        audio_segment *= (2**15 - 1) / max(np.max(np.abs(audio_segment)), 1)
        audio_segment = audio_segment.astype(np.int16)

        return audio_segment

    def _column_to_sound(self, img_column: np.ndarray) -> np.ndarray:
        """
        Turns an image column into an audio segment whose spectrogram contains the image column.

        Args:
            img_columns (np.ndarray (1d)): a single column of an image to convert into sound
        Returns
            np.ndarray (1d): the column as a audio byte stream
        """
        # We want to create a single sound wave that represents the image
        # column. We use Fourier's theorem and sum up the sine waves
        # corresponding to the pixel values in the image column.

        # We start with an empty wave.
        total_waveform = self._pixel_to_sound(0, 0)

        # Convert each pixel to a sine wave, and add it to the running wave.
        for i, pixel_val in enumerate(img_column):
            # We need to count backwards, else the text in the spectrogram is
            # mirrored.
            total_waveform += self._pixel_to_sound(len(img_column) - i, pixel_val)

        return total_waveform

    def _pixel_to_sound(self, i: int, pixel_val: int) -> np.ndarray:
        """
        Turn a pixel's position and value in an image into a corresponding sine wave.

        Args:
            i (int): the position of the pixel on the y-axis (from the bottom)
            pixel_val (int): the pixel's integer value
        Returns:
            np.ndarray (1d): the pixel as a audio byte stream
        """
        # Map the pixel's position to a frequency between MIN_FREQ and MAX_FREQ.
        freq = MIN_FREQ + (MAX_FREQ - MIN_FREQ) / self.HEIGHT * i

        # Code based on https://stackoverflow.com/a/69152477.
        ts = np.linspace(
            start=0,
            stop=self.DURATION_COL,
            num=int(self.DURATION_COL * SAMPLE_RATE),
            endpoint=False,
        )
        sinewave = pixel_val * np.sin(2 * np.pi * freq * ts)

        return sinewave

    def encode(self, data_filename: str, out_filename: str) -> None:
        """
        Write base64 encoded bytes to an audio file's spectrogram. The
        resulting .wav file will be written to out_filename.

        Args:
            data_filename (str): path to the data file to encode.
            out_filename (str): path where the resulting audio file should be written
        Returns:
            None
        """
        # Read the data.
        with open(data_filename, "rb") as f:
            bytes_to_convert = f.read()
        # Convert the data to base64 format.
        b64text = b64encode(bytes_to_convert).decode()
        # Conver the data to images.
        imger = self.StringToCharImages(b64text)
        # Convert each character image to an audio segment and concatenate them.
        print(
            f"{Fore.YELLOW}[!]{Fore.RESET} Converting base64 encoded data to an audio stream"
        )
        audio = np.hstack(
            [self.image_to_sound(img) for img in tqdm(imger, total=len(b64text))]
        )
        # Write the resulting audio file.
        print(f"{Fore.YELLOW}[!]{Fore.RESET} Writing results to {out_filename}")
        wavio.write(out_filename, audio, SAMPLE_RATE, scale="none", sampwidth=2)

    def decode(self, filename: str) -> bytes:
        """
        Extract base64 encoded bytes from an audio file's spectrogram.

        Args:
            filename (str): the audio file from which to extract hidden data from
        Returns:
            bytes: the decoded bytes
        """
        data = wavio.read(filename).data.flatten()
        # Calculate how many bytes from the audio stream a single character takes.
        BYTES_PER_CHAR = int(self.DURATION_COL * SAMPLE_RATE) * self.WIDTH
        extracted_char_list = []
        # Split the audio byte stream into character sized chunks.
        print(
            f"{Fore.YELLOW}[!]{Fore.RESET} Extracting base64 encoded data from {filename}"
        )
        for char_arr in tqdm(
            np.split(data, data.shape[0] // BYTES_PER_CHAR),
            total=data.shape[0] // BYTES_PER_CHAR,
        ):
            # Use kNN to find the most similar character. By using kNN we can
            # extract the bytes from a audio file that has been compressed (but
            # not too much).
            highest_score = -1
            for c in self.ALPHABET:
                char_score = np.sum(self.CHAR_LIBRARY[c] == char_arr)
                if char_score > highest_score:
                    highest_score = char_score
                    most_likely_char = c
            extracted_char_list.append(most_likely_char)
        # The bytes we extracted are base64 encoded. Decode them before returning.
        b64text = "".join(extracted_char_list)
        return b64decode(b64text)
