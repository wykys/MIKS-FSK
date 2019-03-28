#!/usr/bin/env python3
# wykys 2019

from numpy import arange, sin, cos, pi, convolve, array, correlate
import numpy as np

from bin_print import bin_print
from bell202 import FREQ_H, FREQ_L, BIT_SIZE
from filter_coe import LP_FILTER, HP_FILTER
import sig_load
import sig_plot
import bell202


def customized_filter_rx(rf_sig: np.ndarray, fs: float) -> bool:
    # band pass split
    lp_sig = np.abs(convolve(rf_sig, LP_FILTER, 'valid'))
    hp_sig = np.abs(convolve(rf_sig, HP_FILTER, 'valid'))

    # marge lp and hp
    marge_sig = lp_sig - hp_sig

    # integrator
    int_sig = convolve(marge_sig, LP_FILTER, 'valid')

    # tresholding
    bin_sig = int_sig > 0.07
    """
    sig_plot.splitplot(
        [lp_sig, hp_sig, marge_sig, int_sig,bin_sig],
        title=[
            '|LP|',
            '|HP|',
            '|LP| - |HP|',
            '$\int$ (|LP| - |HP|) $\mathrm{d}t$', 'BIN'
        ]
    )
    """

    data = bell202.find_data_bytes(bin_sig)
    #bin_print(data)
    #return bell202.parse_print(data)
    return bell202.check_data(data)


if __name__ == '__main__':
    fs, rf_sig = sig_load.wav('1.wav', 10)
    customized_filter_rx(rf_sig, fs)
    sig_plot.show()
