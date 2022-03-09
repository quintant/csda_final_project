import sys
import wave

import pylab
def graph_spectrogram(wav_file1, wav_file2):
    sound_info1, frame_rate1 = get_wav_info(wav_file1)
    sound_info2, frame_rate2 = get_wav_info(wav_file2)
    if frame_rate1 != frame_rate2:
        print('Not similar files.')

    sound_info = sound_info1 - sound_info2
    pylab.figure(num=None, figsize=(19, 12))
    pylab.subplot(111)
    pylab.title(f'spectrogram of diff between {wav_file1} and {wav_file2}')
    pylab.specgram(sound_info, Fs=frame_rate1)
    pylab.savefig('spectrogram.png')
    # pylab.show()
def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.frombuffer(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate


if __name__ == "__main__":
    graph_spectrogram(sys.argv[1], sys.argv[2])