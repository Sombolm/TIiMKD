import LZWCoder

coder = LZWCoder.LZWCoder()

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
    print("First 10 decoded text from file: ", coder.decode(encodedText, code)[:10])
    print("Code from file: ", code)

    print("Average code length: ", coder.getAvgCodeLength())
    print("Code efficiency: ", coder.getCodeEfficiency())

def main():
    #testFunctions()
    testFromFile()

if __name__ == "__main__":
    main()