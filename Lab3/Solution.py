import math
import os
from collections import defaultdict
import random

class Solution:

    def getProbabilityForChars(self, filePath):
        file = open(filePath, 'r')
        count = defaultdict(int)
        totalChars = 0

        for line in file:
            for char in line:
                count[char] += 1
                totalChars += 1

        probability = {
            key: value / totalChars
            for key, value in count.items()
        }
        file.close()
        return probability

    def getProbabilityForWords(self, filePath):
        file = open(filePath, 'r')
        count = defaultdict(int)
        totalWords = 0

        for line in file:
            words = line.strip().split()
            for word in words:
                count[word] += 1
                totalWords += 1

        probability = {
            key: value / totalWords
            for key, value in count.items()
        }
        file.close()
        return probability

    def getJointAndConditionalProbabilityAccordingToPrevNChars(self,filePath, n):
        file = open(filePath, 'r')
        nPlusCount = defaultdict(int)
        nCount = defaultdict(int)

        for line in file:
            for i in range(n, len(line)):
                nPlusKey = line[i - n: i + 1]
                nKey = line[i - n: i]
                nPlusCount[nPlusKey] += 1
                nCount[nKey] += 1

        conditionalProbability = {
            key: nPlusCount[key] / nCount[key[:-1]]
            for key in nPlusCount
        }
        sumNPlusCount = sum(nPlusCount.values())
        jointProbability = {
            key: nPlusCount[key] / sumNPlusCount
            for key in nPlusCount
        }



        file.close()
        return jointProbability,conditionalProbability

    def getJointAndConditionalProbabilityAccordingToPrevNWords(self,filePath, n):
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

        sumNPlusCount = sum(nPlusCount.values())
        jointProbability = {
            key: nPlusCount[key] / sumNPlusCount
            for key in nPlusCount
        }

        file.close()
        return jointProbability,conditionalProbability

    def calculateEntropy(self,probability: dict) -> float:
        return -sum(p * math.log(p, 2) for p in probability.values() if p > 0)

    def calculateEntropyConditional(self, jointProbability, conditionalProbability: dict) -> float:
        entropy = 0
        for key in conditionalProbability:
            pJoint = jointProbability[key]
            pConditional = conditionalProbability[key]
            if pConditional > 0:
                entropy += pJoint * math.log2(pConditional)
        return -entropy

    def plotEntropies(self, charEntropies: dict, wordEntropies: dict, fileName) -> None:

        import matplotlib.pyplot as plt

        plt.plot(list(charEntropies.keys()), list(charEntropies.values()), label='Char Entropy')
        plt.plot(list(wordEntropies.keys()), list(wordEntropies.values()), label='Word Entropy')
        plt.xlabel('N')
        plt.ylabel('Entropy')
        plt.title('Entropy vs N for ' + fileName)
        plt.legend()
        plt.show()

    def plotAllEntropies(self, allCharEntropies: dict, allWordEntropies: dict) -> None:
        import matplotlib.pyplot as plt

        files = list(allCharEntropies.keys())
        filesCount = len(files)

        cols = 2
        rows = math.ceil(filesCount / cols)

        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), squeeze=False)
        axes = axes.flatten()

        for idx, filename in enumerate(files):
            ax = axes[idx]
            charEntropies = allCharEntropies[filename]
            wordEntropies = allWordEntropies[filename]

            ax.plot(list(charEntropies.keys()), list(charEntropies.values()),
                    marker='o', label='Char Entropy')
            ax.plot(list(wordEntropies.keys()), list(wordEntropies.values()),
                    marker='x', label='Word Entropy')

            ax.set_xlabel('N')
            ax.set_ylabel('Entropy (bits)')
            ax.set_title(f'Entropy vs N for {os.path.basename(filename)}')
            ax.legend()
            ax.grid(True)


        plt.tight_layout()
        plt.show()

    def generateZeroMarkovFile(self, n):
        print("Generating zero Markov file with n = ", n)
        file = open('Dane/zeroMarkov.txt', 'w')
        chars = 'abcdefghijklmnopqrstuvwxyz '
        for i in range(n):
            char = random.choice(chars)
            file.write(char)
        file.close()

    def run(self):

        fileNames = os.listdir('Dane')
        allCharEntropies = {}
        allWordEntropies = {}
        self.generateZeroMarkovFile(10788941)
        filePath = os.path.join('Dane', "zeroMarkov.txt")

        print("Entropy for zero Markov file: ")
        print("Char Entropy: ", self.calculateEntropy(self.getProbabilityForChars(filePath)))
        print("Word Entropy: ", self.calculateEntropy(self.getProbabilityForWords(filePath)))

        for filename in fileNames:
            print("calculating for file: ", filename)
            filePath = os.path.join('Dane', filename)

            probabilityForChars = self.getProbabilityForChars(filePath)
            probabilityForWords = self.getProbabilityForWords(filePath)

            charEntropies = dict()
            wordEntropies = dict()

            charEntropies[0] = self.calculateEntropy(probabilityForChars)
            wordEntropies[0] = self.calculateEntropy(probabilityForWords)

            for i in range(1,4):
                print("calculating for N = ", i)

                jointProbabilityForChars, conditionalProbabilityForChars = self.getJointAndConditionalProbabilityAccordingToPrevNChars(filePath, i)
                jointProbabilityForWords, conditionalProbabilityForWords = self.getJointAndConditionalProbabilityAccordingToPrevNWords(filePath, i)

                charEntropies[i] = self.calculateEntropyConditional(jointProbabilityForChars, conditionalProbabilityForChars)
                wordEntropies[i] = self.calculateEntropyConditional(jointProbabilityForWords, conditionalProbabilityForWords)

            allCharEntropies[filename] = charEntropies
            allWordEntropies[filename] = wordEntropies

        self.plotAllEntropies(allCharEntropies, allWordEntropies)











