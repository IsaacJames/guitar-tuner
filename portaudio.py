import pyaudio
import wave
import sys

p = pyaudio.PyAudio()
wf = wave.open(sys.argv[1], 'rb')
while(True):
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)