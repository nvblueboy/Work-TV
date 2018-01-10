from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty


import time, requests, json

import weathercodes



class WeatherApp(RelativeLayout):
	updated = False
	oldRunTime = 0

	weather_location = "San+Juan+Capistrano,CA"

	updateTime = 600

	current_weather = StringProperty()

	def __init__(self,**kwargs):
		super(WeatherApp, self).__init__(**kwargs)
		current_weather = "Loading weather..."


	def update(self, *args):
		if self.oldRunTime != args[0]:
			if args[0] % self.updateTime == 2:
				self.updateData()
			self.oldRunTime = args[0]

	def updateData(self):
		baseurl = "https://query.yahooapis.com/v1/public/yql?q="
		query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+self.weather_location+'")'
		form = "&format=json"
		r = requests.get(baseurl+query+form)

		if (r.status_code==200):
			# try:
				jsonData = json.loads(str(r.text).encode("utf-8"))
				item = jsonData["query"]["results"]["channel"]["item"]
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
			# except:
			# 	print("Failed to get latest weather.")

class Left(RelativeLayout):
	def __init__(self,**kwargs):
		super(Left, self).__init__(**kwargs)


class Right(BoxLayout):
	def __init__(self,**kwargs):
		super(Right, self).__init__(**kwargs)

class DayForecast(BoxLayout):
	def __init__(self,**kwargs):
		super(DayForecast, self).__init__(**kwargs)