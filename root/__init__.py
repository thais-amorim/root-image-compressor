from root.compressor import Huffman
from root.util import ImageUtil as util
import argparse

parser = argparse.ArgumentParser(description='Compresses or decompresses images.', epilog='Enjoy it! :)', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('filename', nargs=1, metavar='file name',type=str ,help='The complete path to target image.')
parser.add_argument('-d','--decompress', help='Decompress the image.', action='store_true')
parser.add_argument('-c','--compress', help='Compress the image.', action='store_true')
parser.add_argument('-m','--method', help='Set the used method', action='store_true', default='huffman')

args = parser.parse_args()

def main():
    if args.decompress:
        decompressor = Huffman(args.filename[0])
        decompressor.decompress()
    elif args.compress:
        compressor = Huffman(args.filename[0])
        compressor.compress()
    else:
        print("Use -c to compress or -d to decompress")


if __name__ == "__main__":
    main()
