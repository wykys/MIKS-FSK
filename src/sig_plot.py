#!/usr/bin/env python3
from matplotlib.pyplot import (
    plot,
    show,
    legend,
    figure,
    subplot,
    xlabel,
    ylabel,
    title
)
from matplotlib import pyplot as plt
from numpy.fft import fft, fftshift
import numpy as np


def get_color(i: int) -> str:
    COLOR = 'bgrcmyk'
    return COLOR[i % len(COLOR)]


def grid():
    plt.grid(color='gray', linestyle='--', linewidth=0.5)


def lim(xlim: list = None, ylim: list = None):
    if not (xlim is None):
        plt.xlim(xlim)
    if not (ylim is None):
        plt.ylim(ylim)


def tim(s: np.ndarray, fs: int, c: str = get_color(0)):
    t = np.arange(0, s.size/fs, 1/fs)
    plt.plot(t, s, c=c)
    plt.xlabel('$t$ [s]')
    plt.ylabel('|$s$| [-]')
    grid()


def mod(s: np.ndarray, fs: int, c: str = get_color(0)):
    module = fftshift(abs(fft(s))) / s.size
    f = np.linspace(-fs/2, fs/2, s.size)
    plt.plot(f, module, c=c)
    plt.xlabel('$f$ [Hz]')
    plt.ylabel('|$S$| [-]')
    grid()


def tim_mod(s: np.ndarray, fs: int):
    plt.figure()
    plt.subplot(211)
    tim(s, fs, c=get_color(0))
    plt.subplot(212)
    mod(s, fs, c=get_color(1))


def splitplot(sig_list: list, title: list = None, xlim: list = None, ylim: list = None):
    plt.figure()
    for i, s in enumerate(sig_list):
        plt.subplot(len(sig_list), 1, i + 1)
        plt.plot(s, c=get_color(i))
        grid()
        lim(xlim, ylim)
        if title is not None and len(title) == len(sig_list):
            plt.title(title[i])
    plt.tight_layout(pad=0, h_pad=0, w_pad=0.01)


def multiplot(sig_list: list, xlim: list = None, ylim: list = None):
    plt.figure()
    for s in sig_list:
        plt.plot(s)
    grid()
    lim(xlim, ylim)
