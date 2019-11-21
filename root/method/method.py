from aenum import Enum


class Method(Enum):
    _init_ = 'compression_extension'

    runlength = 'rle'
    huffman = 'huf'
    huffman_with_scale = 'shuf'
    lzw = 'lzw'
    crominance = 'cro'

    def __str__(self):
        return self.string
