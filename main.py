import wave
import os
import numpy as np
from midiutil.MidiFile import MIDIFile
import matplotlib.pyplot as plt
from scipy import fft
from scipy.stats import mode

audio = wave.open(f"{os.getcwd()}\\audio\\Test_2.wav", 'rb')
frame_rate = audio.getframerate()
num_frames = audio.getnframes()
duration = num_frames/frame_rate

# Read all frames
frames = audio.readframes(num_frames)
audio.close()

times = np.linspace(0, duration, num=num_frames)

audio_signal = np.frombuffer(frames, dtype=np.int16)
plt.figure(figsize=(15, 5))
plt.plot(times, audio_signal)
plt.title('Left Channel')
plt.ylabel('Signal Value')
plt.xlabel('Time (s)')
plt.xlim(0, duration)
plt.show()