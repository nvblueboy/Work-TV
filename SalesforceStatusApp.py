from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.logger import Logger

import requests, json, time

class Server():

	order = ["NA","CS","EU","AP"]

	def __init__(self, name, status):
		self.code = name[0:2].upper()
		self.num = int(name[2:])
		self.status = status
		self.component = ""
		self.name = name

	def __str__(self):
		cm = ""
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

class Event():

	def __init__(self, name, instances, startTime):
		self.name = name
		self.instances = instances
		self.startTime = startTime

class SalesforceStatusApp(RelativeLayout):

	updateTime = 300

	oldRunTime = 0

	setupDone = False

	boxes = {}

	statusString = StringProperty()
	affectedServers = StringProperty()

	def __init__(self,**kwargs):
		super(SalesforceStatusApp, self).__init__(**kwargs)
		if "app" in kwargs:
			self.app = kwargs["app"]
			self.setup()
		self.statusString = "Loading server data..."
		self.affectedServers = ""

	def setup(self):
		Logger.info("Salesforce Status: Setting up module.")
		self.headline = self.app.head
		self.caption = self.app.cap

	def updateServers(self):
		Logger.info("Salesforce Status: Updating info.")
		self.servers = []
		count = 0
		r = requests.get("https://api.status.salesforce.com/v1/instances/status")
		if r.status_code == 200:
			try:
				jsonData = json.loads(r.text)
				self.servers = []
				for server in jsonData:
					if server["status"] != "OK":
						s = Server(server["key"],server["status"])
						self.servers.append(s)
				if len(self.servers) == 0:
					self.statusString = "All servers operational."
					self.affectedServers = ""
					self.ids.status.pos_hint = {"top":.7}
				else:
					self.statusString = "Servers are impacted."
					self.affectedServers = makeServersString([svr.name for svr in self.servers], 8)
					self.ids.status.pos_hint = {"top":.9}
			except:
				Logger.error("Salesforce Status: Could not parse JSON." + r.text)
		else:
			Logger.error("Salesforce Status: Couldn't pull Salesforce status, status code: "+str(r.status_code))

	def updateCalendar(self):
		r = requests.get("https://api.status.salesforce.com/v1/maintenances?startTime="+time.strftime("%Y-%m-%d"))
		if r.status_code == 200:
			jsonData = json.loads(r.text)
			evts = {}
			for evt in jsonData:
				name = evt["name"]
				timeString = evt["plannedStartTime"]
				start = time.strptime(timeString,"%Y-%m-%dT%H:%M:%S.000Z")
				if timeString+name not in evts:
					evts[timeString+name] = Event(name, set(evt["instanceKeys"]), start)
				else:
					for server in list(evt["instanceKeys"]):
						evts[timeString+name].instances.add(server)
			self.evts = list(evts.values())
			self.evts.sort(key=lambda x: x.startTime)

		for i in range(3):
			e = self.evts[i]
			box = self.ids["evt_"+str(i)]
			box.eventName = time.strftime("%m/%d/%y: ", e.startTime) + e.name
			svrs = [Server(name, "") for name in e.instances]
			svrs.sort()
			box.servers = makeServersString([svr.name for svr in svrs], 6)


	def update(self, *args):
		if not self.setupDone:
			self.updateData()
			self.setupDone = True
		if self.oldRunTime != args[0]:
			if args[0] % self.updateTime == 0:
				self.updateData()
			self.oldRunTime = args[0]

	def updateData(self):
		Logger.info("Salesforce Status: Updating data.")
		self.updateServers()
		self.updateCalendar()


def makeServersString(instances, amount = 10):
	if len(instances) > amount:
		l = instances[:amount]
		extras = len(instances) - amount
		return ", ".join(l) + " + " + str(extras) + " more"
	else:
		return ", ".join(instances)

class EventBox(RelativeLayout):

	eventName = StringProperty()
	servers = StringProperty()

	def __init__(self,**kwargs):
		super(EventBox, self).__init__(**kwargs)
		


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

	print("Getting upcoming events...")

	r = requests.get("https://api.status.salesforce.com/v1/maintenances?startTime="+time.strftime("%Y-%m-%d"))
	if r.status_code == 200:
		jsonData = json.loads(r.text)
		evts = {}
		for evt in jsonData:
			name = evt["name"]
			timeString = evt["plannedStartTime"]
			start = time.strptime(timeString,"%Y-%m-%dT%H:%M:%S.000Z")
			if timeString+name not in evts:
				evts[timeString+name] = Event(name, set(evt["instanceKeys"]), start)
			else:
				for server in list(evt["instanceKeys"]):
					evts[timeString+name].instances.add(server)
		evts = list(evts.values())
		evts.sort(key=lambda x: x.startTime)


	instances = ["NA"+str(i) for i in range(20)]

	print(makeServersString(instances, 10))