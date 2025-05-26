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
    decodedText = bincoder.decode(encodedText, code)
    print("First 10 decoded text from file: ", decodedText[:10])
    print("Code from file: ", code)
    print("Length of text: ", len(text))
    print("Length of decoded text: ", len(decodedText))
    for idx in range(len(text)):
        if decodedText[idx] != text[idx]:
            print(f"Mismatch at index {idx}: {decodedText[idx]} != {text[idx]}")
            print("Mismatched text: ", text[idx], " vs ", decodedText[idx])
            break

    print("Average code length: ", bincoder.getAvgCodeLength())
    print("Code efficiency: ", bincoder.getCodeEfficiency())

    bincoder.compareFileSizes(filename, "encoded/encoded.bin", "encoded/code.txt")


def main():
    # testFunctions()
    testFromFile()

if __name__ == "__main__":
    main()