from collections import defaultdict
import random

class Solution:

    def getConditionalProbabilityAccordingToPrevNChars(self, filePath, n) -> dict:
        file = open(filePath, 'r')
        accurances = defaultdict(int)

        for line in file:
            for i in range(n, len(line)):
                key = line[i -n: i + 1]
                accurances[key] += 1

        overallSum = sum(accurances.values())
        conditionalProbability = {key: accurances[key] / overallSum for key in accurances}
        file.close()

        return conditionalProbability

    def sortAccurances(self, accurances: dict):
        return sorted(accurances.items(), key=lambda x: x[1], reverse=True)

    def ShowTopAndBottomNChars(self, accurances: dict):
        sortedAccurances = self.sortAccurances(accurances)
        #print("Top 5 characters: ", sortedAccurances[:5])
        #print("Bottom 5 characters: ", sortedAccurances[-5:])

    def countAverageWordLengthFromFile(self, path: str):
        file = open(path, 'r')

        sum_ = 0
        count = 0
        for line in file:
            words = line.split()
            for word in words:
                sum_ += len(word)
                count += 1
        file.close()
        #print("Average word length: ", sum_ / count)

    def countAverageWordLengthFromString(self, text: str):
        sum_ = 0
        count = 0
        words = text.split()
        for word in words:
            sum_ += len(word)
            count += 1

        #print("Average word length: ", sum_ / count)


    def loadTextFile(self, path: str):
        file = open(path, 'r')
        accurances = defaultdict(int)
        propability = defaultdict(float)

        for line in file:
            for char in line:
                accurances[char] += 1

        overAllSum = sum(accurances.values())
        for key in accurances:
            propability[key] = accurances[key] / overAllSum

        file.close()

        return accurances, propability

    def generateText(self, propability: defaultdict, length: int):
        text = ''
        chars = random.choices(list(propability.keys()), list(propability.values()), k=length)
        accurances = defaultdict(int)

        for char in chars:
            text += str(char)
            accurances[char] += 1

        return text, accurances

    def generateMarkovText(self, order, filePath, textLength):
        propability = self.getConditionalProbabilityAccordingToPrevNChars(filePath, order)
        text = ''

        chars = [x[-1] for x in propability.keys()]
        chosenChars = random.choices(chars, list(propability.values()), k=textLength)

        accurances = defaultdict(int)

        for char in chosenChars:
            text += str(char)
            accurances[char] += 1
        print(text)
        print(accurances)

        return text, accurances


    def run(self, filePath: str):

        '''
        accurances, propability = self.loadTextFile(filePath)
        self.ShowTopAndBottomNChars(accurances)
        self.countAverageWordLengthFromFile(filePath)


        generatedText, generatedTextAccurances = self.generateText(propability, sum(accurances.values()))
        self.ShowTopAndBottomNChars(generatedTextAccurances)
        self.countAverageWordLengthFromString(generatedText)
        '''

        self.generateMarkovText(6, filePath, 500)

