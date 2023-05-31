import wave
import os
import numpy as np
from midiutil.MidiFile import MIDIFile
import matplotlib.pyplot as plt
from scipy import fft
import math

CHUNK_SIZE = 4096

audio = wave.open(f"{os.getcwd()}\\audio\\Test_2.wav", 'rb')
frame_rate = audio.getframerate()
num_frames = audio.getnframes()
duration = num_frames/frame_rate

# Read all frames
frames = audio.readframes(num_frames)
audio.close()

audio_signal = np.frombuffer(frames, dtype=np.int16)

x = CHUNK_SIZE
frequencies = []
while x<num_frames:
    yfft = fft(audio_signal[x-CHUNK_SIZE:x])[:int(CHUNK_SIZE*0.75)]
    frequency = np.argmax(yfft)*frame_rate/CHUNK_SIZE
    if np.amax(yfft) > 200000:
        frequencies.append(frequency)
    else:
        frequencies.append(0)
    x+=CHUNK_SIZE
print(frequencies)
print(np.argmax(yfft))
plt.plot(frequencies)

mf = MIDIFile(1)     # only 1 track
track = 0   # the only track

time = 0    # start at the beginning
mf.addTrackName(track, time, "Sample Track")
mf.addTempo(track, time, 6000)

# add some notes
channel = 0
note_length = duration/len(frequencies)
for value in frequencies:
    if(value != 0):
        volume = 100
        pitch = 12*math.log2(value/220.0)+57
        mf.addNote(track, channel, int(pitch), int(time*100.0), int(note_length*100.0), int(volume))
    time += note_length

# write it to disk
with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)

plt.show()