import sys
import math
import random
import copy

from common import *

if(len(sys.argv) < 5):
    print "usage: python imm_predict.py train_real train_false test test.scores"
    exit(1)

#Get command-line arguments
trainingPositiveFilename = sys.argv[1]
trainingNegativeFilename = sys.argv[2]
testFilename = sys.argv[3]
testScoresFilename = sys.argv[4]

#Train positive and negative models
positiveSequences, positiveLength = readFile(trainingPositiveFilename)
negativeSequences, negativeLength = readFile(trainingNegativeFilename)
positive_imm = imm(positiveSequences, 5)
negative_imm = imm(negativeSequences, 5)

#read in test seqeunces
testSequences, testLength = readFile(testFilename)

#read in chi^2 -> pvalues conversion file
pvalues = read_pvalues("hw3_chisquare_df3_pvalues")

#score test sequences then output to file
outputFile = open(testScoresFilename, "w")
for sequence in testSequences:
	positive = positive_imm.score(sequence, 5, pvalues)
	negative = negative_imm.score(sequence, 5, pvalues)
	score = positive - negative
	outputFile.write(str(score) + "\n")
outputFile.close()
