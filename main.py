from kivy.uix.listview import ListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from alignment import Alignment

class MainView(GridLayout):

	def on_touch_down(self, touch):
		self.alignment.step()
		self.alignment.output(self.table)

	def __init__(self, **kwargs):

		self.table = []

		sequence1 = "AGC"
		sequence2 = "AAAC"
		self.alignment = Alignment(sequence1, sequence2)

		rows = len(sequence2) + 2
		cols = len(sequence1) + 2

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