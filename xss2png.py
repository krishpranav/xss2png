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