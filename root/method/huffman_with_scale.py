import numpy as np
from root.method import Huffman
from root.util import ImageUtil as util


class HuffmanWithScale():
    def __init__(self, filename):
        self.filename = filename

    def get_nearest_neighbour_pixel_interpolation(self, img, posX, posY):
        out = []

        # Get integer parts of positions
        modXi = int(posX)
        modYi = int(posY)
        # Get fractional parts of positions
        modXf = posX - modXi
        modYf = posY - modYi
        # To avoid going over image bounderies
        height, width = util.get_image_dimensions(img)
        modXiPlusOneLim = min(modXi + 1, width - 1)
        modYiPlusOneLim = min(modYi + 1, height - 1)

        for channel in range(img.shape[2]):
            target = img[modYi, modXi, channel]
            out.append(int(target + 0.5))
        return out

    def apply_nearest_neighbour(self, img, scale):
        if scale <= 0:
            return img

        imHeight, imWidth = util.get_image_dimensions(img)
        enlargedShape = list(
            map(int, [imHeight * scale, imWidth * scale, img.shape[2]]))
        enlargedImg = np.empty(enlargedShape, dtype=np.uint8)
        enlargedHeight, enlargedWidth = util.get_image_dimensions(enlargedImg)
        rowScale = float(imHeight) / float(enlargedHeight)
        colScale = float(imWidth) / float(enlargedWidth)
        for row in range(enlargedHeight):
            for col in range(enlargedWidth):
                # Find position in original image
                oriRow = row * rowScale
                oriCol = col * colScale
                enlargedImg[row, col] = self.get_nearest_neighbour_pixel_interpolation(
                    img, oriCol, oriRow)

        return enlargedImg

    def get_bilinear_pixel_interpolation(self, img, posX, posY):
        out = []

        # Get integer parts of positions
        modXi = int(posX)
        modYi = int(posY)
        # Get fractional parts of positions
        modXf = posX - modXi
        modYf = posY - modYi
        # To avoid going over image bounderies
        height, width = util.get_image_dimensions(img)
        modXiPlusOneLim = min(modXi + 1, width - 1)
        modYiPlusOneLim = min(modYi + 1, height - 1)

        # Get pixels in four corners
        for channel in range(img.shape[2]):
            bottom_left = img[modYi, modXi, channel]
            bottom_right = img[modYi, modXiPlusOneLim, channel]
            top_left = img[modYiPlusOneLim, modXi, channel]
            top_right = img[modYiPlusOneLim, modXiPlusOneLim, channel]

            # Calculate interpolation
            obtained_bottom = modXf * bottom_right + (1. - modXf) * bottom_left
            obtained_top = modXf * top_right + (1. - modXf) * top_left
            new_channel = modYf * obtained_top + (1. - modYf) * obtained_bottom
            out.append(int(new_channel + 0.5))

        return out

    def apply_bilinear_interpolation(self, img, scale):
        if scale <= 0:
            return img

        imHeight, imWidth = util.get_image_dimensions(img)
        enlargedShape = list(
            map(int, [imHeight * scale, imWidth * scale, img.shape[2]]))
        enlargedImg = np.empty(enlargedShape, dtype=np.uint8)
        enlargedHeight, enlargedWidth = util.get_image_dimensions(enlargedImg)
        rowScale = float(imHeight) / float(enlargedHeight)
        colScale = float(imWidth) / float(enlargedWidth)
        for row in range(enlargedHeight):
            for col in range(enlargedWidth):
                oriRow = row * rowScale  # Find position in original image
                oriCol = col * colScale
                enlargedImg[row, col] = self.get_bilinear_pixel_interpolation(
                    img, oriCol, oriRow)

        return enlargedImg

    def compress(self):
        COMPRESSED_EXTENSION = 'shuf'

        initial_bytes_amount = self.__read_bytes_amount(self.filename)
        img = util.read_image(self.filename)
        img = self.apply_bilinear_interpolation(img, 0.8)
        scaled_filename = self.__format_scaled_filename(self.filename)
        util.save_image(scaled_filename, img)
        compressor = Huffman(scaled_filename, COMPRESSED_EXTENSION)
        compressor.compress()
        return compressor.compress_filename, initial_bytes_amount, compressor.final_bytes_amount

    def __format_scaled_filename(self, original):
        splitted = original.split('.')
        splitted[0] += "_small"

        return '.'.join(splitted)

    def decompress(self):
        compressor = Huffman(self.filename)
        compressor.decompress()
        img = util.read_image(compressor.decompress_filename)
        img = self.apply_bilinear_interpolation(img, 1.25)
        scaled_filename = compressor.decompress_filename.replace(
            "small", "big")
        util.save_image(scaled_filename, img)
        return scaled_filename

    def __read_bytes_amount(self, input_path):
        all_bytes = []
        with open(input_path, 'rb') as binaryfile:
            all_bytes = binaryfile.read()
        return len(all_bytes)
