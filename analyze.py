import wave
import os
import numpy as np
from midiutil.MidiFile import MIDIFile
import matplotlib.pyplot as plt
from scipy import fft
import math
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tracks", help="Amount of tracks", type=int, default=1)
    parser.add_argument("-c", "--chunksize", help="Chunk size (typically pick a multiple of 2)", type=int, default=4096)
    parser.add_argument("-i", "--input", help="input file path", type=str, required=True)
    parser.add_argument("-o", "--output", help="Output file path", type=str, required=True)
    parser.add_argument("-m", "--mp3", help="file type is mp3", action="store_true")
    args = parser.parse_args()

    track_amount = args.tracks
    chunk_size = args.chunksize
    input_file = args.input
    output_file = args.output

    if(args.mp3):
        subprocess.run(["ffmpeg", "-i", input_file, "-ab", "160k", "-ac", "-2", "-ar", "44100", "-vn", 'temp.wav'], shell=True)
        input_file = 'temp.wav'


    fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

    audio = wave.open(input_file, 'rb')
    frame_rate = audio.getframerate()
    num_frames = audio.getnframes()
    duration = num_frames/frame_rate

    # Read all frames
    frames = audio.readframes(num_frames)
    audio.close()

    audio_signal = np.frombuffer(frames, dtype=np.int16)

    x = chunk_size
    sound = []

    while x<num_frames:
        yfft = fft(audio_signal[x-chunk_size:x])[:int(chunk_size*0.75)]
        frequencies = np.argsort(yfft)[len(yfft)-track_amount:]
        volumes = np.sort(yfft)[len(yfft)-track_amount:]
        sound.append([frequencies, volumes])
        x+=chunk_size

    sound = np.array(sound)
    max_volumes = []

    for i in range(0, track_amount):
        max_volumes.append(np.amax(sound[:,1,i]))

    max_volume = max(max_volumes)

    for i in range(0, len(sound)):
        for j in range(0, track_amount):
            sound[i][1][j] = sound[i][1][j]/max_volume*100

    ax1.plot(sound[:,0,0])
    ax2.plot(sound[:,1,0])

    mf = MIDIFile(track_amount)     # only 1 track
    time = 0    

    for i in range(0, track_amount):
        mf.addTrackName(i, time, f"Track {i}")
        mf.addTempo(i, time, 6000)

    # add some notes
    channel = 0
    note_length = duration/len(sound)
    for value in sound[1:]:
        for i in range(0, track_amount):
            if(value[0][i] != 0):
                volume = abs(value[1][i])
                pitch = 12*math.log2(value[0][i]*frame_rate/chunk_size/220.0)+57
                mf.addNote(i, channel, int(pitch), int(time*100.0), int(note_length*100.0), int(volume))
        time += note_length

    # write it to disk
    with open(output_file, 'wb') as outf:
        mf.writeFile(outf)

    if(args.mp3):
        os.remove('temp.wav')

    plt.show()

if __name__ == "__main__":
    main()