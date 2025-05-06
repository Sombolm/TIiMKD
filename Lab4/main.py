import BInaryCoder

bincoder = BInaryCoder.BinaryCoder()

def testFunctions():
    text = "hello world"
    frequencies = bincoder.getFrequenciesFromText(text)
    print("Frequencies: ", frequencies)

    code = bincoder.create(frequencies)
    print("Code: ", code)

    encodedText = bincoder.encode(text, code)
    print("Encoded Text: ", encodedText)
    decodedText = bincoder.decode(encodedText, code)
    print("Decoded Text: ", decodedText)

    bincoder.save("encoded.txt", code, encodedText)

    code , encodedText = bincoder.load("encoded.txt")
    print("Decoded Text: ", bincoder.decode(encodedText, code))

def testFromFile():
    filename = "Dane/norm_wiki_sample.txt"
    frequencies, text = bincoder.getFrequenciesAndTextFromFile(filename)
    print("Frequencies: ", frequencies)

    code = bincoder.create(frequencies)
    print("Code: ", code)

    encodedText = bincoder.encode(text, code)
    symbolLen = len(list(code.values())[0])
    print("First 10 Encoded Text: ", encodedText[:10 *symbolLen])

    #decodedText = bincoder.decode(encodedText, code)
    #print("First 10 Decoded Text: ", decodedText[:10])

    bincoder.save("encoded", code, encodedText)

    code , encodedText = bincoder.load("encoded")
    print("First 10 decoded text from file: ", bincoder.decode(encodedText, code)[:10])
    print("Code from file: ", code)

    print("Average code length: ", bincoder.getAvgCodeLength())
    print("Code efficiency: ", bincoder.getCodeEfficiency())


def main():
    # testFunctions()
    testFromFile()

if __name__ == "__main__":
    main()