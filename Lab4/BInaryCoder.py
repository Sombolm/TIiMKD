import math
from collections import defaultdict

import json

class BinaryCoder:

    def __init__(self):
        pass

    def getFrequenciesFromText(self, text) -> dict:
        frequencies = defaultdict(int)

        for char in text:
            frequencies[char] += 1

        return frequencies
    def getFrequenciesFromFile(self, filename) -> dict:
        file = open(filename, 'r')
        frequencies = defaultdict(int)

        for line in file:
            for char in line.strip():
                frequencies[char] += 1

        return frequencies
    def getFrequenciesAndTextFromFile(self, filename) -> tuple:
        file = open(filename, 'r')
        frequencies = defaultdict(int)
        text = ''

        for line in file:
            text += line.strip()
            for char in line.strip():
                frequencies[char] += 1

        return frequencies, text

    def create(self, frequencies) -> dict:
        symbols = sorted(list(frequencies.keys()), key=lambda x: frequencies[x], reverse=True)
        numberOfSymbols = len(symbols)

        codeLength = math.ceil(math.log2(numberOfSymbols))
        codes = {}
        numberOfBytes = math.ceil(codeLength / 8)

        for idx, symbol in enumerate(symbols):
            code = bytearray(idx.to_bytes(numberOfBytes, byteorder='big'))
            codes[symbol] = code

        return codes

    def encode(self, text, code):
        encodedText = bytearray()

        for char in text:
            if char in code:
                encodedText += code[char]
            else:
                print("Invalid character: ", char)

        return encodedText

    def decode(self, encodedText ,code):
        reversedCode = {tuple(v): k for k, v in code.items()}

        decodedText = ''

        for i in range(0, len(encodedText), len(list(code.values())[0])):
            byte = encodedText[i:i + len(list(code.values())[0])]
            if tuple(byte) in reversedCode:
                decodedText += reversedCode[tuple(byte)]
            else:
                print("Invalid byte: ", byte)

        return decodedText

    def save(self, filename, code, encodedText) -> bool:


    def load(self, filename) -> tuple:
        pass

