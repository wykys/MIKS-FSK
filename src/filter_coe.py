#!/usr/bin/env python3
# wykys 2019

import numpy as np
from scipy import signal
from bell202 import SAMPLE_RATE, FREQ_H, FREQ_L

fs = SAMPLE_RATE
numtaps = 41
fm = (FREQ_L + FREQ_H)/2
f_shift = 10
win = ('kaiser', 14)

LP_FILTER = signal.firwin(
    numtaps,
    fm - f_shift,
    fs=fs,
    window=win,
    scale=True
)

HP_FILTER = signal.firwin(
    numtaps,
    fm + f_shift,
    fs=fs,
    window=win,
    pass_zero=False,
    scale=True
)

if __name__ == '__main__':
    import sig_plot

    freq_l, h_l = signal.freqz(LP_FILTER, fs=fs)
    freq_h, h_h = signal.freqz(HP_FILTER, fs=fs)

    h_l = 20*np.log10(np.abs(h_l))
    h_h = 20*np.log10(np.abs(h_h))

    sig_plot.figure()
    sig_plot.plot(freq_l, h_l, label='LP')
    sig_plot.plot(freq_h, h_h, label='HP')
    sig_plot.grid()
    sig_plot.legend()
    sig_plot.show()
