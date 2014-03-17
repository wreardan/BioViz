import sys
import math
import random
import copy

from common import *

if(len(sys.argv) < 5):
    print "usage: python pwm_predict.py train_real train_false test test.scores"
    exit(1)

#Get command-line arguments
trainingPositiveFilename = sys.argv[1]
trainingNegativeFilename = sys.argv[2]
testFilename = sys.argv[3]
testScoresFilename = sys.argv[4]

#Read positive and negative sequences
positiveSequences, positiveLength = readFile(trainingPositiveFilename)
negativeSequences, negativeLength = readFile(trainingNegativeFilename)

#Compute positive and negative profile matrices
positiveModel = computeProfileWeightMatrix(positiveSequences)
negativeModel = computeProfileWeightMatrix(negativeSequences)

#Test sequences
def scoreSequences(sequences, matrix):
	scores = []
	for seq in sequences:
		score = 0.0
		for index, base in enumerate(seq):
			letter_index = dictionary[base]
			score += math.log(matrix[letter_index][index], 2)
		scores.append(score)
	return scores

#compute positive and negative scores
testSequences, testLength = readFile(testFilename)
positiveScores = scoreSequences(testSequences, positiveModel)
negativeScores = scoreSequences(testSequences, negativeModel)

#log(positive) - log(negative) = log(positive/negative)
scores = [pos - neg for pos, neg in zip(positiveScores, negativeScores)]

#write scores to output file
outputFile = open(testScoresFilename, "w")
for score in scores:
	outputFile.write(str(score) + "\n")
outputFile.close()

