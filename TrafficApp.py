from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty, ObjectProperty
from kivy.logger import Logger

import requests, json

class TrafficApp(RelativeLayout):

	oldRunTime = 0
	updateTime = 600

	source = StringProperty()

	img = ObjectProperty()

	noResize = True

	location = StringProperty()

	def __init__(self,**kwargs):
		super(TrafficApp, self).__init__(**kwargs)
		if "app" in kwargs:
			self.app = kwargs["app"]
			self.setup()

	def setup(self):
		self.headline = self.app.head
		self.caption = self.app.cap
		self.location = self.app.loc
		self.updateData()

	def update(self, *args):
		if self.oldRunTime != args[0]:
			if args[0] % self.updateTime == 2:
				self.updateData()
			self.oldRunTime = args[0]

	def updateData(self):
		url = "https://rsz.io/dev.virtualearth.net/REST/v1/Imagery/Map/Road?"+self.location+"?format=jpg"
		self.source = url
		try:
			self.img.reload()
		except:
			Logger.info("Traffic Image App: Had issues reloading.")
