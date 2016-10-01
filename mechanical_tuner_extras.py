import sounddevice as sd
import matplotlib.pyplot as plt

CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 0.1
sd.default.samplerate = RATE

print("Ready")


# Finds frequency from zero crossings
def zero_crossings(signal):
    prev = signal[0]
    crossings = 0

    for cur in signal:
        if cur == 0 and prev != 0:
            crossings += 1
        if prev * cur < 0:
            crossings += 1
        prev = cur

    return RECORD_SECONDS, crossings, (RECORD_SECONDS / (crossings - 1 // 2))


# Finds frequency via autocorrelation
def autocorrelation(signal):
    
    # Cross-correlation
    cross_correlations = []
    prev = 0
    
    for i in range(0, len(signal)):

        cor = 0
        for k in range(0, len(signal)):
            if k >= len(signal) - i:
                cor += (signal[k]) * (signal[k + i - len(signal)])
            else:
                cor += (signal[k]) * (signal[k + i])
        cross_correlations.append(cor)
        
        if i > 10 and prev > 0.8 * cross_correlations[0] and cor < prev:
            peak = i - 1
            break
        
        prev = cor

    # Standard autocorrelation
    correlations = []
    prev = 0

    for i in range(0, len(signal)):
        cor = 0
        
        for k in range(0, len(signal) - i):
            cor += (signal[k]) * (signal[k + i])
        correlations.append(cor)
        
        if i > 10 and prev > 0.8 * correlations[0] and cor < prev:
            peak = i - 1
            break
        
        prev = cor

    # Plots correlation coefficients in matplotlib figures
    ax3 = fig.add_subplot(312)
    ax3.plot(correlations)

    ax2 = fig.add_subplot(313)
    ax2.plot(cross_correlations)
    
    # Standalone peak-finder
    for i in range(1, (len(correlations) - 1)):
        thresh = 0.75 * correlations[0]

        if correlations[i] > correlations[i - 1] and correlations[i] > correlations[i + 1] and correlations[i] > thresh:
            peak = i
            break

    return correlations[0], peak, 1 / (peak * (RECORD_SECONDS / (RATE * RECORD_SECONDS))), correlations[peak] / correlations[0]


while True:

    # Waits for enter key to be pressed
    input()

    print("Recording")

    # Generates 2D array from microphone audio
    recording = sd.rec(int(RECORD_SECONDS * RATE), samplerate=RATE, channels=CHANNELS, blocking=True, dtype='float64')

    print("Finished")

    # Converts recording into 1D array
    buffer = [item for sublist in recording for item in sublist]

    fig = plt.figure()

    # Calls frequency-finding functions
    print(zero_crossings(buffer))
    print(autocorrelation(buffer))

    # Plots unprocessed signal
    amplitudes = fig.add_subplot(311)
    amplitudes.plot(buffer)

    plt.show()
