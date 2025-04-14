import math
import os
from collections import defaultdict
import random

from sympy import print_glsl


class Solution:

    def getConditionalProbabilityAccordingToPrevNWords(self, filePath, n) -> dict:
        file = open(filePath, 'r')
        accurances = defaultdict(int)


        for line in file:
            words = line.strip().split(' ')
            for i in range(0, len(words), n):
                key = words[i:i+n + 1]
                accurances[tuple(key)] += 1

        probabilitySum = sum(accurances.values())
        conditionalProbability = {key: accurances[key] / probabilitySum for key in accurances}

        file.close()

        return conditionalProbability

    def getConditionalProbabilityAccordingToPrevNChars(self, filePath, n) -> dict:
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

    def getProbabilityForChars(self, filePath) -> dict:
        file = open(filePath, 'r')
        accurances = defaultdict(int)

        for line in file:
            for char in line:
                accurances[char] += 1

        probabilitySum = sum(accurances.values())
        probability = {key: accurances[key] / probabilitySum for key in accurances}

        file.close()

        return probability

    def getProbabilityForWords(self, filePath) -> dict:
        file = open(filePath, 'r')
        accurances = defaultdict(int)

        for line in file:
            words = line.strip().split(' ')
            for word in words:
                accurances[word] += 1

        probabilitySum = sum(accurances.values())
        probability = {key: accurances[key] / probabilitySum for key in accurances}

        file.close()

        return probability

    def calculateEntropy(self, probability: dict) -> float:
        entropy = 0
        for key in probability:
            entropy += probability[key] * math.log(probability[key], 2)
        return entropy * -1

    def calculateEntropyConditional(self, probability, conditionalProbability: dict) -> float:
        entropy = 0

        for key in conditionalProbability:
            sumProbability = 0
            for char in key:
                sumProbability += probability[char]

            entropy += sumProbability * math.log(conditionalProbability[key], 2)
        return entropy * -1

    def plotEntropies(self, charEntropies: dict, wordEntropies: dict, fileName) -> None:

        import matplotlib.pyplot as plt

        plt.plot(list(charEntropies.keys()), list(charEntropies.values()), label='Char Entropy')
        plt.plot(list(wordEntropies.keys()), list(wordEntropies.values()), label='Word Entropy')
        plt.xlabel('N')
        plt.ylabel('Entropy')
        plt.title('Entropy vs N for ' + fileName)
        plt.legend()
        plt.show()


    def run(self):

        fileNames = os.listdir('Dane')

        for filename in fileNames:
            filePath = os.path.join('Dane', filename)

            probabilityForChars = self.getProbabilityForChars(filePath)
            probabilityForWords = self.getProbabilityForWords(filePath)

            charEntropies = dict()
            wordEntropies = dict()

            charEntropies[0] = self.calculateEntropy(probabilityForChars)
            wordEntropies[0] = self.calculateEntropy(probabilityForWords)

            for i in range(1,4):
                conditionalProbabilityForChars = self.getConditionalProbabilityAccordingToPrevNChars(filePath, i)
                conditionalProbabilityForWords = self.getConditionalProbabilityAccordingToPrevNWords(filePath, i)

                charEntropies[i] = self.calculateEntropyConditional(probabilityForChars, conditionalProbabilityForChars)
                wordEntropies[i] = self.calculateEntropyConditional(probabilityForWords, conditionalProbabilityForWords)

            self.plotEntropies(charEntropies, wordEntropies, filePath)











