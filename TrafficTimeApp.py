from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty, ObjectProperty
from kivy.logger import Logger

import requests, json
import jsonRequests

from BaseApp import BoxApp

class TrafficTimeApp(BoxApp):

	oldRunTime = 0
	updateTime = 600

	location = ["Chapman University","John Wayne Airport","San Diego"]

	destinations = []
	objs = {}

	def __init__(self,**kwargs):
		super(TrafficTimeApp, self).__init__(**kwargs)

	def setup(self):
		l = self.app.loc.replace(", ",",").split(",")
		self.destinations = l[1:]
		self.here = l[0]
		super(TrafficTimeApp, self).setup()

	def update(self, *args):
		super(TrafficTimeApp, self).update(*args)

	def updateData(self):
		for loc in self.destinations:
			if loc not in self.objs:
				obj = TrafficTimeComponent(destination = loc, id=loc)
				self.ids.components.add_widget(obj)
				self.objs[loc] = obj
				
		for loc in self.objs.keys():
			if loc not in self.destinations:
				del self.objs[loc]
		times = self.getTrafficTime(self.here, self.destinations, self.api_key)

		if times != None:
			for loc in times.keys():
				if loc in self.objs:
					self.objs[loc].time = times[loc]

	oldAcceptable = ""

	def getTrafficTime(self, origin, destinations, api_key):

		d_query = "|".join(["+".join(x.split(" ")) for x in destinations])
		print(d_query)
		Logger.info("Traffic Time App: Loading times.")
		url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+("+".join(origin.split(" ")))+"&destinations="+d_query+"&departure_time=now&key="+self.api_key
		response = jsonRequests.getResponse(url)
		output = None
		if response.status:
			output = {}
			rows = response["rows"][0]["elements"]
			print(json.dumps(rows, indent=4))
			print(self.destinations)
			for i in range(len(self.destinations)):
				dest = self.destinations[i]
				row = rows[i]
				duration = -1
				if "duration_in_traffic" in row:
					duration = row["duration_in_traffic"]["text"]
				output[dest] = duration
			
		else:
			Logger.error("TrafficTimeApp: Failed to get latest traffic time: "+response.message) 

		return output


class TrafficTimeComponent(RelativeLayout):
	destination = StringProperty()
	time = StringProperty()
	def __init__(self, **kwargs):
		super(TrafficTimeComponent, self).__init__(**kwargs)
