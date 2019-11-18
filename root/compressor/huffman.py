import sys
import os
from math import ceil

LEFT = '1'
RIGHT = '0'


class Huffman():
    def __init__(self, filename):
        self.filename = filename
        self.outputname = filename + '.huffman'

    def compress(self):
        all_bytes = self.read_bytes(self.filename)
        print('Initial bytes amount: ', len(all_bytes))

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

        self.write_bytes(self.outputname, header_bytes, output_bytes)
        print('Final bytes amount: ', len(output_bytes) + len(header_bytes))

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
