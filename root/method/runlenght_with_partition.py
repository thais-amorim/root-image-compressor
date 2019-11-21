class RunLengthPartition():

    def __init__(self, filename):
        self.filename = filename
        self.compress_filename = filename + '.rle2'
        self.decompress_filename = "images/output_rle_partition.bmp"

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

        divider = self.decide_divider()

        all_bytes = self.read_bytes(self.filename)
        self.initial_bytes_amount = len(all_bytes)
        previous_byte = -1
        count = 0
        output_bits = b''
        for i, b in enumerate(all_bytes[:int(len(all_bytes)/divider)], start=1):

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

        output_bits = output_bits + all_bytes[int(len(all_bytes)/divider):]
        header_bits = bytes([divider])
        self.write_bytes(self.compress_filename,header_bits, output_bits)
        self.final_bytes_amount = len(output_bits)
        return self.compress_filename, self.initial_bytes_amount, self.final_bytes_amount

    def read_bytes(self, input_path):
        all_bytes = []
        with open(input_path, 'rb') as binaryfile:
            all_bytes = binaryfile.read()
        return all_bytes

    def write_bytes(self, output_path, header_bytes, output_bytes):
        with open(output_path, 'wb') as out_file:
            out_file.write(header_bytes)
            out_file.write(output_bytes)

    def decompress(self):

        with open(self.filename, 'rb') as input_file:
            divider = int.from_bytes(input_file.read(1),sys.byteorder)
            rle = input_file.read()
        output_bytes = b''
        for i in range(0, int(len(rle)/divider), 2):
            rep = int(rle[i])
            value = rle[i + 1]
            for j in range(rep):
                output_bytes = output_bytes + bytes([value])

        output_bytes = output_bytes + rle[int(len(rle)/divider) : ]

        with open(self.decompress_filename, 'wb') as output_file:
            output_file.write(output_bytes)
        return self.decompress_filename

    def analise_repetitions(self, tolerance):
        all_bytes = self.read_bytes(self.filename)
        previous_byte = -1
        previous_pos = 0
        total_repetitions = 0
        count = 0
        repetitions = []
        for i,b in enumerate(all_bytes,start=0):
            if (b != previous_byte) or count >= 255:
                if previous_byte != -1:
                    
                    if(count>=tolerance):
                        total_repetitions += count
                        # print("prev_pos: " + str(previous_pos) )
                        repetitions.append([previous_pos,count])
                count = 0
                previous_byte = b
                previous_pos = i
                
            else:
                count += 1
        total_repetitions += count
        # print(repetitions)
        # print("Lenght of repetitions:" + str(len(repetitions)))
        # print("Total repetitions:" + str(total_repetitions))
        # print("Last index: " + str(repetitions[len(repetitions)-1][0]))
        # print("Last index minus total repetition: " + str(repetitions[len(repetitions)-1][0] - total_repetitions))
        # print(len(all_bytes))
        if(len(repetitions)>0 and total_repetitions>0):
            return repetitions[len(repetitions)-1][0], total_repetitions
        return 1,0

    def decide_divider(self):
        all_bytes = self.read_bytes(self.filename)
        best_index, best_rep = 1,0
        for i in range(50,255,30):
            index, total_rep = self.analise_repetitions(i)
            if(total_rep/index > best_rep/best_index):
                best_index,best_rep = index,total_rep
        # print(best_index,best_rep)
        if((best_rep,best_index > 0.5) and (len(all_bytes)/best_index) <255):
            # print(len(all_bytes)/best_index)
            return int(len(all_bytes)/best_index)
        else:
            return 1

f = RunLengthPartition("images/benchmark.bmp.rle2")
# f.analiserRepetitions(100)
# x = f.decide_divider()
# print(x)
# f.compress()
# f.analiseImage(0)
f.decompress()