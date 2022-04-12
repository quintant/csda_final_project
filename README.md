
# `CSDA Final Project` - *Audio Steganography*  

  > ### **Bjarni Dagur** <bjarnidt19@ru.is>  
  > ### **Sigurjón Ingi** <sigurjonj20@ru.is>  

---
<br>
<br>
<br>
<br>

# How to run the Extended LSB algorithm
Here we use the flag `-lsb` to run the extended LSB algorithm.

## **Encode**

```bash
python3 austeg.py -lsb -e -k KEY -i INPUT_FILE --data DATA_FILE -o OUTPUT_FILE
```
Some things to note:
- `-e` is the flag for encoding
- `-k` is read as a string from stdin. It's possible to have spaces in the key but then you need to use quotes.
  - `-k "This is a key with spaces"`
- `-i` should be a path to a wav file.
- `--data` should be a path to a text file.
- `-o` is optional and will be the output file. If not specified, the output will be `out.wav`.


## **Decode**

```bash
python3 austeg.py -lsb -d -k KEY -i INPUT_FILE -b NO_BITS
```
Some things to note:
- `-d` is the flag for decoding.
- `-i` should be a path to the wav file that contains the hidden data.
- `-b` tells the program how many bits it has to decode from the wav file.

After decoding the hidden data, it will be printed to stdout. If the wrong key is used, the program will print some gibberish. If the wrong number of bits is specified, the program will only print a part of the hidden data, or print the hidden data followed by gibberish.

<br>
<br>
<br>
<br>

# How to run the Spectrogram algorithm
Here we use the flag `-spectro` to run the Spectrogram algorithm.
## **Encode**

```bash
python3 austeg.py -spectro -e --data DATA_FILE -o OUTPUT_FILE
```
Some things to note:
- `-e` is the flag for encoding
- `--data` should be a path to a text file.
- `-o` is optional and will be the output file. If not specified, the output will be `out.wav`.


## **Decode**

```bash
python3 austeg.py -spectro -d -i INPUT_FILE
```
Some things to note:
- `-d` is the flag for decoding.
- `-i` should be a path to the wav file that contains the hidden data.


<br>
<br>
<br>
<br>

# Misc
## **Convert to wav**
Inside the `Misc` folder, you can find a script that converts all sorts of audio files and some video files to wav files.
This script has not been tested very well but should work at least for some audio files if the user has no other software to convert the files.

```bash
python3 convert.py FILENAME
```
