from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty, ObjectProperty
from kivy.logger import Logger

import requests, json

from BaseApp import RelativeApp

class TrafficApp(RelativeApp):

	oldRunTime = 0
	updateTime = 600

	source = StringProperty()

	img = ObjectProperty()

	noResize = True

	location = StringProperty()

	def __init__(self,**kwargs):
		super(TrafficApp, self).__init__(**kwargs)


	def setup(self):
		super(TrafficApp, self).setup()

	def update(self, *args):
		super(TrafficApp, self).update(*args)

	def updateData(self):
		url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Road?"+self.location
		self.source = url
		try:
			self.img.reload()
		except:
			Logger.info("Traffic Image App: Had issues reloading.")
