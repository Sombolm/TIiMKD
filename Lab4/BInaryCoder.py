import math
from collections import defaultdict
from bitarray import bitarray

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
        symbols = sorted(list(frequencies.keys()))
        numberOfSymbols = len(symbols)

        codeLength = math.ceil(math.log2(numberOfSymbols))
        codes = {}

        for idx, symbol in enumerate(symbols):
            code = bitarray(format(idx, f'0{codeLength}b'))
            codes[symbol] = code

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

    def save(self, filename, code, encodedText) -> bool:
        try:
            allBits = bitarray()

            numSymbols = len(code)
            allBits.frombytes(numSymbols.to_bytes(1, 'big'))

            codeLength = len(next(iter(code.values()))) if code else 0
            allBits.frombytes(codeLength.to_bytes(1, 'big'))

            for symbol, bits in code.items():
                symbolBytes = symbol.encode('utf-8')
                allBits.frombytes(len(symbolBytes).to_bytes(1, 'big'))
                allBits.frombytes(symbolBytes)
                allBits += bits

            allBits.frombytes(len(encodedText).to_bytes(4, 'big'))
            allBits += encodedText

            unusedBits = (8 - (len(allBits) % 8)) % 8
            if unusedBits:
                allBits.extend([0] * unusedBits)
            allBits.frombytes(unusedBits.to_bytes(1, 'big'))

            with open(filename, 'wb') as f:
                f.write(allBits.tobytes())

            return True
        except Exception as e:
            print("Error during save:", e)
            return False

    def load(self, filename) -> tuple:
        try:
            with open(filename, 'rb') as f:
                fileBits = bitarray()
                fileBits.fromfile(f)

                unusedBits = int.from_bytes(fileBits[-8:].tobytes(), 'big')
                del fileBits[-8:]
                if unusedBits:
                    del fileBits[-unusedBits:]

                pos = 0

                numSymbols = int.from_bytes(fileBits[pos:pos + 8].tobytes(), 'big')
                pos += 8

                codeLength = int.from_bytes(fileBits[pos:pos + 8].tobytes(), 'big')
                pos += 8

                code = {}
                for _ in range(numSymbols):
                    symbolLen = int.from_bytes(fileBits[pos:pos + 8].tobytes(), 'big')
                    pos += 8
                    symbolBytes = fileBits[pos:pos + 8 * symbolLen].tobytes()
                    symbol = symbolBytes.decode('utf-8')
                    pos += 8 * symbolLen
                    bits = fileBits[pos:pos + codeLength]
                    code[symbol] = bits
                    pos += codeLength

                textLength = int.from_bytes(fileBits[pos:pos + 32].tobytes(), 'big')
                pos += 32
                encodedText = fileBits[pos:pos + textLength]

                return code, encodedText
        except Exception as e:
            print("Error during load:", e)
            return {}, bitarray()


