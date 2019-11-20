class RunLength():

    def __init__(self, filename):
        self.filename = filename
        self.compress_filename = filename + '.rle'
        self.decompress_filename = "images/output_huffman.bmp"

    def analiseImage(self, tolerance):
        all_bytes = self.read_bytes(self.filename)
        previous_byte = -1
        total_repetitions = 0
        count = 0
        for b in all_bytes:
            if (b != previous_byte) or count >= 255:
                if previous_byte != -1:
                    total_repetitions += count
                count = 0
                previous_byte = b
            else:
                count += 1
        total_repetitions += count
        image_size = len(all_bytes)
        compressed_size = 2 * (len(all_bytes) - total_repetitions)
        print("Total Repetitions: " + str(total_repetitions))
        print("Original Size: " + str(image_size))
        print("Compressed Size: " + str(compressed_size))
        if(float(compressed_size) / (image_size) < (1 - tolerance)):
            return True
        return False

    def compress(self):
        all_bytes = self.read_bytes(self.filename)
        self.initial_bytes_amount = len(all_bytes)
        previous_byte = -1
        count = 0
        output_bits = b''
        for i, b in enumerate(all_bytes, start=1):

            if (b != previous_byte) or count >= 255:
                if previous_byte != -1:
                    output_bits = output_bits + bytes([count])
                    output_bits = output_bits + bytes([previous_byte])
                count = 1
                previous_byte = b
            else:
                count += 1
        output_bits = output_bits + bytes([count])
        output_bits = output_bits + bytes([previous_byte])

        self.write_bytes(self.compress_filename, output_bits)
        self.final_bytes_amount = len(output_bits)
        return self.compress_filename, self.initial_bytes_amount, self.final_bytes_amount

    def read_bytes(self, input_path):
        all_bytes = []
        with open(input_path, 'rb') as binaryfile:
            all_bytes = binaryfile.read()
        return all_bytes

    def write_bytes(self, output_path, output_bytes):
        with open(output_path, 'wb') as out_file:
            out_file.write(output_bytes)

    def decompress(self):

        with open(self.filename, 'rb') as input_file:
            rle = input_file.read()
        output_bytes = b''
        for i in range(0, len(rle), 2):
            rep = int(rle[i])
            value = rle[i + 1]
            for j in range(rep):
                output_bytes = output_bytes + bytes([value])

        with open(self.decompress_filename, 'wb') as output_file:
            output_file.write(output_bytes)
        return self.decompress_filename
