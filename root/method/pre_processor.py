from root.method import Method
from root.method import RunLength

class PreProcessor():

    def __init__(self, filename):
        self.filename = filename
        self.extension = filename.split('.')[-1]

    def get_compression_method(self, is_lossy):
        compressor = RunLength(self.filename)
        if(compressor.analiseImage(0.1)):
            print("The image is good to be compacted with RunLenght and Huffman")
            return 'rle_plus_huff'
        elif is_lossy:
            print("The image is good to be compacted with Huffman")
            return 'huffman_with_scale'
        print("The image is good to be compacted with Huffman")
        return 'huffman'

    def get_decompression_method(self):
        try:
            return Method(self.extension).name
        except:
            print("We do not know how to decompress extension", self.extension)
