from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.logger import Logger

import requests, json

class Server():

	order = ["NA","CS","EU","AP"]

	def __init__(self, name, status):
		self.code = name[0:2].upper()
		self.num = int(name[2:])
		self.status = status
		self.component = ""

	def __str__(self):
		if self.component != "":
			cm = ", Linked"
		return self.code + str(self.num) + ": " + self.status + cm

	def __lt__(self, other):
		o = {self.order[i]:i for i in range(len(self.order))}
		if o[self.code] < o[other.code]:
			return True
		elif o[self.code] > o[other.code]:
			return False
		else:
			return self.num < other.num

	def setComponent(self, component):
		self.component = component

	def updateBox(self):
		if self.component == "":
			return
		self.component.name = self.code + str(self.num)
		s = "cross.png"
		if self.status == "OK":
			s = "check.png"
		self.component.source = "./status_icons/"+s


class SalesforceStatusApp(BoxLayout):

	updateTime = 60

	oldRunTime = 0

	setupDone = False

	boxes = {}

	def __init__(self,**kwargs):
		super(SalesforceStatusApp, self).__init__(**kwargs)
		if "app" in kwargs:
			self.app = kwargs["app"]
			self.setup()

	def setup(self):
		self.headline = self.app.head
		self.caption = self.app.cap
		self.setupBoxes()

	def setupBoxes(self):
		count = 0
		for row in range(9):
			layout = BoxLayout()
			self.ids.rows.add_widget(layout)
			for column in range(20):
				server = SalesforceServer()
				self.boxes[count] = server
				count += 1
				layout.add_widget(server)
		self.setupDone = True

	def updateServers(self):
		self.servers = []
		count = 0
		r = requests.get("https://api.status.salesforce.com/v1/instances/status")
		if r.status_code == 200:
			try:
				jsonData = json.loads(r.text)
				self.servers = []
				for server in jsonData:
					s = Server(server["key"],server["status"])
					self.servers.append(s)
				self.servers.sort()
			except:
				Logger.error("Salesforce Status: Could not parse JSON." + r.text)
		else:
			Logger.error("Salesforce Status: Couldn't pull Salesforce status, status code: "+str(r.status_code))

	def updateBoxes(self):
		for boxNum in range(min(len(self.boxes),len(self.servers))):
			box = self.boxes[boxNum]
			server = self.servers[boxNum]
			server.setComponent(box)
			server.updateBox()


	def update(self, *args):
		if not self.setupDone:
			self.setupBoxes()
			self.updateServers()
			self.updateBoxes()
		if self.oldRunTime != args[0]:
			if args[0] % self.updateTime == 0:
				self.updateData()
			self.oldRunTime = args[0]

	def updateData(self):
		Logger.info("Salesforce Status: Updating data.")
		self.updateServers()
		self.updateBoxes()


class SalesforceServer(RelativeLayout):

	name = StringProperty()
	source = StringProperty()

	def __init__(self,**kwargs):
		super(SalesforceServer, self).__init__(**kwargs)


if __name__ == "__main__":
	s1 = Server("NA01","OK")
	s2 = Server("NA02","OK")
	s3 = Server("CS02", "OK")
	print(s1)
	print(s2)
	print(s1 < s2)
	print(s2 < s1)

	print(s3<s2)
	print(s2<s3)

	servers = []
	count = 0
	r = requests.get("https://api.status.salesforce.com/v1/instances/status")
	if r.status_code == 200:
		jsonData = json.loads(r.text)
		for server in jsonData:
			s = Server(server["key"],server["status"])
			servers.append(s)
		servers.sort()
		for server in servers: print(server)
		print(len(servers))