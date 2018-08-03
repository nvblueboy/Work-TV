from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.logger import Logger

import json, requests, time

from BaseApp import FloatApp

class CruiseTrackerApp(FloatApp):

	updateTime = 600

	image_source = StringProperty()

	first_run = False

	noResize=True
	
	def __init__(self, **kwargs):
		super(CruiseTrackerApp, self).__init__(**kwargs)
		first_run = False

	def setup(self):
		super(CruiseTrackerApp, self).setup()

	def update(self, *args):
		super(CruiseTrackerApp, self).update(*args)

		ratio = self.ids.image.image_ratio
		self.ids.image.size_hint = (1, ratio)

		if not self.first_run:
			self.updateData();
			self.first_run = True

	def updateData(self):
		Logger.info("Cruise Tracker: Getting info...")
		r = requests.get("http://www.cruisemapper.com/map/ships.json?minLat=-180&maxLat=180&minLon=-180&maxLon=180&filter=8191&zoom=9&imo=9304033&mmsi=309906000&t=1533314842", headers={"X-Requested-With":"XMLHttpRequest"})

		if r.status_code == 200:
			json_data = json.loads(r.text)
			freedom = None
			for obj in json_data:
				if (obj["ship_name"] == "Freedom Of The Seas"):
					freedom = obj
					break

			lat = freedom["lat"]
			lon = freedom["lon"]

			self.image_source = 'https://dev.virtualearth.net/REST/V1/Imagery/Map/road?centerPoint='+lat+','+lon+'&dpi=Large&ms=1920,1080&pp='+lat+','+lon+';35;JS&zoomLevel=7&key=ApgVA5QHntzi3mwA_psPY3oDE059zXuHbvG8m0IJaWqzsN7PJioBQDIRe7iARa-Q'
			#self.image_source = "https://maps.googleapis.com/maps/api/staticmap?format=png&center="+lat+","+lon+"&scale=2&zoom=4&size=1920x1080&maptype=roadmap&markers=color:blue%7Clabel:J%7C"+lat+","+lon+"7&key=AIzaSyAfMG6IprIdwwh4vvCxCjdonilRQYZynhc"
			print(self.image_source)
