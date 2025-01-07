import math
import pprint
import sys

import n3lang.n3recovery
from n3sort import n3c_sort
from n3utils import colorize_bool, get_n3sort_values, get_sum_width, list_to_str, progress


def n3c_validation():
    verbose = 1
    # print(get_annotation())
    # print(f"Decompressing...")
    for width in range(1, 7):
        # [8, 32, 512,  65536]
        results = dict()
        for d in range(2 ** width):
            s = f"{d:{width}b}".replace(" ", "0")
            arr = [int(char) for char in s]
            data = arr[:]
            if verbose > 0:
                print(f"Compressing...\n")
            values = n3c_sort(data, verbose)
            values["width"] = width
            values["verbose"] = 1
            values.__delitem__("data")
            values.__delitem__("zeros")
            recovery = n3lang.n3recovery.n3c_recovery(**values)
            assertion = recovery == s
            print(f"{colorize_bool(assertion)} width={width} " + \
                  f"'{s}' -> '{recovery}'")
            assert assertion


def main(degrees=None, verbose=0) -> str:
    # if degrees is None:
    #     windows = [i for i in range(1, 2**20)]
    # else:
    #     windows = [2 ** i for i in degrees]
    result = ""
    index = 0
    width = 0
    while True:
        index += 1
        if degrees is None:
            width += 1
        else:
            width = 2 ** index
        summa = get_sum_width(width)
        # summa = math.ceil(summa)
        max_count = 2 ** summa
        max_ones = width
        max_bits_key = summa + math.ceil(math.log2(max_ones + 1)) + 1
        percent = max_bits_key / width
        if degrees is None:
            result += \
            f"w={width}, summa={summa}\n"
        else:
            result += \
            f"index={str(index).rjust(1, ' ')}, " + \
            f"width={str(width).rjust(5, ' ')}, " + \
            f"summa={str(summa)[:3].rjust(2, ' ')}, " + \
            f"max_count={str(max_count).rjust(14, ' ')}, " + \
            f"max_ones={str(max_ones).rjust(5, ' ')}, " + \
            f"max_bits_key={str(max_bits_key).rjust(2, ' ')}, " + \
            f"percent={str(100 * percent)[:6].rjust(6, ' ')}%\n"
        if verbose > 0:
            print(result)
    return result


if __name__ == "__main__":
    # ? P(W)
    # P(W) = Limit[Sum[Log[2, W + 1], {W, 0, Log[2, 2 ^ N - 1]}]] as N->M
    # 0.5 <= P(W) > 0
    # N=5: 10>=(Sum[Log[2, W + 1], {W, 0, Log[2, 2 ^ N - 1]}])>0
    # plot (4 * Ceiling[log2(w)]+2)/w, w=23 to 32
    # w>=23: TRUE = 1 > ((4 * Ceiling[log2(w)]+2)/w)
    # w=22+4.i: 1 = ((4 * Ceiling[log2(w)] + 2) / w)
    # 1 == ((4*Ceiling[Log2[22 + y*I]] + 2)/(22 + y*I))
    # y=4: 1 == ((4*Ceiling[Log2[22 + y*I]] + 2)/(22 + y*I))

    # n3c_get_path_by_name(degrees=[3, 9, 23, 55], verbose=1)
    # n3c_get_path_by_name(verbose=1)

    n3c_validation()
