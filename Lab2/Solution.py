from collections import defaultdict
import random



class Solution:

    runOnce = False

    def getConditionalProbabilityAccordingToPrevNWords(self,filePath, n):
        file = open(filePath, 'r')
        nPlusCount = defaultdict(int)
        nCount = defaultdict(int)

        for line in file:
            words = line.strip().split()
            for i in range(n, len(words)):
                context = tuple(words[i - n: i])
                nextWord = words[i]
                nPlusKey = context + (nextWord,)
                nPlusCount[nPlusKey] += 1
                nCount[context] += 1


        conditionalProbability = {
            key: nPlusCount[key] / nCount[key[:-1]]
            for key in nPlusCount
        }

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
        print("Average word length: ", sum_ / count)

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

    def generateMarkovText(self, order, filePath, textLengthInWords, startProbability):
        probability = self.getConditionalProbabilityAccordingToPrevNWords(filePath, order)
        text = []

        if startProbability:
            text.append('probability')
            textLengthInWords -= 1

            for words in probability:
                if words[0] == 'probability':
                    text.extend(words[1:order:])
                    textLengthInWords -= order
                    break

        else:
            chosenWords = random.choices(list(probability.keys()), list(probability.values()), k=1)
            reversedChosenWords = list(chosenWords[0])
            text.extend(reversedChosenWords[:order])

            textLengthInWords -= order

        for i in range(textLengthInWords):
            key = text[-order:]
            possibleWords = [list(words) for words in probability if list(words[:order]) == key]
            probabilities = [probability[tuple(words)] for words in possibleWords]

            nextWords = random.choices(possibleWords, probabilities, k=1)
            nextWord = nextWords[0][::-1]
            text.append(nextWord[0])

        return text


    def run(self, filePath: str, order: int, length: int, startProbability: bool):

        '''
        accurances, propability = self.loadTextFile(filePath)
        self.ShowTopAndBottomNChars(accurances)
        self.countAverageWordLengthFromFile(filePath)


        generatedText, generatedTextAccurances = self.generateText(propability, sum(accurances.values()))
        self.ShowTopAndBottomNChars(generatedTextAccurances)
        self.countAverageWordLengthFromString(generatedText)
        '''

        text = self.generateMarkovText(order, filePath, length, startProbability)

        print(text)

