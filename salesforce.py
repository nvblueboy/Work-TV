##Salesforce integration


import requests, json

class Slide():
	def __init__(self, img, head, cap):
		self.img = img
		self.head = head
		self.cap = cap
	def __str__(self):
		i = "Img: "+self.img
		h = "Head: "+self.head
		c = "Cap: "+self.cap
		return i + "\n" + h + "\n" + c

class App():
	def __init__(self, name, head, cap, loc):
		self.name = name
		self.head = head
		self.cap = cap
		self.loc = loc
	def __str__(self):
		n = "name: " + self.name
		h = "head: " + self.head
		c = "cap: " + self.cap
		l = "loc: " + self.loc

		return n + "\n" + h + "\n" + c + "\n" + l

				
def getData(debug = False):
	url = "https://dtb-sa.cs17.force.com/public/services/apexrest/WallBoard"
	r = requests.get(url)
	if r.status_code == 200:
		jsonData = json.loads(r.text.decode('string-escape').strip('"'))
		appList = []
		slideList = []
		if debug:
			print(json.dumps(jsonData, indent=4, sort_keys=True))
		for result in jsonData["slides"]:
			s = Slide(result["img"], result["head"], result["cap"])
			slideList.append(s)
		for result in jsonData["apps"]:
			a = App(result["app"], result["head"], result["cap"], result["loc"])
			appList.append(a)
		return appList, slideList

if __name__ == "__main__":
	print(getData(debug=True))