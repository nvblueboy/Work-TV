from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.image import Image
from kivy.properties import StringProperty, ObjectProperty
from kivy.logger import Logger

class BoxApp(BoxLayout):
	text_color = (.196,.416,.702,1)

	oldRunTime = 0
	updateTime = 60

	def __init__(self,**kwargs):
		super(BoxApp, self).__init__(**kwargs)
		if "app" in kwargs:
			self.app = kwargs["app"]

		self.oldRunTime = 0

	def setup(self):
		self.headline = self.app.head
		self.caption = self.app.cap
		self.api_key = self.app.key
		self.location = self.app.loc

		if len(self.children) > 0:
			for child in self.children[0].children:
				setupFN = getattr(child,"setup", None)

				if callable(setupFN):
					child.setup()

		updateDataFN = getattr(self, "updateData", None)
		if callable(updateDataFN):
			self.updateData()

	def update(self, *args):
		if args[0] > self.oldRunTime + self.updateTime:
			self.oldRunTime = args[0]
			updateDataFN = getattr(self, "updateData", None)

			if callable(updateDataFN):
				self.updateData()

		if len(self.children) > 0:
			for child in self.children[0].children:
				updateFN = getattr(child, "update", None)

				if callable(updateFN):
					child.update(args)


class RelativeApp(RelativeLayout):
	text_color =  (.196,.416,.702,1)

	oldRunTime = 0
	updateTime = 60

	def __init__(self,**kwargs):
		super(RelativeApp, self).__init__(**kwargs)
		if "app" in kwargs:
			self.app = kwargs["app"]

		self.oldRunTime = 0

	def setup(self):
		self.headline = self.app.head
		self.caption = self.app.cap
		self.api_key = self.app.key
		self.location = self.app.loc

		if len(self.children) > 0:
			for child in self.children[0].children:
				setupFN = getattr(child,"setup", None)

				if callable(setupFN):
					child.setup()

		updateDataFN = getattr(self, "updateData", None)
		if callable(updateDataFN):
			self.updateData()

	def update(self, *args):
		if args[0] > self.oldRunTime + self.updateTime:
			self.oldRunTime = args[0]
			updateDataFN = getattr(self, "updateData", None)

			if callable(updateDataFN):
				self.updateData()

		if len(self.children) > 0:
			for child in self.children[0].children:
				updateFN = getattr(child, "update", None)

				if callable(updateFN):
					child.update(args)


class FloatApp(FloatLayout):
	text_color = (.196,.416,.702,1)

	oldRunTime = 0
	updateTime = 60

	def __init__(self,**kwargs):
		super(FloatApp, self).__init__(**kwargs)
		if "app" in kwargs:
			self.app = kwargs["app"]

		self.oldRunTime = 0

	def setup(self):
		self.headline = self.app.head
		self.caption = self.app.cap
		self.api_key = self.app.key
		self.location = self.app.loc

		if len(self.children) > 0:
			for child in self.children[0].children:
				setupFN = getattr(child,"setup", None)

				if callable(setupFN):
					child.setup()

		updateDataFN = getattr(self, "updateData", None)
		if callable(updateDataFN):
			self.updateData()

	def update(self, *args):
		if args[0] > self.oldRunTime + self.updateTime:
			self.oldRunTime = args[0]
			updateDataFN = getattr(self, "updateData", None)

			if callable(updateDataFN):
				self.updateData()

		if len(self.children) > 0:
			for child in self.children[0].children:
				updateFN = getattr(child, "update", None)

				if callable(updateFN):
					child.update(args)