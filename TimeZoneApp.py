from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty

import pytz, datetime

import time

from BaseApp import RelativeApp

class TimeZoneApp(RelativeApp):

	fmt = "%I:%M:%S %p"
	pacifictz = pytz.timezone('US/Pacific')
	pacific = StringProperty()

	mountaintz = pytz.timezone('US/Mountain')
	mountain = StringProperty()

	centraltz = pytz.timezone('US/Central')
	central = StringProperty()

	easterntz = pytz.timezone('US/Eastern')
	eastern = StringProperty()

	alaskatz = pytz.timezone('US/Alaska')
	alaska = StringProperty()

	universaltz = pytz.timezone('Universal')
	universal = StringProperty()


	date = StringProperty()

	location = ""

	def __init__(self,**kwargs):
		super(TimeZoneApp, self).__init__(**kwargs)

	def setup(self):
		super(TimeZoneApp, self).setup()

	def update(self, *args):
		now = datetime.datetime.now()
		pacific_dt = self.pacifictz.localize(now)
		self.pacific = pacific_dt.strftime(self.fmt).lstrip("0")

		mountain_dt = pacific_dt.astimezone(self.mountaintz)
		self.mountain = mountain_dt.strftime(self.fmt).lstrip("0")

		central_dt = pacific_dt.astimezone(self.centraltz)
		self.central = central_dt.strftime(self.fmt).lstrip("0")

		eastern_dt = pacific_dt.astimezone(self.easterntz)
		self.eastern = eastern_dt.strftime(self.fmt).lstrip("0")

		alaska_dt = pacific_dt.astimezone(self.alaskatz)
		self.alaska = alaska_dt.strftime(self.fmt).lstrip("0")

		universal_dt = pacific_dt.astimezone(self.universaltz)
		self.universal = universal_dt.strftime(self.fmt).lstrip("0")

		self.date = str(time.strftime("%A, %B ")) + str(time.strftime("%d, ")).lstrip("0") + str(time.strftime("%Y"))

		

class TimeZone(RelativeLayout):
	def __init__(self,**kwargs):
		super(TimeZone, self).__init__(**kwargs)
