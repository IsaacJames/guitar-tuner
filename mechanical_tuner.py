import sounddevice as sd
import numpy as np
import time
import RPi.GPIO as GPIO

# Sets up GPIO pins for use
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

# Rate and recording time can be changed to vary accuracy of frequency detection
CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 0.1
sd.default.samplerate = RATE

std_tuning = [82.41, 110, 146.8, 196, 246.9, 329.6]

print("Ready")


# Finds frequency from zero crossings
def zero_crossings(signal):
    prev_cor = signal[0]
    crossings = 0

    for cur in signal:
        if cur == 0 and prev_cor != 0:
            crossings += 1
        if prev_cor * cur < 0:
            crossings += 1
        prev_cor = cur

    return RECORD_SECONDS, crossings, (RECORD_SECONDS / (crossings - 1 // 2))


# Finds frequency via autocorrelation
def autocorrelation(signal):
    correlations = []
    prev_cor = 0

    peak = 1

    for i in range(0, len(signal)):
        cor = 0
        for k in range(0, len(signal) - i):
            cor += (signal[k]) * (signal[k + i])
        correlations.append(cor)

        if i > 10 and prev_cor > 0.8 * correlations[0] and cor < prev_cor:
            peak = i - 1
            break

        prev_cor = cor

    if peak == 1 or peak == 10:
        return

    else:
        return 1 / (peak * (RECORD_SECONDS / (RATE * RECORD_SECONDS)))


while True:

    #print("Recording")

    # Generates 2D array from microphone audio
    recording = sd.rec(int(RECORD_SECONDS * RATE), samplerate=RATE, channels=CHANNELS, blocking=True, dtype='float64')

    #print("Finished")

    # Converts recording into 1D array
    buffer = [item for sublist in recording for item in sublist]
    abs_amp = [abs(num) for num in buffer]
    avg_abs_amp = np.average(abs_amp)

    if avg_abs_amp > 0.001:

        recorded_frequency = autocorrelation(buffer)

        prev_diff = 999

        for frequency in std_tuning:
            diff = abs(frequency - recorded_frequency)
            if diff < prev_diff:
                target = frequency
                final_diff = diff
            prev_diff = diff

        if final_diff < 5:
            print('tuned!')
            exit()

        if recorded_frequency < target:
            GPIO.output(17, True)
            GPIO.output(18, False)
            time.sleep(1)
        else:
            GPIO.output(17, False)
            GPIO.output(18, True)
            time.sleep(1)

        GPIO.output(17, False)
        GPIO.output(18, False)