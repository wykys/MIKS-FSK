#!/usr/bin/env python3
from numpy import arange, sin, cos, pi, convolve, array, correlate
import numpy as np

from bin_print import bin_print
from bell202 import FREQ_H, FREQ_L, BIT_SIZE
from filter_coe import LP_FILTER
import sig_load
import sig_plot
import bell202


def correlation_rx(rf_sig: np.ndarray, fs: float) -> bool:
    #sig_plot.tim_mod(rf_sig, fs)

    # generate base signals
    t = arange(0, BIT_SIZE/fs, 1/fs)
    base_cos_l = cos(2*pi*FREQ_L*t)
    base_sin_l = sin(2*pi*FREQ_L*t)
    base_cos_h = cos(2*pi*FREQ_H*t)
    base_sin_h = sin(2*pi*FREQ_H*t)
    """
    sig_plot.splitplot(
        [base_cos_l, base_sin_l, base_cos_h, base_sin_h],
        title=[
            '$\cos(2\pi f_L t)$',
            '$\sin(2\pi f_L t)$',
            '$\cos(2\pi f_H t)$',
            '$\sin(2\pi f_H t)$'
        ]
    )
    """

    # detector valid, full, same
    cor1 = correlate(rf_sig, base_cos_l, 'full')
    cor2 = correlate(rf_sig, base_sin_l, 'full')
    cor3 = correlate(rf_sig, base_cos_h, 'full')
    cor4 = correlate(rf_sig, base_sin_h, 'full')
    #sig_plot.splitplot([cor1, cor2, cor3, cor4],

    # sumator
    sum_l = cor1**2 + cor2**2
    sum_h = cor3**2 + cor4**2
    """
    sig_plot.splitplot(
        [sum_l, sum_h],
        title=['cor$_1^2$ + cor$_2^2$', 'cor$_3^2$ + cor$_4^2$']
    )
    """

    # integrator
    det_l = convolve(sum_l, LP_FILTER, 'valid')
    det_h = convolve(sum_h, LP_FILTER, 'valid')

    # value size thresholding
    bin_sig = det_h > det_l
    """
    sig_plot.splitplot(
        [det_l, det_h, bin_sig],
        title=[
            'det$_L = \int$ (cor$_1^2$ + cor$_2^2$) $\mathrm{d}t$',
            'det$_H = \int$ (cor$_3^2$ + cor$_4^2$) $\mathrm{d}t$',
            'BIN = det$_H$ > det$_L$'
        ]
    )
    """

    data = bell202.find_data_bytes(bin_sig)
    #bin_print(data)
    #return bell202.parse_print(data)
    return bell202.check_data(data)


if __name__ == '__main__':
    # get data and normalization
    fs, rf_sig = sig_load.wav('3.wav')
    correlation_rx(rf_sig, fs)
    sig_plot.show()
