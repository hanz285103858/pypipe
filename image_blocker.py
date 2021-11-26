import os
import math
import logging

import cv2
import colour
import numpy as np
import matplotlib.pyplot as plt


class ImageBlocker(object):
    def __init__(self, img, blocksize, func):
        self.__src = img
        self.__blocksize = blocksize
        self.__func = func
        self.__srcp = None
        self.__srcrow, self.__srccol, self.__srcch = img.shape
        self.__blockrow, self.__blockcol = blocksize
        self.__blocknumrow, self.__blocknumcol = self._calcblocknum()
        self.__blocksrc = []
        self.__blockdst = []
        self.__dst = None

    def get_blocksize(self):
        return self.__blocksize

    def set_blocksize(self, blocksize):
        self.__blocksize = blocksize
        self.__blocknumrow, self.__blocknumcol = self._calcblocknum()

    def get_dst(self):
        self._blocking()
        self._processing()
        self._reconstruct()
        return self.__dst

    def _calcBlockNum(self):
        if self.__srcrow % self.__blockrow:
            blocknumrow = self.__srcrow // self.__blockrow + 1
        else:
            blocknumrow = self.__srcrow // self.__blockrow
        if self.__srccol % self.__blockcol:
            blocknumcol = self.__srccol // self.__blockcol + 1
        else:
            blocknumrow = self.__srccol // self.__blockcol
        return blocknumrow, blocknumcol

    def _padding(self):
        if self.__srcrow % self.__blockrow == 0 and self.__srccol % self.__blockcol == 0:
            self.__srcp = self.__src
        else:
            rowpadend = 0
            colpadend = 0
            if self.__srcrow % self.__blockrow:
                rowpadend = self.__blockrow - self.__srcrow % self.__blockrow
            if self.__srccol % self.__blockcol:
                colpadend = self.__blockcol - self.__srccol % self.__blockcol
            self.__srcp = np.pad(self.__src, ((0, rowpadend), (0, colpadend), (0, 0), 'symmetric'))


    def _blocking(self):
        self._padding()
        for i in range(self.__blocknumrow):
            for j in range(self.__blocknumcol):
                block = self.__srcp[i*self.__blockrow:(i+1)*self.__blockrow, j*self.__blockcol:(j+1)*self.__blockcol, :]
                self.__blocksrc.append(block)

    def _processing(self):
        self.__blockdst = list(map(self.__blocksrc, self.__func))

    def _reconstruct(self):
        dstch = self.__blockdst[0].shape[2]
        dstrow, dstcol, _ = self.__srcp.shape
        self.__dst = np.zeros((dstrow, dstcol, dstch))
        for i in range(self.__blocknumrow):
            for j in range(self.__blocknumcol):
                idx = i * self.__blocknumcol + j
                self.__dst[i * self.__blockrow:(i + 1) * self.__blockrow, j * self.__blockcol:(j + 1) * self.__blockcol, :] = self.__blockdst[idx]
        self.__dst = self.__dst[:self.__srcrow, :self.__srccol, :]


def test():
    pass


if __name__ == "__main__":
    test()