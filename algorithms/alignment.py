class AlignmentNode:
	def __init__(self, score=0):
		this.score = score
		this.backpointers = []

class Alignment:
	"A class to execute the Needleman-Wunsch Algorithm"

	def __init__(self, sequence1, sequence2):
		self.sequence1 = sequence1.strip()
		self.width = len(self.sequence1) + 1

		self.sequence2 = sequence2.strip()
		self.height = len(self.sequence2) + 1

		self.match = 1
		self.mismatch = -1
		self.gap_penalty = -2

		self.stage = 0
		self.col = 0
		self.row = 0

		self.matrix = [[None for _ in range(self.width)] for _ in range(self.height)]

		self.local_align = False

	def set_parameters(self, match, mismatch, gap_penalty):
		"set the scoring parameters"
		self.match = match
		self.mismatch = mismatch
		self.gap_penalty = gap_penalty

	def output(self, table):
		"output matrix structure to a gui table"
		#draw first sequence
		sequence1 = "  " + self.sequence1
		for index, label in enumerate(table[0]):
			label.text = sequence1[index]

		#draw second sequence
		sequence2 = "  " + self.sequence2
		for y in range(len(table)):
			table[y][0].text = sequence2[y]

		#draw other cells
		for y in range(self.height):
			for x in range(self.width):
				if not self.matrix[y][x] is(None):
					table[y + 1][x + 1].text = str(self.matrix[y][x])
				else:
					table[y + 1][x + 1].text = "N/A"

	def step_initialize(self):
		"The algorithm's initialization step"
		if self.row == 0 and self.col == 0:
			self.matrix[0][0] = 0
			self.col += 1
		elif self.col < self.width:
			if self.local_align:
				self.matrix[0][self.col] = 0
			else:
				self.matrix[0][self.col] = self.gap_penalty * self.col
			self.col += 1
		else:
			index = self.row + 1
			if self.local_align:
				self.matrix[index][0] = 0
			else:
				self.matrix[index][0] = self.gap_penalty * index
			if index > self.height - 2:
				self.next_stage()
				return
			self.row += 1

	def step_through(self):
		"The algorithm's main computation step"
		left_score = self.matrix[self.row][self.col - 1] + self.gap_penalty
		up_score = self.matrix[self.row - 1][self.col] + self.gap_penalty

		match_score = self.matrix[self.row - 1][self.col - 1]
		if self.sequence1[self.col - 1] == self.sequence2[self.row - 1]:
			match_score += self.match
		else:
			match_score += self.mismatch

		scores = [left_score, up_score, match_score]
		if self.local_align:
			scores.append(0)

		self.matrix[self.row][self.col] = max(scores)

		self.col += 1
		if(self.col >= self.width):
			self.col = 1
			self.row += 1

	def next_stage(self):
		"Move onto the next stage in the algorithm"
		self.stage += 1
		self.row, self.col = 1, 1 #hackity hack hack, only 2 stages atm

	def step(self):
		"Step through the Needleman-Wunsch algorithm"
		if self.stage == 0:
			self.step_initialize()
		elif self.stage == 1:
			self.step_through()