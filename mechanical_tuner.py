import sounddevice as sd
import numpy as np
import RPi.GPIO as GPIO
import time

# Sets up GPIO pins for use
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

# Sampling RATE and RECORDING_TIME can be changed to vary accuracy of frequency detection
CHANNELS = 1
RATE = 10000
RECORDING_TIME = 0.1
LISTENING_THRESHOLD = 0.001     # Average amplitude of signal below which input is ignored
TUNING_ACCURACY = 1             # +- Hz
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

    return RECORDING_TIME, crossings, (RECORDING_TIME / (crossings - 1 // 2))


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

        return 1 / (peak * (RECORDING_TIME / (RATE * RECORDING_TIME)))

while True:

    # Generates 2D array from microphone audio
    recording = sd.rec(int(RECORDING_TIME * RATE), samplerate=RATE, channels=CHANNELS, blocking=True, dtype='float64')

    # Converts recording into 1D array
    buffer = [item for sublist in recording for item in sublist]

    # Generates array of absolute amplitudes
    abs_amp = [abs(num) for num in buffer]

    # Finds average of absolute amplitudes (crude volume)
    avg_abs_amp = np.average(abs_amp)

    # Bulk of program only executes when a string pluck is detected
    if avg_abs_amp > LISTENING_THRESHOLD:

        recorded_frequency = autocorrelation(buffer)
        print(recorded_frequency)

        if type(recorded_frequency) == float:   # Avoids using recorded_frequencies which are 'None' due to input error

            prev_diff = 999
            
            # Finds which string is being plucked (chooses nearest frequency)
            for frequency in std_tuning:

                diff = abs(frequency - recorded_frequency)
                if diff < prev_diff:

                    target = frequency
                    final_diff = diff

                prev_diff = diff

            # Motor shakes if string is in tune
            if final_diff < TUNING_ACCURACY:

                print('Tuned!')
                GPIO.output(17, True)
                GPIO.output(18, False)
                time.sleep(0.2)

                GPIO.output(17, False)
                GPIO.output(18, True)
                time.sleep(0.2)
            
            # If recorded_frequency is flat, turns tuning peg clockwise (to sharpen note)
            elif recorded_frequency < target:

                GPIO.output(17, False)
                GPIO.output(18, True)
                time.sleep(0.5)
            
            # If recorded_frequency is sharp, turns tuning peg clockwise (to flatten note)
            else:

                GPIO.output(17, True)
                GPIO.output(18, False)
                time.sleep(0.5)

            # Stops motor
            GPIO.output(17, False)
            GPIO.output(18, False)
