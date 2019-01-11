##Handles all weather.
from kivy.logger import Logger

import jsonRequests

import time

oldWeather = "Loading weather..."

def getWeather(location):
	global oldWeather
	# Using Weather.gov's API.
	
	forecast_url =  "https://api.weather.gov/gridpoints/SGX/43,50/forecast"
	observation_url = "https://api.weather.gov/stations/E2061/observations/latest"

	observation_response = jsonRequests.getResponse(observation_url)
	temp = 0
	if observation_response.status:
		try:
			jsonData = observation_response.data
			temp = celsiusToFahrenheit(jsonData["properties"]["temperature"]["value"])
		except Exception as e:
			print(e)
			oldWeather = "Could not get weather."
			return oldWeather

	forecast_response = jsonRequests.getResponse(forecast_url)
	high = 0
	low = 0
	if forecast_response.status:
		try:
			jsonData = forecast_response.data
			if jsonData["properties"]["periods"][0]["isDaytime"]:
				high = jsonData["properties"]["periods"][0]["temperature"]
				low = jsonData["properties"]["periods"][1]["temperature"]
			else:
				high = jsonData["properties"]["periods"][1]["temperature"]
				low = jsonData["properties"]["periods"][2]["temperature"]
		except Exception as e:
			print(e)
			oldWeather = "Could not get weather."

			return oldWeather

	oldWeather = str(int(round(temp))) + " F | " + str(high) + " / " + str(low)
	return oldWeather

forecast = ""
condition = ""

def celsiusToFahrenheit(celsius): return (9 * celsius / 5) + 32
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
