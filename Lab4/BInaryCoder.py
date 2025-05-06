import math
import os.path
from collections import defaultdict
from bitarray import bitarray

class BinaryCoder:

    def __init__(self):
        self.frequencies = defaultdict(int)
        self.codeLengths = dict

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

    def getAvgCodeLength(self) -> float:
        return (sum([self.codeLengths[symbol] * freq for symbol, freq in self.frequencies.items()]) / sum(self.frequencies.values()))

    def getCodeEfficiency(self) -> float:

        avgCodeLength = self.getAvgCodeLength()
        sumFrequency = sum(self.frequencies.values())
        entropy = -sum((self.frequencies[symbol] / sumFrequency) * math.log2(self.frequencies[symbol] / sumFrequency) for symbol in
                       self.frequencies)

        return entropy / avgCodeLength if avgCodeLength > 0 else 0

    def create(self, frequencies) -> dict:
        symbols = sorted(list(frequencies.keys()))
        numberOfSymbols = len(symbols)

        codeLength = math.ceil(math.log2(numberOfSymbols))
        codes = {}

        for idx, symbol in enumerate(symbols):
            code = bitarray(format(idx, f'0{codeLength}b'))
            codes[symbol] = code

        self.frequencies = frequencies
        self.codeLengths = {symbol: codeLength for symbol in symbols}

        return codes

    def encode(self, text, code):
        encodedText = bitarray()

        for char in text:
            if char in code:
                encodedText += code[char]
            else:
                print("Invalid character: ", char)

        return encodedText

    def decode(self, encodedText ,code):
        reversedCode = {tuple(v): k for k, v in code.items()}

        decodedText = ''
        symbolLen = len(list(code.values())[0])

        for i in range(0, len(encodedText), symbolLen):
            bits = encodedText[i:i + symbolLen]
            tupleBits = tuple(bits)
            if tupleBits in reversedCode:
                decodedText += reversedCode[tupleBits]
            else:
                #print("Invalid byte: ", bits)
                decodedText += '?'

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





