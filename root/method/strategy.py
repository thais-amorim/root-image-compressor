from root.method import Huffman
from root.method import HuffmanWithScale

METHODS = ["huffman", "huffman_with_scale"]


class Strategy():

    @staticmethod
    def compress(method, filename):
        method = method.strip().lower()
        print("Compressing", filename, "using", method, "technique")
        print("\n")

        saved_path = "nowhere"
        initial = 0
        final = 0

        if method not in METHODS:
            print("We have not implemented the method " +
                  str(method) + " for compression. Sorry :(")
        elif "huffman" == method:
            compressor = Huffman(filename)
            saved_path, initial, final = compressor.compress()
        elif "huffman_with_scale" == method:
            compressor = HuffmanWithScale(filename)
            saved_path, initial, final = compressor.compress()

        print("Initial size:", format(initial, ","), "bytes")
        print("Final size:", format(final, ","), "bytes")
        print("Compression percentage:",
              Strategy.get_percentage(initial, final), "%")
        print("Image was saved at", saved_path)

    @staticmethod
    def decompress(method, filename):
        method = method.strip().lower()
        print("Decompressing", filename, "using", method, "technique")

        saved_path = ""

        if "huffman" == method:
            compressor = Huffman(filename)
            saved_path = compressor.decompress()
        elif "huffman_with_scale" == method:
            compressor = HuffmanWithScale(filename)
            saved_path = compressor.decompress()
        else:
            print("We have not implemented the method " +
                  str(method) + "for decompression. Sorry :(")

        print("Image was saved at", saved_path)

    @staticmethod
    def get_percentage(initial, final):
        if initial == 0 or final == 0:
            return 0
        else:
            p = 100 * ((final - initial) / initial)
            return round(p, 2)
