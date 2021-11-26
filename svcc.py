import os
import math
import logging

import cv2
import colour
import numpy as np
import matplotlib.pyplot as plt

from cc_base import CCbase
from image_blocker import ImageBlocker

class SVCC(CCbase):
    def __init__(self, img, ccm, nl, k):
        '''
        :param img: input numpy array with shape(row, col, ch)
        :param ccm: input ccm with shape(3, ch)
        :param nl: input noise level with shape(ch, )
        :param k: input blocksize
        '''
        self.__src = img
        self.__ccm = ccm
        self.__nl = nl
        self.__blocksize = (k, k)
        self.__blocker = ImageBlocker(img, self.__blocksize, self._block_apply)
        self.__dst = None

    def get_dst(self):
        return self.__blocker.get_dst()

    def _block_apply(self, block):
        blkrow, blkcol, blkch = block.shape
        block = block.reshape((-1, blkch)).T    # shape(ch, row*col)
        C = block @ block.T / (blkrow * blkcol)
        Cn = np.diag(self.__nl ** 2)
        CCMOpt = self.__ccm @ (C.T) @ (np.linalg.inv(C+Cn).T)
        block = CCMOpt @ block
        return block.T.reshape((blkrow, blkcol, 3))


def test():
    pass

if __name__ == "__main__":
    test()