from kivy.uix.listview import ListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from algorithms.alignment import Alignment
from kivy.graphics import Color, Ellipse, Line
from random import random

class MainView(GridLayout):

	def on_touch_down(self, touch):

		self.alignment.step()
		self.alignment.output(self.table)
		self.draw_backpointers()

	def make_coords(self, coords, offset=(0,0)):
		col_width = self.width / self.cols
		row_height = self.height / self.rows

		y, x = coords

		x = (x + 1.5) * col_width
		y = self.height - (y + 1.5) * row_height

		x += offset[0]
		y += offset[1]

		return x, y

	def draw_backpointers(self):
		keys = self.alignment.backpointers.keys()
		#keys.sort()
		for key in keys:
			value = self.alignment.backpointers[key]

			offset = -20, 0
			if key[1] == value[1]:
				offset = 20, 0
			x1, y1 = self.make_coords(key, offset)

			offset2 = 20, 0
			x2, y2 = self.make_coords(value, offset2)



			#draw (x1,y1) -> (x2,y2)
			print x1, y1, x2, y2
			color = (random(), 1, 1)
			with self.canvas:
				Color(*color, mode='hsv')
				Line(points=[x1, y1, x2, y2], width=2)

	def __init__(self, **kwargs):

		self.table = []

		sequence1 = "AGC"
		sequence2 = "AAAC"
		self.alignment = Alignment(sequence1, sequence2)

		self.rows = rows = len(sequence2) + 2
		self.cols = cols = len(sequence1) + 2

		kwargs['cols'] = cols
		super(MainView, self).__init__(**kwargs)

		#create initial data structure
		for y in range(rows):
			row = []
			self.table.append(row)
			for x in range(cols):
				#label_text = "%d,%d"%(y, x)
				label_text = ""
				label= Label(text=label_text)
				row.append(label)
				self.add_widget(label)

		#Needleman-Wunsch

		self.alignment.output(self.table)



if __name__ == '__main__':
	from kivy.base import runTouchApp
	runTouchApp(MainView(width=800))