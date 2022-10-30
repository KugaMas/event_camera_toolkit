import os
import sys
import cv2
import time
import argparse

import file as utf
import event as ute


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="a simple event visualization tool")
    parser.add_argument('-i', '--input_path', type=str,
                        default='./file/tests/demo-01.aedat4')
    parser.add_argument('-t', '--dt', type=float, default=1E4,
                        help='temporal interval to view /ms')
    parser.add_argument('-sz', '--size', type=list, default=[346, 260],
                        help='window size to view /pixel')
    parser.add_argument('--flag', action='store_true', help='whether to write .png files')
    args = parser.parse_args()

    data = utf.load(args.input_path)
