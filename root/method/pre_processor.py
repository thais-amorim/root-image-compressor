import imageio
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as colors


class PreProcessor():

    def __init__(self, filename):
        self.filename = filename
        self.extension = filename.split('.')[-1]

    def read_bytes(self, input_path):
        all_bytes = []
        with open(input_path, 'rb') as binaryfile:
            all_bytes = binaryfile.read()
        return all_bytes

    def write_bytes(self, output_path, output_bytes):
        with open(output_path, 'wb') as out_file:
            out_file.write(output_bytes)
