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
        next_code = 256
        current = ''
        encoded = bitarray()


        bits_needed = 9

        for char in text:
            combined = current + char
            if combined in dictionary:
                current = combined
            else:
                code_to_output = dictionary[current]

                encoded.extend(format(code_to_output, f'0{bits_needed}b'))
                if next_code < self.max_dict_size:
                    dictionary[combined] = next_code

                    if next_code >= (1 << bits_needed):
                        max_bits = (self.max_dict_size - 1).bit_length()
                        if bits_needed < max_bits:
                            bits_needed += 1

                    next_code += 1

                current = char

        if current:
            last_code = dictionary[current]
            encoded.extend(format(last_code, f'0{bits_needed}b'))

        return encoded

    def decode(self, encodedText):
        dictionary = {i: chr(i) for i in range(256)}
        next_code = 256
        decoded = ''

        bits_needed = 9

        encoded_string = encodedText.to01()
        i = 0

        if not encoded_string:
            return decoded

        if i + bits_needed <= len(encoded_string):

            code_bits = encoded_string[i:i + bits_needed]
            prev_code = int(code_bits, 2)


            i += bits_needed

            prev_entry = dictionary[prev_code]
            decoded += prev_entry


        while i < len(encoded_string):

            max_bits = (self.max_dict_size - 1).bit_length()
            if next_code >= (1 << bits_needed) and bits_needed < max_bits:
                bits_needed += 1
            # ----------------------------------------------------------------

            if i + bits_needed > len(encoded_string):
                print(
                    f"Warning: Incomplete code at the end. Index {i}, need {bits_needed}, remaining {len(encoded_string) - i} bits: '{encoded_string[i:]}'")
                break

            try:
                code_bits = encoded_string[i:i + bits_needed]
                code = int(code_bits, 2)
            except ValueError:
                raise ValueError(f"Invalid bits for code at index {i}: '{code_bits}' (expected {bits_needed} bits)")


            i += bits_needed

            if code in dictionary:
                entry = dictionary[code]
            elif code == next_code and next_code < self.max_dict_size:
                if prev_entry == "":
                    raise ValueError(
                        f"Invalid LZW sequence: KwKwK case (code={code}) encountered with no previous entry.")
                entry = prev_entry + prev_entry[0]
            else:
                raise ValueError(
                    f"Invalid LZW code encountered: {code} (dict size {len(dictionary)}, next_code {next_code}, reading {bits_needed} bits)")

            decoded += entry

            if next_code < self.max_dict_size:
                if prev_entry == "":
                    raise ValueError("Internal error: prev_entry is empty during dictionary update.")
                new_entry_str = prev_entry + entry[0]
                dictionary[next_code] = new_entry_str
                next_code += 1

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
    coder = LZWCoder(max_dict_size=2**12)
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