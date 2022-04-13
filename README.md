# Audio Steganography - T-742-CSDA Final Project

## Authors
  - **Bjarni Dagur Thor Kárason** <bjarnidt19@ru.is>
  - **Sigurjón Ingi Jónsson** <sigurjonj20@ru.is>

# About
This document describes how to run `austeg`, the implementation of our final project in T-742-CSDA (spring 2022) taught by Dr. Jacky Mallett.

The steganography methods used by `austeg` are described in more detail in our final report but in short, `austeg` is a program that can hide data in audio files (only `.wav` files for now) and extract the data again using two different methods.

The first method, which we call the Extended LSB algorithm, is based on least significant bit steganography. This method can hide data in an audio file in such a way that retrieving it is non-trivial unless you have the correct key. See [How to run the Extended LSB algorithm](#how-to-run-the-extended-lsb-algorithm) for details on how to run the algorithm.

The second method, which we call the Spectrogramming algorithm, hides data in an audio file by writing the data the audio file's spectrogram. To visualise the spectrogram of an audio file we recommend [SonicVisualiser](https://www.sonicvisualiser.org/). See [How to run the Spectrogramming algorithm](#how-to-run-the-spectrogramming-algorithm) for details on how to run the algorithm.

# Requirements
Before you can run `austeg`, you need to install the following dependencies (from [requirements.txt](requirements.txt)) :
```python
colorama==0.4.4
matplotlib==3.5.1
numpy==1.22.3
Pillow==9.1.0
pydub==0.25.1
tqdm==4.63.0
wavio==0.0.4
```

This can be done by running the following command in the terminal:
```
pip install -r requirements.txt
```
or 
```
python3 -m pip install -r requirements.txt
```

# Running the program

## **Note for Windows users.**
If you are on Windows you might have to replace `python3` with `python` or `py` in the examples below to run the code.


## How to run the Extended LSB algorithm
The Extended LSB algorithm can be invoked by running `austeg -lsb`. The `-e` flag and `-d` flag are used to encode and decode data respectively.

### **Encoding using Extended LSB**
The Extended LSB algorithm is able to encode arbitrary plain text and binary data within a `.wav` file. The Extended LSB encoding algorithm expects as input:
- a key (used as a seed to hide and extract secret data) given as a string,
- an input file (which secret data will be encoded in),
- the secret data given as a file,
- (optional) the output destination of the resulting `.wav` file. If not provided then `./out.wav` is used.

The format is as follows:
```bash
python3 austeg.py -lsb -e --key KEY --input INPUT_FILE --data DATA_FILE --output OUTPUT_FILE
```
If the key contains special characters and/or spaces then you need to either escape the characters or wrap the key with quotes. For example, the `--key "my\" pass"` is a valid key.

*Note:* `austeg` will inform you how many bits were encoded. To decode the resulting audio file you will need to know the number of bits encoded, otherwise you might not decode all the secret data (or too much). Look for something like `[!]: Encoded 40 bits` in the output.

#### Example
As an example of encoding data using the Extended LSB algorithm, consider running the following:
```bash
python3 austeg.py -lsb -e --key my_pass --input TestData/mudic.wav --data TestData/data.txt --output hidden.wav
```
Here we have specified that the contents on `TestData/data.txt` should be encoded within `TestData/mudic.wav` using `my_pass` as a key. The resulting audio file will be written to `hidden.wav`.



### **Decoding using Extended LSB**
The Extended LSB algorithm is able to decode any secret data encoded using the Extended LSB algorithm. You will need the same key using during encoding, and the number of bits encoded. The Extended LSB decoding algorithm expects as input:
- a key (used as a seed to hide and extract secret data) given as a string,
- an input file (which some secret data is encoded in),
- the number of bits to decode.

The format is as follow:
```bash
python3 austeg.py -lsb -d -key KEY --input INPUT_FILE --bits NO_BITS
```

The decoded secret data will be printed to standard output. If the wrong key is used, then the program will output garbage. If the wrong number of bits is specified, then the program will only output a part of the secret data, or output the secret data followed by garbage.

#### Example
As an example of decoding data using the Extended LSB algorithm, consider running the following:
```bash
python3 austeg.py -lsb -d --key my_pass --input hidden.wav --bits 40  
```
Here we have specified that 40 bits should be decoded from `hidden.wav` using `my_pass` as a key. If you also ran the encoding example above, then the contents of `TestData/data.txt` should be printed to your console.



## How to run the Spectrogramming algorithm
The Spectrogramming algorithm can be invoked by running `austeg -spectro`. The `-e` flag and `-d` flag are used to encode and decode data respetively.

### **Encoding using Spectrogramming**
The Spectrogramming algorithm is able to encode arbitrary plain text and binary data within a `.wav` file. However, before writing the secret data to the spectrogram of an audio file, the secret data is base64 encoded. This is done as not all bytes are printable. The Spectrogramming encoding algorithm expects as input:
- the secret data given as a file,
- (optional) the output destination of the resulting `.wav` file. If not provided then `./out.wav` is used.

The format is as follows:
```bash
python3 austeg.py -spectro -e --data DATA_FILE --output OUTPUT_FILE
```

#### Example
As an example of encoding data using the Spectrogramming algorithm, consider running the following:
```bash
python3 austeg.py -spectro -e --data TestData/data.txt --output hidden.wav
```
Here we have specified that the contents of `TestData/data.txt` should be encoded and the resulting audio file should be written to `hidden.wav`. A screenshot of the spectrogram of `hidden.wav` is provided at [example_spectrogram.png](TestData/example_spectrogram.png). We can see that the spectrogram contains the base64 encoded contents of `TestData/data.txt`.


#### **Decoding using Spectrogramming**
The Spectrogramming algorithm is able to decode any secret data encoded using the Spectrogramming algorithm (given that you do not change any of the algorithm's paramters after encoding). The Spectrogramming decoding algorithm expects as input:
- an input file (which some secret data is encoded in).

The format is as follows:
```bash
python3 austeg.py -spectro -d --input INPUT_FILE
```
The decoded secret data will be printed to standard output.

#### Example
As an example of decoding data using the Spectrogramming algorithm, consider running the following:
```bash
python3 austeg.py -spectro -d --input hidden.wav 
```
Here we have specified that some secret data should be decoded from `hidden.wav`. If you also ran the encoding example above, then the contents of `TestData/data.txt` should be printed to your console.
