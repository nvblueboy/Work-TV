from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.logger import Logger


import time

import weathercodes, jsonRequests

from BaseApp import RelativeApp

class WeatherApp(RelativeApp):
	updated = False
	oldRunTime = 0

	location = "San+Juan+Capistrano,CA"

	updateTime = 600

	current_weather = StringProperty()

	def __init__(self,**kwargs):
		super(WeatherApp, self).__init__(**kwargs)

		self.current_weather = "Loading weather..."

	def setup(self):
		super(WeatherApp, self).setup()

	def update(self, *args):
		super(WeatherApp, self).update(*args)

	def updateData(self):
		baseurl = "https://query.yahooapis.com/v1/public/yql?q="
		query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+self.location+'")'
		form = "&format=json"
		response = jsonRequests.getResponse(baseurl+query+form)
		if response.status:
			jsonData = response.data
			try:
				item = jsonData["query"]["results"]["channel"]["item"]
			except:
				Logger.error("Weather App: jsonData was invalid.")
				return
			forecast=item["forecast"]
			condition=item["condition"]

			fc = forecast[0]
			temp = condition["temp"]
			cond = weathercodes.code_strings[condition["code"]]
			high = fc["high"]
			low = fc["low"]

			string = temp +" F | " + cond + " | "+high+ " / "+low

			self.current_weather = string

			for i in range(1,6):
				fc = forecast[i]
				widget = self.ids["day_"+str(i)]
				img = "./weather_icons/"+weathercodes.weathercodes[fc["code"]]
				widget.condition = img
				widget.day = weathercodes.days[fc["day"].encode('utf-8').lower()]
				widget.high = fc["high"]
				widget.low = fc["low"]
		else:
			Logger.error("WeatherApp: Couldn't update data: "+response.message)


class DayForecast(BoxLayout):
	def __init__(self,**kwargs):
		super(DayForecast, self).__init__(**kwargs)
