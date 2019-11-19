from root.method import Huffman

class Strategy():

    @staticmethod
    def compress(method, filename):
        method = method.strip().lower()
        print("Compressing ",args.filename[0]," using method",args.method)

        if "huffman" == method:
            compressor = Huffman(filename)
            compressor.compress()
        else:
            print("We have not implemented the method " + str(method) + " for compression. Sorry :(")

    @staticmethod
    def decompress(method, filename):
        method = method.strip().lower()
        print("Decompressing ",args.filename[0]," using method",args.method)

        if "huffman" == method:
            compressor = Huffman(filename)
            compressor.decompress()
        else:
            print("We have not implemented the method " + str(method) + "for decompression. Sorry :(")
