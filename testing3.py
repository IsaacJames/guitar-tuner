import sounddevice as sd
import matplotlib.pyplot as plt

CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 0.5
sd.default.samplerate = RATE

print("Ready")


while True:

    # Waits for enter key to be pressed
    input()

    print("Recording")

    recording = sd.rec(int(RECORD_SECONDS * RATE), samplerate=RATE, channels=CHANNELS, blocking=True, dtype='float64')
    print("Finished")

    # Converts recording into 1D array
    amplitudes = [item for sublist in recording for item in sublist]

    # Finds frequency from zero crossings
    def zero_crossings():

        prev = amplitudes[0]
        crossings = 0

        for cur in amplitudes:
            if cur == 0 and prev != 0:
                crossings += 1
            if prev * cur < 0:
                crossings += 1
            prev = cur

        return RECORD_SECONDS / (crossings - 1//2)

    # Finds
    correlations = []

    for i in range(0, len(amplitudes)):
        cor = 0
        for k in range(0, len(amplitudes) - i):
            cor += (amplitudes[k]) * (amplitudes[k + i])
            correlations.append(cor)

    fig = plt.figure()

    ax1 = fig.add_subplot(211)
    ax1.plot(amplitudes)

    ax2 = fig.add_subplot(212)
    ax2.plot(correlations)

    plt.show()