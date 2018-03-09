from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.logger import Logger

import time

class WelcomeGuestApp(RelativeLayout):
	updated = False
	oldRunTime = 0

	top_text = StringProperty()
	image_source = StringProperty()

	def __init__(self,**kwargs):
		super(WelcomeGuestApp, self).__init__(**kwargs)
		self.top_text = "Welcome to our guests!"
		self.image_source = "./images/CULogo.jpg"
		if "app" in kwargs:
			self.app = kwargs["app"]
			self.setup()


	def setup(self):
		self.headline = self.app.head
		self.caption = self.app.cap
		self.top_text = self.app.loc
		self.image_source = self.app.key

	def update(self, *args):
		if self.oldRunTime != args[0]:
			self.oldRunTime = args[0]
