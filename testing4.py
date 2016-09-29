for i in range(0, len(amplitudes)):
    sum = 0
    for k in range(0, len(amplitudes) - i):
        sum += (amplitudes[k]) * (amplitudes[k + i] / 256)