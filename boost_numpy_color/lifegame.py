# -*- coding: utf-8 -*-

import random as rnd
import sys

import cv2
import numpy as np

from itertools import product
from six.moves import range

import build.liblifegame as lifegame

CELL_SIZE = 100
DISPLAY_CELL_RATIO = 2
MUTATE_RATIO = 0.001


def update(frame, next_frame) :
    lifegame.lifegame_update(frame, next_frame, MUTATE_RATIO)


def main(argv) :

    cell_size = (CELL_SIZE + 2, CELL_SIZE + 2)
    display_size = (int(CELL_SIZE * DISPLAY_CELL_RATIO), int(CELL_SIZE * DISPLAY_CELL_RATIO))

    frame = np.zeros((cell_size[0], cell_size[1], 3), int)
    next_frame = np.zeros((cell_size[0], cell_size[1], 3), int)

    ### Random
    for x, y, c in product(range(1, CELL_SIZE), range(1, CELL_SIZE), range(3)) :
        frame[x, y, c] = 1 if rnd.random() <= 0.5 else 0

    while True :
        ### Update
        for c in range(3) :
            nc = c + 1 if c + 1 < 3 else 0
            update(frame[:, :, c], next_frame[:, :, nc])

        ### Display
        display_frame = next_frame * 255
        display_frame = cv2.resize(display_frame, display_size, interpolation = cv2.INTER_NEAREST)
        display_frame = display_frame.astype(np.uint8)
        cv2.imshow("Window", display_frame)

        key = cv2.waitKey(30)
        if key == ord('q') :
            break

        ### Next frame
        tmp_frame = frame
        frame = next_frame
        next_frame = tmp_frame
        next_frame[:] = 0

if __name__ == '__main__' :
    main(sys.argv)

