from kivy.app import App
from kivy.config import Config
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty

import time

import ImageApp, TimeZoneApp


class WorkTV(RelativeLayout):
	def __init__(self,**kwargs):
		super(WorkTV, self).__init__(**kwargs)

		self.ids.appContainer.setCaptionBox(self.ids.bottomRibbon.ids.captionBox)

	def update(self, *args):
		for child in self.children[0].children:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update(args)

class BottomRibbon(RelativeLayout):
	def __init__(self, **kwargs):
		super(BottomRibbon, self).__init__(**kwargs)

	def update(self, *args):
		for child in self.children[0].children:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update(args)

class LogoBox(RelativeLayout):
	def __init__(self, **kwargs):
		super(LogoBox, self).__init__(**kwargs)

	def update(self, *args):
		for child in self.children[0].children:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update(args)

class CaptionBox(RelativeLayout):
	headline = StringProperty()
	caption = StringProperty()
	weather = StringProperty()

	def __init__(self, **kwargs):
		super(CaptionBox, self).__init__(**kwargs)

	def update(self, *args):
		for child in self.children[0].children:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update(args)			


class AppContainer(RelativeLayout):
	transitionTime = 5


	def __init__(self, **kwargs):
		super(AppContainer, self).__init__(**kwargs)
		self.runTime = 0
		self.oldTime = 0

		self.captionBox = None

	def setCaptionBox(self,captionBox):
		self.captionBox = captionBox

	def update(self, *args):
		for child in self.ids.Carousel.slides:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update(args)

		if (self.captionBox != None):
			slide = self.ids.Carousel.current_slide
			self.captionBox.headline = slide.headline
			self.captionBox.caption = slide.caption


		if (int(time.time()) != self.oldTime):
			self.oldTime = int(time.time())
			self.runTime += 1

			if self.runTime % self.transitionTime == 0:
				self.ids.Carousel.load_next()	

class WorkTVApp(App):
	def build(self):
		Config.set('graphics', 'width', '1920')
		Config.set('graphics', 'height', '1080')
		Config.set('graphics', 'fullscreen', 'true')
		self.load_kv('WorkTV.kv')
		self.appWindow = WorkTV()
		Clock.schedule_interval(self.appWindow.update, .2)
		return self.appWindow

if __name__ == "__main__":
	WorkTVApp().run()