import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 1
sd.default.samplerate = RATE

print("Ready")

while True:
    input()
    print("Recording")

    myrecording = sd.rec(int(RECORD_SECONDS * RATE), samplerate=RATE,
                         channels=CHANNELS, blocking=True, dtype='float64')
    print("*")

    amplitudes = [item for sublist in myrecording for item in sublist]


    prev = amplitudes[0]
    count = 0

    for num in amplitudes:
        if num == 0 and prev != 0:
            count += 1
        if prev * num < 0:
            count += 1
        prev = num

    print("Zero crossings: ", count // 2)

    windowed = amplitudes *
    #plt.plot(np.fft.rfft(amplitudes))