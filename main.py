from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.cache import Cache
from kivy.config import Config
from kivy.core.image import Image as CoreImage

import time,json

import weather

class Slide():
	def __init__(self, filename="./images/mountain.jpg", headline="Headline", caption="This is where a caption would go."):
		self.filename = filename
		self.headline = headline
		self.caption = caption
	def __str__(self):
            return("Filename: "+self.filename+"\nHeadline: " +self.headline + "\nCaption: "+self.caption)

class WorkTV(RelativeLayout):

	ImageSource = StringProperty()
	Headline = StringProperty()
	Caption = StringProperty()

	slideIndex = 0
	currentSlide = Slide()

	slideTime = 10


	def __init__(self, **kwargs):
		super(WorkTV, self).__init__(**kwargs)
		print("Initializing")
		fileHandle = open("./config.json")
		contents = fileHandle.read()
		fileHandle.close()
		try:
                    jsonData = json.loads(contents)
                except:
                    print("Something went wrong, dumping contents:")
                    print(contents)
                    quit()
		outList = []
		for d in jsonData["slides"]:
			s = Slide(d["img"],d["head"],d["desc"])
			outList.append(s)
		self.settings = jsonData["settings"]
		self.slideTime = self.settings["time"]
		self.weatherTime = self.settings["weather-update"]
		self.weatherLocation = self.settings["weather-location"]
		self.slides = outList
		
		print("Slides loaded:")
		for slide in self.slides:
                    print(slide)

		self.currentSlide = self.slides[self.slideIndex]
		self.ImageSource = self.currentSlide.filename
		self.updated = True
		self.oldTime = 0;
		self.runTime = 0;

	def setContainer(self, cont):
		self.container = cont;

	def update(self, *args):
		t = int(time.time())
		if t != self.oldTime:
			self.runTime += 1
			if self.runTime % self.slideTime == 0:
                                Cache.remove('kv.image')
                                Cache.remove('kv.texture')
				self.slideIndex = (self.slideIndex + 1) % len(self.slides)
				self.currentSlide = self.slides[self.slideIndex]
				self.ImageSource = self.currentSlide.filename
				print("Changed slide:")
				print(self.currentSlide)
				print("Read file: "+self.ImageSource)
			self.oldTime = t

		for child in self.children[0].children:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update(self.currentSlide, self.settings, self.runTime)



	def close(self, *args):
		for child in self.children[0].children:
			closeFN = getattr(child, "close", None)
			if callable(closeFN):
				child.close()	

class BottomRibbon(RelativeLayout):
	def __init__(self, **kwargs):
		super(BottomRibbon, self).__init__(**kwargs)
		self.slide=Slide()

	def update(self, *args):
		for child in self.children[0].children:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update(args)

	def setSlide(slide):
		self.slide = slide

class LogoBox(RelativeLayout):
	def __init__(self, **kwargs):
		super(LogoBox, self).__init__(**kwargs)

class CaptionBox(RelativeLayout):

	Headline = StringProperty()
	Caption = StringProperty()

	Weather = StringProperty()

	def __init__(self, **kwargs):
		super(CaptionBox, self).__init__(**kwargs)
		self.weatherString = "Loading weather..."

	def update(self, *args):
		self.Headline = args[0][0].headline
		self.Caption = args[0][0].caption

		if args[0][2] % args[0][1]["weather-update"] == 1:
			print("Updating weather")
			self.weatherString = weather.getWeather(args[0][1]["weather-location"])

		self.Weather = self.weatherString + " | " + time.strftime("%I:%M %p").lstrip("0")

class WorkTVApp(App):
	def build(self):
		Config.set('graphics', 'width', '1920')
		Config.set('graphics', 'height', '1080')
		Config.set('graphics', 'fullscreen', 'true')
		self.load_kv('WorkTV.kv')
		self.appWindow = WorkTV()
		self.appWindow.setContainer(self)
		Clock.schedule_interval(self.appWindow.update, .5)
		return self.appWindow
	def on_stop(self):
		self.appWindow.close()

if __name__ == "__main__":
	WorkTVApp().run()