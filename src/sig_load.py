#!/usr/bin/env python3
# wykys 2019

from numpy import ndarray
from awgn import awgn

WAV_PATH = '../wav/'

def wav(path: str, snr_db: float = None) -> list:
    from scipy.io import wavfile
    fs, s = wavfile.read(WAV_PATH + path)

    if not (snr_db is None):
        s = awgn(s, snr_db)

    s = s / s.max()
    return fs, s
