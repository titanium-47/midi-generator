import wave
import os
import numpy as np

audio = wave.open(f"{os.getcwd()}\\audio\\Test_2.wav", 'rb')
sample_frequency = audio.getframerate()
sample_number = audio.getnframes()
sample_duration = sample_number/sample_frequency
sample_channels = audio.getnchannels()

print(f"{sample_channels}\n{sample_duration}\n{sample_number}\n{sample_frequency}")

