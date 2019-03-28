#!/usr/bin/env python3
# wykys 2019

import numpy as np


def awgn(s: np.ndarray, snr_db: float = 20) -> np.ndarray:
    sig_avg_watts = np.mean(s**2)
    sig_avg_db = 10 * np.log10(sig_avg_watts)

    noise_avg_db = sig_avg_db - snr_db
    noise_avg_watts = 10 ** (noise_avg_db / 10)

    mean_noise = 0
    noise_volts = np.random.normal(
        mean_noise,
        np.sqrt(noise_avg_watts),
        len(s)
    )
    return s + noise_volts


if __name__ == '__main__':
    import sig_plot
    f = 1e3
    fs = 100*f
    t = np.arange(0, 1/f, 1/fs)
    s1 = np.sin(2*np.pi*f*t)
    s2 = awgn(s1, 10)
    sig_plot.splitplot([s1, s2])
    sig_plot.show()
