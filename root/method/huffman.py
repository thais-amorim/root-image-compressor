import sys
import os
from math import ceil

LEFT = '1'
RIGHT = '0'
COMPRESSED_EXTENSION = 'huf'


class Huffman():
    def __init__(self, filename, extension=COMPRESSED_EXTENSION):
        self.filename = filename
        self.compress_filename = filename + '.' + extension
        self.decompress_filename = self.__format_decompress_filename(filename)

    def __format_decompress_filename(self, original):
        splitted = original.split('.')[:-1]
        splitted[0] += "_out"

        return '.'.join(splitted)

    def compress(self):
        all_bytes = self.read_bytes(self.filename)
        self.initial_bytes_amount = len(all_bytes)

        byte_frequencies = self.get_frequency_per_value(all_bytes)
        leaves, _ = build_tree(byte_frequencies)

        symbol_map = {leaf.data[0]: leaf.code for leaf in leaves}

        output_bits = '1'
        for b in all_bytes:
            output_bits = output_bits + symbol_map[b]

        byte_count = (len(output_bits) + 7) // 8
        output_int = int(output_bits, 2)
        output_bytes = output_int.to_bytes(byte_count, sys.byteorder)
        max_count_bytes = ceil(leaves[-1].data[1].bit_length() / 8)

        header_bytes = len(leaves).to_bytes(2, sys.byteorder)
        header_bytes += max_count_bytes.to_bytes(8, sys.byteorder)

        for leaf in leaves:
            header_bytes += (leaf.data[0].to_bytes(1, sys.byteorder))
            header_bytes += leaf.data[1].to_bytes(
                max_count_bytes, sys.byteorder)

        self.write_bytes(self.compress_filename, header_bytes, output_bytes)
        self.final_bytes_amount = len(output_bytes) + len(header_bytes)
        return self.compress_filename, self.initial_bytes_amount, self.final_bytes_amount

    def get_frequency_per_value(self, all_bytes):
        byte_set = set(all_bytes)
        byte_frequencies_dict = {b: 0 for b in byte_set}

        for b in all_bytes:
            byte_frequencies_dict[b] = byte_frequencies_dict[b] + 1

        return sorted(
            [item for item in byte_frequencies_dict.items()], key=lambda item: item[1])

    def read_bytes(self, input_path):
        all_bytes = []
        with open(input_path, 'rb') as binaryfile:
            all_bytes = binaryfile.read()
        return all_bytes

    def write_bytes(self, output_path, header_bytes, output_bytes):
        with open(output_path, 'wb') as out_file:
            out_file.write(header_bytes)
            out_file.write(output_bytes)

    def decompress(self):
        input_bytes, byte_frequencies = self.read_compressed_file()
        _, tree = build_tree(byte_frequencies)
        input_bits = bin(int.from_bytes(input_bytes, sys.byteorder))[3:]
        output_bytes = b''
        current_node = tree
        for bit in input_bits:
            if bit == LEFT:
                current_node = current_node.left
            else:
                current_node = current_node.right

            if type(current_node) is Leaf:
                output_bytes += current_node.data[0]
                current_node = tree

        with open(self.decompress_filename, 'wb') as output_file:
            output_file.write(output_bytes)
        return self.decompress_filename

    def read_compressed_file(self):
        byte_frequencies = []
        input_bytes = None
        with open(self.filename, 'rb') as input_file:
            byte_frequencies = self.__get_byte_frequencies(
                input_file, byte_frequencies)
            input_bytes = input_file.read()
        return input_bytes, byte_frequencies

    def __get_byte_frequencies(self, input_file, byte_frequencies):
        leaves_count = int.from_bytes(input_file.read(2), sys.byteorder)
        max_count_bytes = int.from_bytes(input_file.read(8), sys.byteorder)
        while leaves_count > 0:
            b = input_file.read(1)
            c = int.from_bytes(input_file.read(max_count_bytes), sys.byteorder)
            byte_frequencies.append((b, c))
            leaves_count -= 1
        return byte_frequencies


class Leaf():
    def __init__(self, data, value):
        self.data = data
        self.value = value
        self.parent = None
        self.code = ''

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()

    def update_code(self, update):
        self.code = update + self.code


class Node():
    def __init__(self, left, right, value):
        self.value = value
        self.left = left
        self.right = right
        self.code = ''

        self.left.update_code(LEFT)
        self.right.update_code(RIGHT)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

    def update_code(self, update):
        self.code = update + self.code
        self.left.update_code(update)
        self.right.update_code(update)


def build_tree(byte_frequencies):
    tree = [Leaf(bf, bf[1]) for bf in byte_frequencies]

    leaves = []

    while len(tree) > 1:
        left, right = tree[:2]
        if isinstance(left, Leaf):
            leaves.append(left)
        if isinstance(right, Leaf):
            leaves.append(right)
        tree = tree[2:]
        node = Node(left, right, left.value + right.value)
        tree.append(node)
        tree = sorted(tree, key=lambda node: node.value)

    return leaves, tree[0]
