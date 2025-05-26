import HuffmanCoder

coder = HuffmanCoder.HuffmanCoder()

def testFunctions():
    text = ("a"*5) + ("b"*9) + ("c"*12) + ("d"*13) + ("e"*16) + ("f"*45)
    frequencies = coder.getFrequenciesFromText(text)
    print("Frequencies: ", frequencies)

    code = coder.create(frequencies)
    print("Code: ", code)

    encodedText = coder.encode(text, code)
    print("Encoded Text: ", encodedText)
    decodedText = coder.decode(encodedText, code)
    print("Decoded Text: ", decodedText)

    coder.save("encoded.txt", code, encodedText)

    code , encodedText = coder.load("encoded.txt")
    print("Decoded Text from file: ", coder.decode(encodedText, code))


    print("Average code length: ", coder.getAvgCodeLength())
    print("Code efficiency: ", coder.getCodeEfficiency())

def testFromFile():
    filename = "Dane/norm_wiki_sample.txt"
    frequencies, text = coder.getFrequenciesAndTextFromFile(filename)
    print("Frequencies: ", frequencies)

    code = coder.create(frequencies)
    print("Code: ", code)

    encodedText = coder.encode(text, code)
    symbolLen = len(list(code.values())[0])
    print("First 10 Encoded Text: ", encodedText[:10 *symbolLen])

    decodedText = coder.decode(encodedText, code)
    print("First 10 Decoded Text: ", decodedText[:10])

    coder.save("encoded", code, encodedText)

    code , encodedText = coder.load("encoded")
    decodedText = coder.decode(encodedText, code)
    print("First 10 decoded text from file: ", decodedText[:10])
    print("Code from file: ", code)
    print("Length of text: ", len(text))
    print("Length of decoded text: ", len(decodedText))
    for idx in range(len(text)):
        if decodedText[idx] != text[idx]:
            print(f"Mismatch at index {idx}: {decodedText[idx]} != {text[idx]}")
            print("Mismatched text: ", text[idx], " vs ", decodedText[idx])
            break

    print("Average code length: ", coder.getAvgCodeLength())
    print("Code efficiency: ", coder.getCodeEfficiency())

    coder.compareFileSizes(filename, "encoded/encoded.bin", "encoded/code.txt")

def main():
    #testFunctions()
    testFromFile()

if __name__ == "__main__":
    main()