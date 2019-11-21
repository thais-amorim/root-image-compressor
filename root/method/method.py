from aenum import Enum

class Method(Enum):
    _init_ = 'compression extension'

    RUNLENGTH = 1, 'rle'
    HUFFMAN = 2, 'huf'
    HUFFMAN_WITH_SCALE = 3, 'shuf'
    LZW = 4, 'lzw'
    CROMINANCE = 5, 'cro'

    def __str__(self):
        return self.string

    @classmethod
    def get_name(self):
        return self.name.lower()

    @classmethod
    def contains(self, method):
        return method in Method.__members__
