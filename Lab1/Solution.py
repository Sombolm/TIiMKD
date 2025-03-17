from collections import defaultdict
import random

class Solution:

    def getConditionalProbabilityAccordingToPrevNChars(self, filePath, n) -> dict:
        file = open(filePath, 'r')
        accurances = defaultdict(int)
        conditionAccurances = defaultdict(int)

        for line in file:
            for i in range(n, len(line)):
                key = line[i -n: i + 1]
                accurances[key] += 1
                conditionAccurances[key[:-1]] += 1

        overallSum = sum(accurances.values())
        sumPropability = {key: accurances[key] / overallSum for key in accurances}

        conditionPropabilitySum = sum(conditionAccurances.values())
        conditionProbability = {key: conditionAccurances[key] / conditionPropabilitySum for key in conditionAccurances}

        conditionalProbability = {key: sumPropability[key] / conditionProbability[key[:-1]] for key in sumPropability}
        file.close()

        return conditionalProbability

    def getConditionalProbabilityAccordingToPrevNCharsV2(self, filePath, n) -> dict:
        file = open(filePath, 'r')
        accurances = defaultdict(int)

        for line in file:
            for i in range(n, len(line)):
                key = line[i -n: i + 1]
                accurances[key] += 1

        probabilitySum = sum(accurances.values())
        conditionalProbability = {key: accurances[key] / probabilitySum for key in accurances}

        file.close()

        return conditionalProbability

    def sortAccurances(self, accurances: dict):
        return sorted(accurances.items(), key=lambda x: x[1], reverse=True)

    def ShowTopAndBottomNChars(self, accurances: dict, n: int):
        sortedAccurances = self.sortAccurances(accurances)
        print("Top 5 characters: ", sortedAccurances[:n])
        print("Bottom 5 characters: ", sortedAccurances[-n:])

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

        print("Average word length: ", sum_ / count)

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

    def generateText(self, probability: defaultdict, length: int):
        text = ''
        chars = random.choices(list(probability.keys()), list(probability.values()), k=length)
        accurances = defaultdict(int)

        for char in chars:
            text += str(char)
            accurances[char] += 1

        return text, accurances

    def countAccurancesFromText(self, text: str):
        accurances = defaultdict(int)
        for char in text:
            accurances[char] += 1

        return accurances

    def generateMarkovText(self, order, filePath, textLength):
        probability = self.getConditionalProbabilityAccordingToPrevNCharsV2(filePath, order)
        text = ''

        #First chars
        chosenChars = random.choices(list(probability.keys()), list(probability.values()), k=1)
        text += chosenChars[0]

        textLength -= order

        for i in range(textLength):
            key = text[-order:]
            possibleChars = [char for char in probability if char.startswith(key)]
            probabilitiesForChars = [probability[char] for char in possibleChars]

            nextChar = random.choices(possibleChars, probabilitiesForChars, k=1)
            text += nextChar[0][-1]

        print(text)
        print(self.countAverageWordLengthFromString(text))
        print(self.ShowTopAndBottomNChars(self.countAccurancesFromText(text),5))

        return


    def run(self, filePath: str, order: int, length: int):

        '''
        accurances, propability = self.loadTextFile(filePath)
        self.ShowTopAndBottomNChars(accurances)
        self.countAverageWordLengthFromFile(filePath)


        generatedText, generatedTextAccurances = self.generateText(propability, sum(accurances.values()))
        self.ShowTopAndBottomNChars(generatedTextAccurances)
        self.countAverageWordLengthFromString(generatedText)
        '''

        self.generateMarkovText(order, filePath, length)

