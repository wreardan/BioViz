import copy
import math
import sys

dictionary = {'A': 0, 'C': 1, 'G': 2, 'T': 3,
			  'a': 0, 'c': 1, 'g': 2, 't': 3,}
reverse_dictionary = ['A', 'C', 'G', 'T']

#read sequences into array (one sequence per line)
def readFile(filename):
	sequences = []
	max_length = 0
	file = open(filename, "r")
	for line in file:
		stripped = line.rstrip()
		sequences.append(stripped)
		if len(stripped) > max_length:
			max_length = len(stripped)
	file.close()
	return sequences, max_length

#utility function to create a width*height table
def createMatrix(width, height):
	return [[0.0 for x in xrange(width)] for x in xrange(height)]

#Compute PWM - count subsequence/total # subsequences 
def computeProfileWeightMatrix(sequences):
	matrix = createMatrix(len(sequences[0]), 4)
	#Count bases
	for seq in sequences:
		for index, letter in enumerate(seq):
			letter_index = dictionary[letter]
			matrix[letter_index][index] += 1
	#Normalize with pseudocounts (+1/+4)
	for base_index, base in enumerate(matrix):
		for col_index, col in enumerate(base):
			matrix[base_index][col_index] = (col + 1) / (len(sequences) + 4)
	return matrix

#Compute the consensus string
def getConsensus(matrix):
	consensus = ""
	for position in xrange(len(matrix[0])):
		max = 0.0
		max_letter = 0
		for base in xrange(len(matrix)):
			score = matrix[base][position]
			if(score > max):
				max = score
				max_letter = base
		consensus += reverse_dictionary[max_letter]
	return consensus

def compute_consensus(sequences):
	matrix = computeProfileWeightMatrix(sequences)
	return getConsensus(matrix)

#compute chi^2 score of contingency table
#currently accepts a 2x4 table with each column beinga distribution
#in the future, may want to generalize to MxN table
def chi_squared_score(matrix):
	#compute sum of all counts in table
	N = 0.0
	for i in xrange(len(matrix)):
		for j in xrange(len(matrix[0])):
			N += matrix[i][j]
	if N == 0:
		return 0.0
	#compute score
	score = 0.0
	for i in xrange(4):
		Ri = sum(matrix[i])
		for j in xrange(2):
			Cj = 0.0
			for x in xrange(4):
				Cj += matrix[x][j]
			#Eij = Ri*Cj/N
			Eij = Ri*Cj/N
			#(Oij - Eij)^2/Eij
			Oij = matrix[i][j]
			if(Eij != 0.0):
				score += (Oij - Eij)**2/Eij
	return score

#compute chi^2 test for two columns in the MDD model
def chi_squared_test(sequences, column1, column2, cc):
	matrix = [[0.0 for x in xrange(2)] for x in xrange(4)]
	#compute contingency table
	for sequence in sequences:
		i = sequence[column1]
		j = sequence[column2]
		index = dictionary[j]
		if(i == cc):
			matrix[index][0] += 1
		else:
			matrix[index][1] += 1
	#Compute chi squared score
	score = chi_squared_score(matrix)
	return score

#split sequences into two subsets
#  based on character @ position == true
def split_sequences(sequences, character, position):
	left = []
	right = []
	for sequence in sequences:
		c = sequence[position]
		if c == character:
			left.append(sequence)
		else:
			right.append(sequence)
	return left, right;

#fill in 1's for position columns that have already been computed
# (missing from positions list)
#this will make that columns calculation 0
def fill_in_pwm(matrix, positions):
	for base in xrange(len(matrix)):
		for pos in xrange(len(matrix[0])):
			if positions.count(pos) == 0:
				matrix[base][pos] = 1

