from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.logger import Logger

import time

from BaseApp import RelativeApp

class WelcomeGuestApp(RelativeApp):
	updated = False

	top_text = StringProperty()
	image_source = StringProperty()

	def __init__(self,**kwargs):
		super(WelcomeGuestApp, self).__init__(**kwargs)
		self.top_text = "Welcome to our guests!"
		self.image_source = "./images/CULogo.jpg"


	def setup(self):
		super(WelcomeGuestApp, self).setup()
		self.top_text = self.app.loc
		self.image_source = self.app.key

	def update(self, *args):
		if self.oldRunTime != args[0]:
			self.oldRunTime = args[0]
