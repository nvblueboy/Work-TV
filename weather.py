##Handles all weather.
from kivy.logger import Logger

import requests, json

import time

def getWeather(location):
	baseurl = "https://query.yahooapis.com/v1/public/yql?q="
	query = 'select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+location+'")'
	form = "&format=json"
	r = requests.get(baseurl+query+form)
        Logger.info("Weather Module: Updaing weather string @ "+time.strftime("%d %b %Y %H:%M:%S"))
	if (r.status_code==200):
		try:
			jsonData = json.loads(r.text)
			condition = jsonData["query"]["results"]["channel"]["item"]["condition"]
			return condition["temp"] + " F | " + condition["text"]
		except:
			Logger.error("Weather Module: Something went wrong: "+r.text)
			return "Failed to get weather."

def getWeather_app(location):
	baseurl = "https://query.yahooapis.com/v1/public/yql?q="
	query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+location+'")'
	form = "&format=json"
	r = requests.get(baseurl+query+form)
	Logger.info("Weather Module: Updating weather app @ "+time.strftime("%d %b %Y %H:%M:%S"))
	if (r.status_code==200):
		try:
			jsonData = json.loads(r.text)
			item = jsonData["query"]["results"]["channel"]["item"]
			forecast=item["forecast"]
			condition=item["condition"]
			return forecast, condition
		except:
			print("weather.getWeather_app(): Failed to get latest weather.")
			return False
if __name__ == "__main__":
	print(getWeather_app("San+Juan+Capistrano,CA"));
