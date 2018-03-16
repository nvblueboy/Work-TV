##Handles all weather.
from kivy.logger import Logger

import jsonRequests

import time

oldWeather = "Loading weather..."

def getWeather(location):
        global oldWeather
	baseurl = "https://query.yahooapis.com/v1/public/yql?q="
	query = 'select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+location+'")'
	form = "&format=json"
	response = jsonRequests.getResponse(baseurl+query+form)
	if response.status:
		jsonData = response.data
		condition = ""
		try:
			condition = jsonData["query"]["results"]["channel"]["item"]["condition"]
		except:
			oldWeather = "Could not get weather."
			return oldWeather	
		oldWeather = condition["temp"] + " F | " + condition["text"]
	else:
		Logger.error("Weather Module: Had issues: "+response.message)
	return oldWeather

forecast = ""
condition = ""

def getWeather_app(location):
	return None, None
	baseurl = "https://query.yahooapis.com/v1/public/yql?q="
	query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+location+'")'
	form = "&format=json"
	response = jsonRequests.getResponse(baseurl+query+form)
	if response.status:
		jsonData = response.data
		item = jsonData["query"]["results"]["channel"]["item"]
		forecast=item["forecast"]
		condition=item["condition"]
	else:
		Logger.error("Weather Module: Had issues: "+response.message)
	return forecast, condition

if __name__ == "__main__":
	print(getWeather("San+Juan+Capistrano,CA"))
	print(getWeather_app("San+Juan+Capistrano,CA"))
