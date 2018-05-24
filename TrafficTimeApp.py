from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty, ObjectProperty
from kivy.logger import Logger

import requests, json
import jsonRequests

class TrafficTimeApp(BoxLayout):

	oldRunTime = 0
	updateTime = 600

	location = ["Chapman University","John Wayne Airport","San Diego"]

	objs = {}

	def __init__(self,**kwargs):
		super(TrafficTimeApp, self).__init__(**kwargs)
		if "app" in kwargs:
			self.app = kwargs["app"]
			self.setup()

	def setup(self):
		self.headline = self.app.head
		self.caption = self.app.cap
		self.api_key = self.app.key
		l = self.app.loc.replace(", ",",").split(",")
		self.location = l[1:]
		self.here = l[0]
		self.updateData()

	def update(self, *args):
		if self.oldRunTime != args[0]:
			if args[0] % self.updateTime == 10:
				self.updateData()
			self.oldRunTime = args[0]

	def updateData(self):
		for loc in self.location:
			if loc not in self.objs:
				obj = TrafficTimeComponent(destination = loc, id=loc)
				self.ids.components.add_widget(obj)
				self.objs[loc] = obj
				
		for loc in self.objs.keys():
			if loc not in self.location:
				del self.objs[loc]

		for i in self.objs.keys():
			obj = self.objs[i]
			dest = obj.destination
			t = self.getTrafficTime(self.here, dest, self.api_key)
			if t != -1:
				obj.time = str(t)
				
	oldAcceptable = ""

	def getTrafficTime(self, origin, destination, api_key):
		Logger.info("Traffic Time App: Loading times.")
		url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+("+".join(origin.split(" ")))+"&destinations="+("+".join(destination.split(" ")))+"&departure_time=now&key="+self.api_key
		response = jsonRequests.getResponse(url)
		if response.status:
			if "duration_in_traffic" in response.data["rows"][0]["elements"][0]:
				self.oldAcceptable = response.data["rows"][0]["elements"][0]["duration_in_traffic"]["text"]
			else:
				Logger.error("TrafficTimeApp: Could not get traffic time from response: "+response.raw)
		else:
			Logger.error("TrafficTimeApp: Failed to get latest traffic time: "+response.message) 
			print(self.oldAcceptable)
			return self.oldAcceptable


class TrafficTimeComponent(RelativeLayout):
	destination = StringProperty()
	time = StringProperty()
	def __init__(self, **kwargs):
		super(TrafficTimeComponent, self).__init__(**kwargs)
