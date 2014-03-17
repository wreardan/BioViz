import sys
import math
import random
import copy

from common import *

if(len(sys.argv) < 5):
    print "usage: python mdd_predict.py train_real train_false test test.scores"
    exit(1)

#Get command-line arguments
trainingPositiveFilename = sys.argv[1]
trainingNegativeFilename = sys.argv[2]
testFilename = sys.argv[3]
testScoresFilename = sys.argv[4]

#Read positive and negative sequences
positiveSequences, positiveLength = readFile(trainingPositiveFilename)
negativeSequences, negativeLength = readFile(trainingNegativeFilename)

#Create PWM matrices
positiveModel = createMatrix(positiveLength, 4)
negativeModel = createMatrix(negativeLength, 4)

#Compute positive and negative profile matrices
positive_root = tree_node()
positive_root.find_mdd_subtree(positiveSequences, range(positiveLength))
#positive_root.display()	#uncommenting this will print the tree

#train model
negative_root = tree_node()
negative_root.find_mdd_subtree(negativeSequences, range(negativeLength))

#read in test scores
testSequences, testLength = readFile(testFilename)

#output test sequence scores
outputFile = open(testScoresFilename, "w")
for sequence in testSequences:
	positive = positive_root.score(sequence)
	negative = negative_root.score(sequence)
	#log(positive/negative) = log(positive) - log(negative)
	score = positive - negative
	outputFile.write(str(score) + "\n")
outputFile.close()
