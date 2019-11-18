from root.util import ImageUtil as util
from root.util import RgbUtil as rgb
import numpy as np

_MAX_INTENSITY = 255


class LzwCompressor():

    def __init__(self, image):
        self.image = image

    def compress(self):
        self.height, self.width = util.get_image_dimensions(self.image)
        self.red, self.green, self.blue = rgb.get_rgb_layers(self.image)

        compressed_r = self.compress_color_layer(self.red)
        compressed_g = self.compress_color_layer(self.green)
        compressed_b = self.compress_color_layer(self.blue)

        breakpoint()
        compressed_img = rgb.merge_rgb_layers(
            compressed_r, compressed_b, compressed_g)

        return compressed_img

    def compress_color_layer(self, uncompressed):
        height, width = util.get_image_dimensions(uncompressed)
        obtained = np.zeros((height, width), np.uint8)

        # Build the dictionary.
        dict_size = _MAX_INTENSITY + 1
        dictionary = {chr(i): i for i in range(dict_size)}

        w = ""
        result = []
        for row in range(height):
            for column in range(width):
                pixel = uncompressed[row][column]

                #current word + current image pixel
                if w == "":
                    wc = str(pixel)
                else:
                    wc = str(w) + "-" +str(pixel)
                # breakpoint()

                if wc in dictionary:
                    w = wc
                else:
                    obtained[row][column] = dictionary.get(w, -1)
                    # Add wc to the dictionary.
                    dictionary[wc] = dict_size
                    dict_size += 1
                    w = str(pixel)

            if w:
                obtained[row][column] = dictionary.get(w, -1)

        return obtained
