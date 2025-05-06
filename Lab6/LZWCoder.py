import math
import os.path
from collections import defaultdict
from bitarray import bitarray



class LZWCoder:

    def __init__(self):

    def create(self, frequencies) -> dict:


        return codes

    def encode(self, text, code):
        encodedText = bitarray()

        for char in text:
            if char in code:
                encodedText += code[char]
            else:
                print("Invalid character: ", char)

        return encodedText

    def decode(self, encodedText, code):
        reversedCode = {v.to01(): k for k, v in code.items()}

        decodedText = ''
        buffer = ''

        for bit in encodedText.to01():
            buffer += bit
            if buffer in reversedCode:
                decodedText += reversedCode[buffer]
                buffer = ''

        return decodedText

    def save(self, filename, code, encodedText: bitarray) -> bool:
        os.makedirs(filename, exist_ok=True)

        if len(encodedText) % 8 != 0:
            padding = 8 - len(encodedText) % 8
            encodedText += bitarray('0' * padding)

        with open(os.path.join(filename, 'encoded.bin'), 'wb') as encodedFile:
            encodedText.tofile(encodedFile)
        encodedFile.close()

        with open(os.path.join(filename, 'code.txt'), 'w') as codeFile:
            for symbol, bits in code.items():
                codeFile.write(f"{symbol}:{bits.to01()}\n")
        codeFile.close()
        return True

    def load(self, filename) -> tuple:
        encodedText = bitarray()
        codes = {}

        with open(os.path.join(filename, 'code.txt'), 'r') as file:
            for line in file:
                symbol, code = line.split(':')
                codes[symbol] = bitarray(code.strip())
        file.close()

        with open(os.path.join(filename, 'encoded.bin'), 'rb') as file:
            encodedText.fromfile(file)
        file.close()

        symbolLen = len(list(codes.values())[0])

        if (len(encodedText) / symbolLen) % 8 != 0:
            padding = 8 - len(encodedText) % 8
            encodedText = encodedText[:-padding]

        return codes, encodedText





