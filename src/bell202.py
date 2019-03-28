import numpy as np
from numpy import array, uint8
from bin_print import bin_print

FREQ_L = 2200
FREQ_H = 1200
SAMPLE_RATE = 9600
DATA_RATE = 1200
BIT_SIZE = SAMPLE_RATE/DATA_RATE


def find_data_bytes(s):
    l_cnt = 0
    h_cnt = 0

    flag_frame_start = False
    flag_change_from_l = False
    flag_change_from_h = False

    raw = []

    for bit in s:
        # bit counters
        if bit:
            h_cnt += 1
            if l_cnt:
                flag_change_from_l = True
        else:
            l_cnt += 1
            if h_cnt:
                flag_change_from_h = True

        # when was start puls
        if flag_frame_start and (flag_change_from_l or flag_change_from_h):

            if flag_change_from_l:
                raw.extend([False] * int(np.round(l_cnt / BIT_SIZE)))
                flag_change_from_l = False
                l_cnt = 0
            else:
                raw.extend([True] * int(np.round(h_cnt / BIT_SIZE)))
                flag_change_from_h = False
                h_cnt = 0

        # wait for start
        if (not flag_frame_start) and flag_change_from_h and (h_cnt > BIT_SIZE):
            flag_frame_start = True
            flag_change_from_h = False
            h_cnt = 0
            #print('START POSITION')

    if l_cnt:
        raw.extend([False] * int(np.round(l_cnt / BIT_SIZE)))
    elif h_cnt > 0:
        raw.extend([True] * int(np.round(h_cnt / BIT_SIZE)))

    i = -1
    byte = 0
    data = []
    for bit in raw:
        if i > 7:
            i = -1
            data.append(uint8(byte))
            byte = 0
            continue
        elif i >= 0:
            byte |= bit << i
        i += 1
    return data


def check_data(data: list) -> bool:
    # check start
    if data[0] != 0x80:
        return False

    # check len
    if data[1] + 3 > len(data):
        return False

    # check sum
    check_sum = 0
    for i in range(0, data[1]+2):
        check_sum += data[i]
    check_sum = ((~check_sum) + 1) & 0xFF

    if check_sum != data[i+1]:
        return False

    # check date time
    if data[2] != 0x01:
        return False
    else:
        for i in data[4:12]:
            if i < 0x30 or i > 0x39:
                return False

    # check number
    if data[12] != 0x02:
        return False
    elif data[13] > 20:
        return False

    # check name
    if data[data[13] + 14] != 0x07:
        return False
    else:
        if (data[13] + 16 + data[data[13] + 15]) > len(data):
            return False
        for c in data[data[13] + 16: data[13] + 16 + data[data[13] + 15]]:
            if c < 31 and c > 126:
                return False

    return True


def parse_print(data: list) -> bool:

    if not check_data(data):
        print('ERROR packet is corrupted')
        return False

    print(f'Packet length {data[1]+3} octets')

    # date
    moon, day, hour, minute = list(
        map(
            lambda x: ''.join(x),
            array(list(map(lambda x: chr(x), data[4:12]))).reshape(4, 2)
        )
    )
    print(f'P1 datetime(MM/DD HH:MM): {moon}/{day} {hour}:{minute}')

    # number
    print('P2 caller number: ', end='')
    for i in range(14, data[13] + 14):
        print(chr(data[i]), end='')
    print()

    # name
    print('P7 caller name: ', end='')
    for i in range(data[13] + 14, data[13] + 16 + data[data[13] + 15]):
        print(chr(data[i]), end='')
    print()

    return True
