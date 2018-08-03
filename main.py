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
from kivy.logger import Logger

import time

import ImageApp, TimeZoneApp, WeatherApp, TrafficApp, TrafficTimeApp, NewsApp, SalesforceStatusApp, salesforce, WelcomeGuestApp, TimeSlipsApp

import weather


restart_at_midnight = False
restart_time = "1426"

appObjs = {"TimeZoneApp":TimeZoneApp.TimeZoneApp, 
		   "WeatherApp":WeatherApp.WeatherApp, 
		   "TrafficApp":TrafficApp.TrafficApp,
		   "TrafficTimeApp":TrafficTimeApp.TrafficTimeApp,
		   "NewsApp":NewsApp.NewsApp,
		   "SalesforceStatusApp":SalesforceStatusApp.SalesforceStatusApp,
           "WelcomeGuestApp":WelcomeGuestApp.WelcomeGuestApp,
           "TimeSlipsApp":TimeSlipsApp.TimeSlipsApp}

class WorkTV(RelativeLayout):
	def __init__(self,**kwargs):
		super(WorkTV, self).__init__(**kwargs)

		self.ids.appContainer.setCaptionBox(self.ids.bottomRibbon.ids.captionBox)

	def update(self, *args):
		for child in self.children[0].children:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update(args)

	def setSlides(self, slides):
		self.ids.appContainer.setSlides(slides)

	def setApps(self, apps):
		self.ids.appContainer.setApps(apps)

	def updateCarousel(self, *args):
		data = salesforce.getData()
		if data:
			apps = data[0]
			slides = data[1]
			if apps or slides:
				self.setSlides(slides)
				self.setApps(apps)



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
	transitionTime = 10
	weatherUpdate = 600
	weatherLocation="San Juan Capistrano, CA"

	weatherUpdated = False

	firstRun = True

	stringDict = {}


	def __init__(self, **kwargs):
		super(AppContainer, self).__init__(**kwargs)
		self.runTime = 0
		self.oldTime = 0

		self.captionBox = None

		self.weatherString = weather.getWeather(self.weatherLocation)

		self.appWidgets = {}
		self.slideWidgets = {}

		self.frameStartTime = 0


	def setCaptionBox(self,captionBox):
		self.captionBox = captionBox

	def setSlides(self, slides):
		#Add or update apps.
		for slide in slides:
			#Determine if the app has updated (or is new).
			updated = True
			new = True
			if slide.img in self.slideWidgets:
				new = False
				w = self.slideWidgets[slide.img]
				if w.headline != slide.head or w.caption != slide.cap:
					updated = True
				else:
					updated = False
			else:
				new = True
				updated = False
			if new:
				image = ImageApp.ImageApp(source=slide.img,headline=slide.head,caption=slide.cap)
				self.ids.Carousel.add_widget(image)
				self.slideWidgets[slide.img] = image
				image.length = slide.length
			if updated:
				image = self.slideWidgets[slide.img]
				image.headline = slide.head
				image.caption = slide.cap
				image.length = slide.length
		currentImages = [slide.img for slide in slides]
		for slideName in self.slideWidgets.keys():
			if slideName not in currentImages:
				self.ids.Carousel.remove_widget(self.slideWidgets[slideName])
				del self.slideWidgets[slideName];



	def setApps(self, apps):
		for app in apps:
			updated = True
			new = True
			if app.id in self.appWidgets:
				new = False
				a = self.appWidgets[app.id]

				if a.id != app.id:
					updated = True
				else:
					updated = False
			else:
				new = True
				updated = False

			if new:
				size = (1,.8)

				if hasattr(appObjs[app.name],"noResize"):
					size = (1,1)

				a = appObjs[app.name](app=app, size_hint=size)
				a.id = app.id
				self.ids.Carousel.add_widget(a)

				if app.name == "NewsApp":
					a.setStringDict(self.stringDict)

				self.appWidgets[app.id] = a
				a.length = app.length
				a.setup()

			if updated:
				a = self.appWidgets[app.id]
				a.app = app
				a.length = app.length
				a.setup()
		#Remove apps.
		currentApps = [app.id for app in apps]
		for appName in self.appWidgets.keys():
			if appName not in currentApps:
				self.ids.Carousel.remove_widget(self.appWidgets[appName])
				del self.appWidgets[appName];

	def update(self, *args):

		for child in self.ids.Carousel.slides:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update(self.runTime)

		slide = self.ids.Carousel.current_slide
		
		if not hasattr(slide,"length") or slide.length == -1:
			slide.length = self.transitionTime

		if (self.captionBox != None):
			self.captionBox.headline = slide.headline
			self.captionBox.caption = slide.caption
			day = time.strftime("%d").lstrip("0")
			month = time.strftime("%m").lstrip("0")
			year = time.strftime("%Y")
			date = month + "/" + day + "/" + year
			self.captionBox.weather = self.weatherString + " | " +date + ", " + str(time.strftime("%I:%M:%S %p")).lstrip("0")

		if (int(time.time()) != self.oldTime):
			self.oldTime = int(time.time())
			self.runTime += 1

			if self.runTime - self.frameStartTime >= slide.length:
				self.ids.Carousel.load_next()
				self.frameStartTime = self.runTime

			if self.runTime % self.weatherUpdate == 0:
				Logger.info("AppContainer: Loading weather")
				self.weatherUpdated = True
				self.weatherString = weather.getWeather(self.weatherLocation)
				Logger.info("AppContainer: Weather String: "+self.weatherString)
					
			else:
				self.weatherUpdated = False

class WorkTVApp(App):
	def build(self):
		Config.set('graphics', 'width', '1600')
		Config.set('graphics', 'height', '900')
		Config.set('graphics', 'fullscreen', 'true')

		#Set configuration settings.
		Config.set('kivy', 'log_level', 'info')
		Config.set('kivy', 'log_dir', "logs")
		Config.set('kivy', 'log_name', "log_%y_%m_%d_%H_%M_%S.txt")
		Config.set('kivy', 'log_enable', 1)
		Config.set('kivy', 'log_maxfile', 50)

		self.load_kv('WorkTV.kv')
		self.appWindow = WorkTV()
		apps,slides = salesforce.getData()
		if apps or slides:
					self.appWindow.setSlides(slides)
					self.appWindow.setApps(apps)
		Clock.schedule_interval(self.appWindow.update, .2)
		Clock.schedule_interval(self.appWindow.updateCarousel, 20)
		return self.appWindow

if __name__ == "__main__":
	print("Loading app...")
	WorkTVApp().run()
