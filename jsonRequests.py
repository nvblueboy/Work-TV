#JSONRequests
#  A Module to handle requests to RESTful APIs
#  Dylan Bowman, 2018

import requests, json

class JSONResponseException(Exception):
    pass

class JSONResponse():
	def __init__(self, status, data="", raw="",message=""):
		self.status = status
		self.raw = raw
		if status:
			self.data = data
		else:
			self.message = message

	def __getitem__(self, key):
		return self.getValue(key)

	def __str__(self):
		outStr = "Status: "+str(self.status)
		if self.status:
			outStr += "\nRaw: " + self.raw
			outStr += "\nData: " + json.dumps(self.data, indent=4)
		else:
			outStr += "\nMessage: "+self.message
			if self.raw != "":
				outStr += "\nRaw: "+self.raw
		return outStr


	def getValue(self,key):
		if self.status:
			return self.data[key]
		else:
			raise JSONResponseException("The response is not valid.")

def getResponse(url):
	try:
		r = requests.get(url, timeout = 5)
	except:
		return JSONResponse(False, message = "Cannot reach endpoint.")
	if r.status_code == 200:
		try:
			jsonData = json.loads(r.text)
			return JSONResponse(True, raw = r.text, data = jsonData)
		except:
			return JSONResponse(False, raw = r.text, message = "Cannot parse JSON.")
	else:
		return JSONResponse(False, message = "Status code was not 200.")



if __name__=="__main__":
	baseurl = "https://query.yahooapis.com/v1/public/yql?q="
	query = 'select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text="orange,ca")'
	form = "&format=json"
	print(getResponse(baseurl+query+form))
	print(getResponse("http://notarestendpoint.com"))
	print(getResponse("https://api.nytimes.com/svc/topstories/v2/business.json"))
