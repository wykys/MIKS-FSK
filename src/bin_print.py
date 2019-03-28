# wykys 2019

def bin_print(byte_array: list, num_in_line: int = 8, space: str = ' | '):
    def bin_to_str(byte_array: list) -> str:
        return ''.join([
            chr(c) if c > 32 and c < 127 else '.' for c in byte_array
        ])

    tmp = ''
    for i, byte in enumerate(byte_array):
        tmp = ''.join([tmp, f'{byte:02X}'])
        if (i+1) % num_in_line:
            tmp = ''.join([tmp, ' '])
        else:
            tmp = ''.join([
                tmp,
                space,
                bin_to_str(byte_array[i-num_in_line+1:i+1]),
                '\n'
            ])

    if (i+1) % num_in_line:
        tmp = ''.join([
            tmp,
            ' '*(3*(num_in_line - ((i+1) % num_in_line)) - 1),
            space,
            bin_to_str(byte_array[i - ((i+1) % num_in_line) + 1:]),
            '\n'
        ])

    print(tmp)
