import imageio
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as colors


class Crominance():

    def __init__(self, filename):
        self.filename = filename
        self.compress_filename = filename + '.cro'
        self.decompress_filename = "images/output_huffman.bmp"

    def read_image(self, image_path):
        return imageio.imread(image_path, as_gray=False, pilmode="RGB")

    # Arredonda todos os últimos bits para 0, por exemplo: 255 vira 250, 123 vira 120
    def round_last_bit(self):
        image = self.read_image(self.filename)
        for k in range(3):
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    image[i, j, k] = int(image[i, j, k] / 10) * 10
        return image

    # Visando melhorar o runlenght, caso os bits estejam em uma certa tolerância, ele iguala ao próximo
    def match_bits(self):
        image = self.read_image(self.filename)
        for k in range(3):
            for i in range(image.shape[0] - 1):
                for j in range(image.shape[1]):
                    tol = 7
                    if(image[i, j, k] >= image[i + 1, j, k] - tol and image[i, j, k] <= image[i + 1, j, k] + tol):
                        image[i, j, k] = image[i + 1, j, k]
        return image

    # Tira a média dos 4 valores adjacentes no rgv
    def mean_4_adjacent(self):
        image = self.read_image(self.filename)
        for k in range(3):
            for i in range(0, image.shape[0], 2):
                for j in range(0, image.shape[1], 2):
                    mean = (float(image[i, j, k]) + float(image[i + 1, j, k]) +
                            float(image[i, j + 1, k]) + float(image[i + 1, j + 1, k])) / 4
                    image[i, j, k] = mean
                    image[i + 1, j, k] = mean
                    image[i, j + 1, k] = mean
                    image[i + 1, j + 1, k] = mean
        return image

    # tira a média dos 4 valores adjacentes no hsv
    def crominance_hsv_mean(self):
        image = self.read_image(self.filename)
        hsv = colors.rgb_to_hsv(image.astype(np.float) / 255)
        print((image.astype(np.float) / 255) * 255)
        for i in range(0, hsv.shape[0], 2):
            for j in range(0, hsv.shape[1], 2):
                mean_h = (hsv[i, j, 0] + hsv[i + 1, j, 0] +
                          hsv[i, j + 1, 0] + hsv[i + 1, j + 1, 0]) / 4
                mean_s = (hsv[i, j, 1] + hsv[i + 1, j, 1] +
                          hsv[i, j + 1, 1] + hsv[i + 1, j + 1, 1]) / 4
                hsv[i, j, 0] = hsv[i + 1, j, 0] = hsv[i,
                                                      j + 1, 0] = hsv[i + 1, j + 1, 0] = mean_h
                hsv[i, j, 1] = hsv[i + 1, j, 1] = hsv[i,
                                                      j + 1, 1] = hsv[i + 1, j + 1, 1] = mean_s
        image = (colors.hsv_to_rgb(hsv)) * 255
        print(image)
        return image.astype(np.uint8)

    def read_bytes(self, input_path):
        all_bytes = []
        with open(input_path, 'rb') as binaryfile:
            all_bytes = binaryfile.read()
        return all_bytes

    def write_bytes(self, output_path, output_bytes):
        with open(output_path, 'wb') as out_file:
            out_file.write(output_bytes)
