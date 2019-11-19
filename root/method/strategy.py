from root.method import Huffman
from root.method import RunLenght

class Strategy():

    @staticmethod
    def compress(method, filename):
        method = method.strip().lower()
        print("Compressing ",filename," using method",method)

        if "huffman" == method:
            compressor = Huffman(filename)
            compressor.compress()
        elif "runlenght" == method:
            compressor = RunLenght(filename)
            compressor.compress()
        else:
            print("We have not implemented the method " + str(method) + " for compression. Sorry :(")

    @staticmethod
    def decompress(method, filename):
        method = method.strip().lower()
        print("Decompressing ",filename," using method",method)

        if "huffman" == method:
            compressor = Huffman(filename)
            compressor.decompress()
        elif "runlenght" == method:
            compressor = RunLenght(filename)
            compressor.decompress()
        else:
            print("We have not implemented the method " + str(method) + "for decompression. Sorry :(")
