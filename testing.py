import pyaudio

CHUNK = 2024
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("* recording")
while True:
    data = stream.read(CHUNK)
    stream.write(data, CHUNK)


stream.stop_stream()
stream.close()

p.terminate()