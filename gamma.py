import os
import math
import logging

import cv2
import colour
import numpy as np
import matplotlib.pyplot as plt

class Gamma(object):
    def __init__(self):
        raise NotImplementedError

    def apply(self):
        raise NotImplementedError

    def config(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError


def test():
    pass


if __name__ == "__main__":
    test()