#tree for problem 2 - MDD
class tree_node:
	def __init__(self):
		self.left = None		#left sbtree (matches condition)
		self.right = None		#right subtree (does not match condition)
		self.max_col = None		#maximizing position
		self.max_score = None	#maximum score = sum(chi squared) at position
		self.maxcc = None		#maximizing consensus character
		self.size = 0			#number of sequences beneath us
		self.matrix = None		#Partial PWM (actually the full PWM)

	#Score sequence by tree, run find_mdd_subtree() before this
	def score(self, sequence):
		if self.maxcc:
			#parent node
			base = sequence[self.max_col]
			base_index = dictionary[base]
			score = math.log(self.matrix[base_index][self.max_col], 2)
			if base == self.maxcc:
				score += self.left.score(sequence)
			else:
				score += self.right.score(sequence)
			return score
		else:
			#leaf nodes
			score = 0.0
			for index in xrange(len(self.matrix[0])):
				base = sequence[index]
				base_index = dictionary[base]
				score += math.log(self.matrix[base_index][index], 2)
			return score

	#output tree in tabbed format
	def display(self, tabs=""):
		#check if parent node or leaf node
		if self.maxcc:
			print tabs + "position " + str(self.max_col) + "==" + self.maxcc + ", score=" + str(self.max_score)
			for index, row in enumerate(self.matrix):
				print tabs + "  " + reverse_dictionary[index] + ": " + str( "{0:.2f}".format( row[self.max_col] ) )
		else:
			print tabs + "leaf node: " + str(self.size) + " sequences"
			for index, row in enumerate(self.matrix):
				pwm = ""
				for col in row:
					pwm += str( "{0:.2f}".format( col ) ) + " "
				print tabs + "  " + reverse_dictionary[index] + ": " + pwm
		#draw subtrees
		if(self.left):
			self.left.display(tabs + "\t")
		if(self.right):
			self.right.display(tabs + "\t")

	#MDD algorithm to construct tree
	def find_mdd_subtree(self, sequences, positions):
		self.size = len(sequences)
		self.matrix = computeProfileWeightMatrix(sequences)
		consensus = getConsensus(self.matrix)
		fill_in_pwm(self.matrix, positions)
		#find highest dependence
		max_score = -1000000
		max_col = positions[0]
		maxcc = ""
		#find highest scoring column
		for pos in positions:
			cc = consensus[pos]	#consensus character
			score = 0.0
			for pos2 in positions:	#should this be all positions?
				if(pos == pos2):
					continue
				score += chi_squared_test(sequences, pos, pos2, cc)
			if(score > max_score):
				max_score = score
				max_col = pos
				maxcc = cc
		if(max_score < 16.3 or len(sequences) < 400 or len(positions) == 0):
			#stop
			return
		else:
			#split tree up
			self.left = tree_node()
			self.right = tree_node()
			left, right = split_sequences(sequences, maxcc, max_col)
			positions.remove(max_col)
			self.left.find_mdd_subtree(left, copy.copy(positions))
			self.right.find_mdd_subtree(right, copy.copy(positions))
			pass
		self.max_col = max_col
		self.max_score = max_score
		self.maxcc = maxcc

#Problem 3
def read_pvalues(filename):
	pvalues = []
	file = open(filename, "r")
	for line in file:
		if line.find("p_value") != -1:	#ignore first line
			continue
		values = line.split(" ")
		pvalues.append(float(values[1].rstrip()))
	file.close()
	return pvalues

class imm:
	@staticmethod
	def get_subsequence_index(subsequence):
		index = 0
		for char in subsequence:
			index = index * 4 + dictionary[char]
		return index

	@staticmethod
	def count_subsequences(sequences, position, length):
		counts = [0] * 4**(length)
		for sequence in sequences:
			subsequence = sequence[position-length+1:position+1]
			index = imm.get_subsequence_index(subsequence)
			counts[index] += 1
		return counts

	@staticmethod
	def create_position_model(sequences, position, order):
		model = [[]] * (order + 1)
		if position < order:
			order = position
		for o in range(order + 1):
			model[o] = imm.count_subsequences(sequences, position, o + 1)
		return model
	
	def __init__(self, sequences, order):
		length = len(sequences[0])
		self.models = [[]] * length
	
		for position in range(length):
			self.models[position] = imm.create_position_model(sequences, position, order)

	def build_column(self, table, column, subsequence, position, order):
		column_sum = 0
		for row, base in enumerate(reverse_dictionary):
			lookup = subsequence + base
			index = imm.get_subsequence_index(lookup)
			table[row][column] = self.models[position][order][index]
			column_sum += table[row][column]
		return column_sum

	def score_orders(self, sequence, position, min_order):
		length = min_order
		lower_subsequence = sequence[position-length:position]
		length += 1
		higher_subsequence = sequence[position-length:position]

		matrix = createMatrix(2, 4)
		min_order_count = self.build_column(matrix, 0, lower_subsequence, position, min_order)
		next_order_count = self.build_column(matrix, 1, higher_subsequence, position, min_order + 1)
		return chi_squared_score(matrix), min_order_count, next_order_count

	def score(self, sequence, order, pvalues):
		total_score = 0.0
		for position, char in enumerate(sequence):
			#compute lambdas
			lambdas = [1.0]
			for o in xrange(min(position, order)):
				chi2, order_min_count, next_order_count = self.score_orders(sequence, position, o)
				p = pvalues[int(round(chi2 * 10))]
				d = 1 - p
				if next_order_count > 40:
					lambdas.append(1.0)
				elif d > 0.5:
					lambdas.append(d * next_order_count / 40.0)
				else:
					lambdas.append(0.0)
			#score character
			score = 0.0
			weight = 1.0
			for o in reversed(range(len(lambdas))):
				subsequence = sequence[position-o:position+1]
				index = imm.get_subsequence_index(subsequence)
				count = self.models[position][o][index]
				indices = [imm.get_subsequence_index(subsequence[:-1]+letter) for letter in reverse_dictionary]
				total_sum = sum([self.models[position][o][idx] for idx in indices])
				prob = ((count + 1.0) / (total_sum + 4.0))
				weighted = lambdas[o] * weight
#				print "  %f * %f"%(count + 1, total_sum + 4)
				score += prob * weighted
				weight *= 1 - lambdas[o]
#			print math.log(score, 2)
			total_score += math.log(score, 2)
#		print total_score
#		sys.exit()
		return total_score