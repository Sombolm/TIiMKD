import os.path
from collections import defaultdict
from bitarray import bitarray
import math

class LZWCoder:
    def __init__(self, max_dict_size=None):
        self.max_dict_size = max_dict_size if max_dict_size else float('inf')
        self.frequencies = defaultdict(int)
        self.codeLengths = {}

    def getAvgCodeLength(self) -> float:
        if not self.frequencies:
            return 0
        total_bits = sum(self.codeLengths[symbol] * freq for symbol, freq in self.frequencies.items())
        total_symbols = sum(self.frequencies.values())
        return total_bits / total_symbols

    def getCodeEfficiency(self) -> float:
        avg_code_length = self.getAvgCodeLength()
        if avg_code_length == 0:
            return 0
        sum_frequency = sum(self.frequencies.values())
        entropy = -sum((self.frequencies[symbol] / sum_frequency) * math.log2(self.frequencies[symbol] / sum_frequency) for symbol in self.frequencies)
        return entropy / avg_code_length

    def encode(self, text):
        dictionary = {chr(i): i for i in range(256)}
        current = ''
        next_code = 256
        encoded = bitarray()
        code_lengths = defaultdict(int)

        for char in text:
            self.frequencies[char] += 1
            combined = current + char
            if combined in dictionary:
                current = combined
            else:
                code = dictionary[current]
                bits_needed = max(9, (next_code - 1).bit_length())
                encoded.extend(f"{code:0{bits_needed}b}")
                code_lengths[current] = bits_needed
                if next_code < self.max_dict_size:
                    dictionary[combined] = next_code
                    next_code += 1
                current = char

        if current:
            code = dictionary[current]
            bits_needed = max(9, (next_code - 1).bit_length())
            encoded.extend(f"{code:0{bits_needed}b}")
            code_lengths[current] = bits_needed

        self.codeLengths = code_lengths
        return encoded

    def decode(self, encodedText):
        dictionary = {i: chr(i) for i in range(256)}
        next_code = 256
        max_bits = max(9, (next_code - 1).bit_length())
        decoded = ''
        prev_entry = ''

        encoded_string = encodedText.to01()
        i = 0

        while i < len(encoded_string):
            code = int(encoded_string[i:i+max_bits], 2)
            i += max_bits

            if code in dictionary:
                entry = dictionary[code]
            elif code == next_code:
                entry = prev_entry + prev_entry[0]
            else:
                raise ValueError(f"Invalid LZW code: {code}")

            decoded += entry

            if prev_entry and next_code < self.max_dict_size:
                dictionary[next_code] = prev_entry + entry[0]
                next_code += 1
                max_bits = max(9, (next_code - 1).bit_length())

            prev_entry = entry

        return decoded

    def save(self, filename, encodedText: bitarray) -> bool:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        if len(encodedText) % 8 != 0:
            padding = 8 - len(encodedText) % 8
            encodedText.extend('0' * padding)
        else:
            padding = 0

        with open(filename, 'wb') as encodedFile:
            encodedFile.write(padding.to_bytes(1, 'big'))
            encodedText.tofile(encodedFile)

        print(f"Encoded data saved to {filename}")
        return True

    def load(self, filename) -> bitarray:
        encodedText = bitarray()
        with open(filename, 'rb') as encodedFile:
            padding = int.from_bytes(encodedFile.read(1), 'big')
            encodedText.fromfile(encodedFile)
            if padding:
                encodedText = encodedText[:-padding]
        return encodedText

    def getFrequenciesAndTextFromFile(self, filename) -> tuple:
        with open(filename, 'r') as file:
            text = file.read()
        frequencies = defaultdict(int)
        for char in text:
            frequencies[char] += 1
        return frequencies, text

    def compareFileSizes(self, original_file, encoded_file):
        original_size = os.path.getsize(original_file)
        encoded_size = os.path.getsize(encoded_file)
        print(f"Original File Size: {original_size} bytes")
        print(f"Encoded File Size: {encoded_size} bytes")
        print(f"Compression Ratio: {original_size / encoded_size:.2f}")

def testFromFile():
    filename = "Dane/norm_wiki_sample.txt"
    coder = LZWCoder(max_dict_size=2**18)
    frequencies, text = coder.getFrequenciesAndTextFromFile(filename)
    print("Frequencies: ", dict(list(frequencies.items())[:10]))

    encodedText = coder.encode(text)
    coder.save("encoded/encoded.lzw", encodedText)

    loadedText = coder.load("encoded/encoded.lzw")
    decodedText = coder.decode(loadedText)

    print("First 100 Encoded Bits: ", encodedText[:100])
    print("First 100 Decoded Characters: ", decodedText[:100])

    print("Average code length: ", coder.getAvgCodeLength())
    print("Code efficiency: ", coder.getCodeEfficiency())

    coder.compareFileSizes(filename, "encoded/encoded.lzw")

testFromFile()
