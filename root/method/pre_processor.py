from root.method import Method
from root.method import RunLength

class PreProcessor():

    def __init__(self, filename):
        self.filename = filename
        self.extension = filename.split('.')[-1]

    def get_compression_method(self, is_lossy):
        print("\nStarting PreProcessor analyse...")
        compressor = RunLength(self.filename)
        if(compressor.analiseImage(0.1)):
            print("The image is good to be compacted with RunLenght\n")
            return 'runlength'
        elif is_lossy:
            print("The image is good to be compacted with Huffman with scale\n")
            return 'huffman_with_scale'
        else:
            print("The image is good to be compacted with Huffman\n")
            return 'huffman'

    def get_decompression_method(self):
        print("\nStarting PreProcessor analyse...")
        try:
            method = Method(self.extension).name
            print("The image should be descompacted using",method,"\n")
            return method
        except:
            print("We do not know how to decompress extension", self.extension)
