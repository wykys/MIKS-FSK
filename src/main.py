#!/usr/bin/env python3
import sig_load
import sig_plot
import numpy as np

from multiprocessing.pool import Pool
from fsk_dem1 import customized_filter_rx
from fsk_dem2 import correlation_rx
from awgn import awgn


def simul(wav_sig, snr_db, number_of_loop):
    dem1_err = 0
    dem2_err = 0

    for i in range(number_of_loop):
        rf_sig = awgn(wav_sig, snr_db)

        if not customized_filter_rx(rf_sig, fs):
            dem1_err += 1

        if not correlation_rx(rf_sig, fs):
            dem2_err += 1

    dem1_err = dem1_err / number_of_loop * 100
    dem2_err = dem2_err / number_of_loop * 100
    print(
        f'SNR: {snr_db:5.1f} dB ... ERR1: {dem1_err:5.1f} % ... ERR2: {dem2_err:5.1f} %'
    )
    return snr_db, dem1_err, dem2_err


if __name__ == '__main__':
    step = 0.5
    snr_range_db = [2, 14]
    number_of_loop = 1000

    fs, wav_sig = sig_load.wav('1.wav')

    pool = Pool(processes=4)
    multiple_results = [
        pool.apply_async(
            simul, (wav_sig, snr_db, number_of_loop)
        ) for snr_db in np.arange(min(snr_range_db), max(snr_range_db)+step, step)
    ]

    snr_db, dem1_err, dem2_err = np.array(
        [res.get() for res in multiple_results]
    ).transpose()

    np.savetxt(
        'log.csv',
        np.asarray(
            [snr_db, dem1_err, dem2_err]
        ).transpose(),
        delimiter=',',
        fmt='%5.1f',
        header='"SNR [dB]","ERR1 [%]","ERR2 [%]"'
    )

    print('OK')

    fig = sig_plot.figure()
    sig_plot.plot(snr_db, dem1_err, label='DEM1')
    sig_plot.plot(snr_db, dem2_err, label='DEM2')
    sig_plot.xlabel('SNR [dB]')
    sig_plot.ylabel('lost packets [%]')
    sig_plot.lim(snr_range_db)
    sig_plot.grid()
    sig_plot.legend()
    fig.savefig('lost_packets.pdf')
    fig.savefig('lost_packets.png')

    sig_plot.show()
