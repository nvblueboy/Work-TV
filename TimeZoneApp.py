from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty

import pytz, datetime

import time

class TimeZoneApp(RelativeLayout):

	fmt = "%I:%M:%S %p"
	pacifictz = pytz.timezone('US/Pacific')
	pacific = StringProperty()

	mountaintz = pytz.timezone('US/Mountain')
	mountain = StringProperty()

	centraltz = pytz.timezone('US/Central')
	central = StringProperty()

	easterntz = pytz.timezone('US/Eastern')
	eastern = StringProperty()

	date = StringProperty()

	def __init__(self,**kwargs):
		super(TimeZoneApp, self).__init__(**kwargs)

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

		self.date = str(time.strftime("%A, %B %d, %Y"))

		

class TimeZone(RelativeLayout):
	def __init__(self,**kwargs):
		super(TimeZone, self).__init__(**kwargs)