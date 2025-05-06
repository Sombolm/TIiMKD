import math
import os.path
from collections import defaultdict
from bitarray import bitarray
import heapq

class Node:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __repr__(self):
        return f"Node({self.symbol}, {self.frequency})"

class HuffmanCoder:

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
        def buildCodes(node, code=""):
            if node.symbol is not None:
                codes[node.symbol] = bitarray(code)
                return
            buildCodes(node.left, code + '0')
            buildCodes(node.right, code + '1')


        heap = [Node(symbol, freq) for symbol, freq in frequencies.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = Node(None, left.frequency + right.frequency)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)

        root = heap[0]
        codes = {}

        buildCodes(root)
        self.frequencies = frequencies
        self.codeLengths = {symbol: len(code) for symbol, code in codes.items()}
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





