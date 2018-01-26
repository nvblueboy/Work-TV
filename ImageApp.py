from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty
from kivy.core.image import Image

class ImageApp(RelativeLayout):
	headline = StringProperty()
	caption = StringProperty()
	source = StringProperty()
	def __init__(self,**kwargs):
		super(ImageApp, self).__init__(**kwargs)
		self.headline = kwargs["headline"]
		self.caption = kwargs["caption"]
		self.source = kwargs["source"]