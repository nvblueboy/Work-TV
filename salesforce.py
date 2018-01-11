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

				
def getSlides():
	url = "https://dbowman-wix-developer-edition.na73.force.com/services/apexrest/WallBoard"
	r = requests.get(url)
	if r.status_code == 200:
		jsonData = json.loads(r.text.decode('string-escape').strip('"'))
		outList = []
		for result in jsonData["result"]:
			s = Slide(result["img"], result["head"], result["cap"])
			outList.append(s)
		return outList

def getApps():
	url = "https://dbowman-wix-developer-edition.na73.force.com/services/apexrest/WallBoardSettings"
	r = requests.get(url)
	if r.status_code == 200:
		jsonData = json.loads(r.text.decode('string-escape').strip('"'))
		outList = []
		for result in jsonData["result"]:
			a = App(result["app"], result["head"], result["cap"], result["loc"])
			outList.append(a)
		return outList



if __name__ == "__main__":
	s = getSlides()
	a = getApps()

	print("Slides: ")
	for i in s: print(i)

	print("Apps: ")
	for i in a: print(i)