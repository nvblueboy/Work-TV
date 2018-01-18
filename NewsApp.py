from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty

import requests, json

class NewsApp(FloatLayout):

	key = 'adae066eaedc43bfbc4a6de04096d189'

	location = "technology"

	ratio_set = False

	noResize = True

	updateTime = 600
	oldRunTime = 0

	article_source = StringProperty()
	article_headline = StringProperty()

	slideUpdated = False

	stringDict = None

	def __init__(self,**kwargs):
		super(NewsApp, self).__init__(**kwargs)
		if "app" in kwargs:
			self.app = kwargs["app"]
			self.setup()

	def setup(self):
		self.headline = self.app.head
		self.caption = self.app.cap
		try:
			self.location = self.app.loc
		except:
			print("Couldn't find a location. Assuming national...")
			self.location="national"
		self.key = self.app.key
		self.ratio_set = False
		self.updateData()

	def setStringDict(self, s):
		self.stringDict = s

	def update(self, *args):
		ratio = self.ids.image.image_ratio
		self.ids.image.size_hint = (1, ratio)
		self.ratio_set = True

		if self.oldRunTime != args[0]:
			if args[0] % self.updateTime == 0:
				self.updateData()
			self.oldRunTime = args[0]

	def updateData(self):
		url = "https://api.nytimes.com/svc/topstories/v2/"+self.location+".json?api-key="+self.key
		try:
			r = requests.get(url)
			if r.status_code == 200:
				jsonData = json.loads(r.text)
				result = jsonData["results"][0]
				if self.stringDict != None:
					# If a stringDict is wired up, then find an article not yet shown.
					count = 0
					while jsonData["results"][count]["title"].lower() in self.stringDict.values():
						count += 1
					result = jsonData["results"][count]
					self.stringDict[self.id] = result["title"].lower()
				title = result["title"]
				img = ""
				for m in result["multimedia"]:
					if m["format"] == "superJumbo":
						img = m["url"]
				self.article_source = img
				self.article_headline = title
			else:
				print("it doesn't work")

		except:
			print("Had issues getting news.")
