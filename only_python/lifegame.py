# -*- coding: utf-8 -*-

import random as rnd
import sys

import cv2
import numpy as np

from itertools import product
from six.moves import range

CELL_SIZE = 100
DISPLAY_CELL_RATIO = 2
MUTATE_RATIO = 0.001


def loop_check(v, max_) :
    while v < 0 :
        v += max_
    while v >= max_ :
        v -= max_
    return v


def get_around(frame, x, y, x_max, y_max) :
    count = -int(frame[x, y])
    for i, j in product(range(x - 1, x + 2), range(y - 1, y + 2)) :
        count += frame[loop_check(i, x_max), loop_check(j, y_max)]
    return count


def update(frame, next_frame) :
    for x, y in product(range(CELL_SIZE), range(CELL_SIZE)) :
        count = get_around(frame, x, y, CELL_SIZE, CELL_SIZE)
        if frame[x, y] == 0 and count == 3 :
            next_frame[x, y] = 1
        elif frame[x, y] == 1 and (count == 2 or count == 3) :
            next_frame[x, y] = 1
        elif frame[x, y] == 1 and (count <= 1 or count >= 4) :
            next_frame[x, y] = 0
        else :
            next_frame[x, y] = frame[x, y]

        ### Mutate
        if rnd.random() <= MUTATE_RATIO :
            next_frame[x, y] = 1 - next_frame[x, y]


def main(argv) :

    cell_size = (CELL_SIZE, CELL_SIZE)
    display_size = (int(CELL_SIZE * DISPLAY_CELL_RATIO), int(CELL_SIZE * DISPLAY_CELL_RATIO))

    frame = np.zeros(cell_size, np.uint8)
    next_frame = np.zeros(cell_size, np.uint8)

    ### Random
    for x, y in product(range(CELL_SIZE), range(CELL_SIZE)) :
        frame[x, y] = 1 if rnd.random() <= 0.5 else 0

    while True :
        ### Update
        update(frame, next_frame)

        ### Display
        display_frame = next_frame * 255
        display_frame = cv2.resize(display_frame, display_size, interpolation = cv2.INTER_NEAREST)
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

