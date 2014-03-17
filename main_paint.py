from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line


class MyPaintWidget(Widget):

	def on_touch_down(self, touch):
		color = (random(), 1, 1)
		with self.canvas:
			Color(*color, mode='hsv')
			d = 30.
			Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
			touch.ud['line'] = Line(points=(touch.x, touch.y))

	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]


class MyPaintApp(App):

	def build(self):
		parent = Widget()
		painter = MyPaintWidget()
		clearbtn = Button(text='Clear')
		parent.add_widget(painter)
		parent.add_widget(clearbtn)

		def clear_canvas(obj):
			painter.canvas.clear()

		clearbtn.bind(on_release=clear_canvas)

		# hello world text
		l = Label(text='Hello world')
		parent.add_widget(l)

		return parent


if __name__ == '__main__':
	MyPaintApp().run()