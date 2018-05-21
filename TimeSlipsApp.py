from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.logger import Logger


import time, jsonRequests, json
import TimeSlipGraphUtility

from BaseApp import RelativeApp

class TimeSlipsApp(RelativeApp):

	lastValidData = ""

	updateTime = 300

	oldRunTime = 0

	source=StringProperty()
	img = ObjectProperty()


	def __init__(self,**kwargs):
		super(TimeSlipsApp, self).__init__(**kwargs)

	def setup(self):
		super(TimeSlipsApp, self).setup()

	def update(self, *args):
		super(TimeSlipsApp, self).update(*args)

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
