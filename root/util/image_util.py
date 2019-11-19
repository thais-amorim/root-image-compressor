#!/usr/bin/python
import imageio
import numpy as np


class ImageUtil():
    @staticmethod
    def read_image(image_path, type="RGB"):
        return imageio.imread(image_path, as_gray=False, pilmode=type)

    @staticmethod
    def save_image(name, image_as_byte):
        imageio.imwrite(name, image_as_byte)

    @staticmethod
    def get_image_dimensions(img):
        data = np.array(img)
        height = data.shape[0]
        try:
            width = data.shape[1]
        except:
            width = 1
        return height, width
