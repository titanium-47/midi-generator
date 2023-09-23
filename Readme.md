## Description
A program that uses an FFT to graph the amplitude and frequency of each note in a song.
This program also saves the notes as a midi file.

## Installation
```pip install -r requirements.txt```

## Dependancies
mp3 usage requires [https://ffmpeg.org/](ffmpeg)

## Usage
```-i   The file that the audio to be analyzed is.```
```-o   The file that the output midi is stored in.```
```-c   The size of each chunk that is processed by the fft```
```-t   The number of tracks to create on the output MIDI```
```-m   Set this flag if the audio to be analyzed is in mp3 format```

### Example
```python analyze.py -i "input.mp3"  -o "output.mid" -m -t 4 -c 2048```