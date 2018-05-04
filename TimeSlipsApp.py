from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.logger import Logger


import time, jsonRequests, json
import TimeSlipGraphUtility

class TimeSlipsApp(RelativeLayout):

	lastValidData = ""

	updateTime = 300

	oldRunTime = 0

	source=StringProperty()
	img = ObjectProperty()


	def __init__(self,**kwargs):
		super(TimeSlipsApp, self).__init__(**kwargs)
		if "app" in kwargs:
			self.app = kwargs["app"]
			self.setup()
		self.updateData()

	def setup(self):
		self.headline = self.app.head
		self.caption = self.app.cap

	def update(self, *args):
		if self.oldRunTime != args[0]:
			if args[0] % self.updateTime == 2:
				self.updateData()
				pass
			self.oldRunTime = args[0]

	def updateData(self):
		url = "https://www.softwareanywhere.com/services/apexrest/TimeSlips"
		response = jsonRequests.getResponse(url)
		if response.status:
			if response.raw != self.lastValidData:
				Logger.info("Time Slips App: Time Slips Changed.")
				parsed = json.loads(response.raw.decode('string-escape').strip('"'))
				TimeSlipGraphUtility.saveImage(parsed, "timeSlips.png")
				self.lastValidData = response.raw
				self.img.source = "timeSlips.png"
				self.img.reload()
