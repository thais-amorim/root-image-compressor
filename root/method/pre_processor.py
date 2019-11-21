from root.method import Method


class PreProcessor():

    def __init__(self, filename):
        self.filename = filename
        self.extension = filename.split('.')[-1]

    def get_compression_method(self, is_lossy):
        return None

    def get_decompression_method(self):
        try:
            return Method(self.extension).name
        except:
            print("We do not know how to decompress extension", self.extension)
