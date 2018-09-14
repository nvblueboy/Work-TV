from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty, ObjectProperty
from kivy.logger import Logger

import json, requests, time

from BaseApp import FloatApp

class CruiseTrackerApp(FloatApp):

	updateTime = 600

	image_source = StringProperty()

	first_run = False

	img=ObjectProperty()

	noResize=True
	
	def __init__(self, **kwargs):
		super(CruiseTrackerApp, self).__init__(**kwargs)
		first_run = False

	def setup(self):
		super(CruiseTrackerApp, self).setup()

	def update(self, *args):
		super(CruiseTrackerApp, self).update(*args)

		ratio = self.ids.image.image_ratio
		self.ids.image.size_hint = (1, ratio)

		if not self.first_run:
			self.updateData();
			self.first_run = True

	def updateData(self):
		Logger.info("Cruise Tracker: Getting info...")
		self.image_source = 'http://webcamsdemexico.net/cancun1/live.jpg'
		try:
			self.img.reload()
		except:
			Logger.info("Cancun Image: Had issues reloading.")
		#self.image_source = "https://maps.googleapis.com/maps/api/staticmap?format=png&center="+lat+","+lon+"&scale=2&zoom=4&size=1920x1080&maptype=roadmap&markers=color:blue%7Clabel:J%7C"+lat+","+lon+"7&key=AIzaSyAfMG6IprIdwwh4vvCxCjdonilRQYZynhc"
		print(self.image_source)
